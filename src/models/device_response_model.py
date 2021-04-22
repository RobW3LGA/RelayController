from pydantic import BaseModel


class DeviceResponse(BaseModel):

  statusCode: int
  response: dict
