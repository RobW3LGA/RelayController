from pydantic import BaseModel
from typing import List


class Input(BaseModel):

  input: int
  name: str


class Relay(BaseModel):

  relay: int
  name: str
  enable: str
  disable: str


class Task(BaseModel):

  name: str
  relays: List[Relay]


class Device(BaseModel):

  name: str
  model: str
  site: str
  protocol: str
  address: str
  port: int
  key: str
  relays: List[Relay]
  inputs: List[Input]


class TaskSource(BaseModel):

  allowedUsers: List[str]
  allTasks: List[str]
  tasks: List[Task]


class DeviceSource(BaseModel):

  allRelays: List[str]
  devices: List[Device]
