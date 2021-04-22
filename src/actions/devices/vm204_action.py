import httpx
from httpx import Response, TimeoutException

from pydantic import BaseModel
from typing import List

from datetime import datetime

from models import Device, Relay, DeviceState, RelayState, InputState, DeviceResponse
from settings import apiServiceParam


class Vm204ResponseBody(BaseModel):

  relays: List[bool]
  inputs: List[bool]
  analog: float


async def vm204Response(device: Device, relay: Relay = None, taskVerb: str = "") -> DeviceResponse:

  deviceUri: str
  statusCode: int

  if relay is None:

    deviceUri = f"{device.protocol}://{device.address}:{device.port}/api/status?key={device.key}"
    statusCode = 200

  else:

    relayState: str = (relay.dict())[taskVerb]
    deviceUri = f"{device.protocol}://{device.address}:{device.port}/api/relay/{relayState}?relay={relay.relay}&key={device.key}"
    statusCode = 201

  try:

    async with httpx.AsyncClient() as client:
      response: Response = await client.get(url=deviceUri, timeout=apiServiceParam["httpxClientTimeout"])

    if response.status_code == 200:

      responseBody: Vm204ResponseBody = Vm204ResponseBody.parse_obj(response.json())

      relayState: List[RelayState] = []
      for index, isEnabled in enumerate(responseBody.relays):

        deviceRelay: RelayState = RelayState(relay=device.relays[index].relay, name=device.relays[index].name, isEnabled=isEnabled)
        relayState.append(deviceRelay)

      inputState: List[InputState] = []
      for index, isTriggered in enumerate(responseBody.inputs):

        deviceInput: InputState = InputState(input=device.inputs[index].input, name=device.inputs[index].name, isTriggered=isTriggered)
        inputState.append(deviceInput)

      deviceState: DeviceState = DeviceState(relays=relayState, inputs=inputState, shelterTemp=responseBody.analog)
      content: dict = {"device": device.name, "state": deviceState.dict(), "timestamp": str(datetime.now()), "responseMs": (response.elapsed.microseconds * .01)}

      return DeviceResponse(statusCode=statusCode, response=content)

    else:

      content: dict = {"device": device.name, "error": response.status_code, "reason": response.text, "timestamp": str(datetime.now()), "responseMs": (response.elapsed.microseconds * .01)}
      return DeviceResponse(statusCode=response.status_code, response=content)

  except TimeoutException:
    return DeviceResponse(statusCode=404, response={"device": device.name, "address": device.address, "reason": "unreachable"})
