import httpx
from httpx import AsyncClient
from fastapi import HTTPException

from .devices import vm204Response

from models import Device, Relay, DeviceResponse


def missingModelException(device: Device, relay: any, taskVerb: any) -> HTTPException:

  raise HTTPException(status_code=404, detail={"error": device.model, "reason": "unsupported device"})


def useDeviceModel(deviceModel: str) -> callable:

  deviceModels: dict = {

    "vm204": vm204Response
  }

  return deviceModels.get(deviceModel, missingModelException)


def getDeviceResponse(device: Device, relay: Relay = None, taskVerb: str = "") -> DeviceResponse:

  getResponse: callable = useDeviceModel(deviceModel=device.model)
  return getResponse(device=device, relay=relay, taskVerb=taskVerb)
