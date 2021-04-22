from pydantic import BaseModel
from typing import List


class InputState(BaseModel):

  input: int
  name: str
  isTriggered: bool


class RelayState(BaseModel):

  relay: int
  name: str
  isEnabled: bool


class DeviceState(BaseModel):

  relays: List[RelayState]
  inputs: List[InputState]
  shelterTemp: float
