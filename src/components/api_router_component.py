from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import List
from first import first
import re as regex

from models import DeviceSource, Device, Relay, TaskSource, Task, DeviceResponse
from actions import getDeviceResponse


def invokeApiRoutes(apiRouter: APIRouter, deviceSource: DeviceSource, taskSource: TaskSource, isAuthenticated: callable):

  @apiRouter.get(path="/getDeviceStatus/{device_name}")
  async def get_device_status(device_name: str, authHeader: HTTPBasicCredentials = Depends(HTTPBasic())) -> JSONResponse:

    deviceName: str = str(device_name).lower()
    if deviceName == "all":

      if isAuthenticated(username=authHeader.username, password=authHeader.password):

        deviceResponses: List[DeviceResponse] = [(await getDeviceResponse(device=device)) for device in deviceSource.devices]

        statusCode: int = 200
        for deviceResponse in deviceResponses:
          if deviceResponse.statusCode > statusCode:
            statusCode = deviceResponse.statusCode

        contentList: List[{}] = []
        for deviceResponse in deviceResponses:
          contentList.append(deviceResponse.dict())

        return JSONResponse(status_code=statusCode, content=contentList)

    else:

      device: Device = first([device for device in deviceSource.devices if device.name.lower() == deviceName])
      if device is None:

        raise HTTPException(status_code=400, detail={"error": device_name, "reason": "invalid device"})

      if isAuthenticated(username=authHeader.username, password=authHeader.password):

        deviceResponse: DeviceResponse = await getDeviceResponse(device=device)
        return JSONResponse(status_code=deviceResponse.statusCode, content=deviceResponse.response)

  @apiRouter.get("/{task_name}/{device_name}")
  async def invoke_tasks(task_name: str, device_name: str, authHeader: HTTPBasicCredentials = Depends(HTTPBasic())):

    taskSections: Match = regex.search(r"^(enable|disable){1}([\w\-\d]+){1}$", task_name.lower())

    try:
      lastIndex: int = taskSections.lastindex

    except Exception:
      raise HTTPException(status_code=400, detail={"error": task_name, "reason": "invalid task"})

    if authHeader.username.lower() not in [user.lower() for user in taskSource.allowedUsers]:
      raise HTTPException(status_code=401, detail={"error": authHeader.username, "reason": "authorization failure"})

    deviceName: str = str(device_name.lower())
    taskVerb: str = str(taskSections[1].lower())
    taskName: str = str(taskSections[2].lower())

    if deviceName == "all":

      if taskName not in [task.lower() for task in taskSource.allTasks]:
        raise HTTPException(status_code=400, detail={"error": task_name, "reason": "invalid task request"})

      if isAuthenticated(username=authHeader.username, password=authHeader.password):

        validTask: Task = first([task for task in taskSource.tasks if task.name.lower() == taskName])
        devices: List[Device] = [device for device in deviceSource.devices for relay in validTask.relays if device.name.lower() == relay.name.lower()]
        deviceResponses: List[DeviceResponse] = [
          (await getDeviceResponse(
            device=device,
            relay=first([relay for relay in validTask.relays if device.name.lower() == relay.name.lower()]),
            taskVerb=taskVerb
          )) for device in devices]

        statusCode: int = 200
        for deviceResponse in deviceResponses:
          if deviceResponse.statusCode > statusCode:
            statusCode = deviceResponse.statusCode

        contentList: List[{}] = []
        for deviceResponse in deviceResponses:
          contentList.append(deviceResponse.dict())

        return JSONResponse(status_code=statusCode, content=contentList)

    if taskName not in [relay.lower() for relay in deviceSource.allRelays]:
      raise HTTPException(status_code=400, detail={"error": task_name, "reason": "invalid device request"})

    device: Device = first([device for device in deviceSource.devices if device.name.lower() == deviceName])
    if device is None:

      raise HTTPException(status_code=400, detail={"error": device_name, "reason": "invalid device"})

    if isAuthenticated(username=authHeader.username, password=authHeader.password):

      validDevice: Device = first([device for device in deviceSource.devices if device.name.lower() == deviceName for relay in device.relays if relay.name.lower() == taskName])
      validRelay: Relay = first([relay for relay in validDevice.relays if relay.name.lower() == taskName])

      deviceResponse: DeviceResponse = await getDeviceResponse(device=validDevice, relay=validRelay, taskVerb=taskVerb)
      return JSONResponse(status_code=deviceResponse.statusCode, content=deviceResponse.response)
