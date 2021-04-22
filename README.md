# The Notionally Awesome Relay Controller Project (NARC-P)
- This project is an OpenAPI-Spec v3 API platform based on FastAPI and is used to control WebAPI-based controller boards via TCP/IP in a JSON-formatted interchange
- This document assumes familiarity with Linux services, Python, PIP, WebAPI, JSON and Docker development

### Usage:
- The service can be used by any framework and in any language that can handle standard WebAPI requests
- [Postman](https://www.postman.com) is an excellent and intuitive GUI-based WebAPI utility and is available for Windows, MacOS and Linux
- Authentication must be provided via encoded request header. User credentials are maintained on the Linux host
- This service stores no data except as indicated below. This includes user credentials or device state
- FastAPI has a baked-in documentation page at '.../api/docs'
- There are currently two url paths to service requests. The ellipses assume the https:// host path to the service:
  - '.../api/getDeviceStatus/deviceName' - this path simply returns the current status of the select device
  - '.../api/[enable|disable]deviceRelay/deviceName' - this path uses a named relay structure to activate or deactivate a named relay
- The service can currently interface with one board type: [Velleman VM-204](https://www.velleman.eu/products/view/?id=420454)

### Data stores:
- There are two data stores, both JSON files:
- The device store is used as a reference for all devices:
```JSON
{
  "name": "DeviceOne",
  "model": "vm204",
  "site": "Remote-101",
  "protocol": "https",
  "address": "192.168.200.5",
  "port": 443,
  "key": "S3cr3tK3y",
  "relays": [
    {
      "relay": 1,
      "name": "PrimaryPump",
      "enable": "on",
      "disable": "off"
    }
  ]
}
```

- For the example above, the URL paths to view or operate this would be '.../api/getDeviceStatus/DeviceOne' or '.../api/enablePrimaryPump/DeviceOne', respectively

- The second is the task store and can be used to control multiple devices:
```JSON
{
  "name": "EmergencyShutdown",
  "relays": [
    {
      "name": "DeviceOne",
      "relay": 1,
      "enable": "off",
      "disable": "on"
    }
  ]
}
```
- In this example, the URL '.../api/enableEmergencyShutdown/all' (note the 'all' keyword) is used to activate the task. By design, the 'enable' keyword is used to trigger the 'off' keyword specific to the device in this instance

### Notes:
- The service is set to HTTPS with a local developer certificate. Replace with a valid cert before going live
- The project files include a [Docker](https://www.docker.com/) configuration file for image builds
- Device reachability can (and should) always be validated directly by using Postman from the same subnet as the host
- Closely examine the data stores and be comfortable with JSON before attempting any changes

### Project dependencies (latest versions):
- Python >=3.9.x installed. Python libraries via PIP for all else:
  - [pytest (dev)](https://github.com/pytest-dev/pytest)
  - [pytest-cov (dev)](https://github.com/pytest-dev/pytest-cov)
  - [pytest_httpx (dev)](https://github.com/Colin-b/pytest_httpx)
  - [pytest-asyncio (dev)](https://github.com/pytest-dev/pytest-asyncio)
  - [requests (dev)](https://github.com/psf/requests)
  - [httpx](https://github.com/encode/httpx/)
  - [uvicorn](https://github.com/encode/uvicorn)
  - [fastapi](https://github.com/tiangolo/fastapi)
  - [first](https://pypi.org/project/first/)
  - [simplepam](https://github.com/leonnnn/python3-simplepam)

### References:
- [OpenAPI](https://github.com/OAI/OpenAPI-Specification)
- [FastAPI](https://fastapi.tiangolo.com)
- [JSON](https://json-schema.org/)