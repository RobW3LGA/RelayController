apiServiceParam: dict = {

  "allhosts": "0.0.0.0",
  "port": 443,
  "ssl_certfile": "./src/settings/cert/cert",
  "ssl_keyfile": "./src/settings/cert/key",
  "device_db": "./src/settings/devices.setting.json",
  "task_db": "./src/settings/tasks.setting.json",
  "docs_url": "/api/docs",
  "redoc_url": "/api/redoc",
  "prefix": "/api",
  "lifespan": "auto",
  "log_level": "debug",
  "httpxClientTimeout": 1.5,
  "allow_credentials": True,
  "allow_headers": {

    "Authorization"
  },
  "allow_methods": {

    "GET",
    "POST"
  },
  "allow_origins": {

    "https://127.0.0.1",
  }
}
