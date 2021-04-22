from models import TaskSource


taskSource: TaskSource = TaskSource.parse_obj({
  "allowedUsers": ["test@email.local"],
  "allTasks": ["testTaskOne"],
  "tasks": [
    {
      "name": "testTaskOne",
      "relays": [
        {
          "name": "testDeviceOne",
          "relay": 1,
          "enable": "on",
          "disable": "off"
        },
        {
          "name": "testDeviceTwo",
          "relay": 1,
          "enable": "on",
          "disable": "off"
        }
      ]
    }
  ]
})
