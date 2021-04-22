from models import DeviceSource


deviceSource: DeviceSource = DeviceSource.parse_obj({
  "allRelays": ["testRelayOneOne", "testRelayTwoOne"],
  "devices": [
    {
      "name": "testDeviceOne",
      "model": "vm204",
      "site": "testSite",
      "protocol": "https",
      "address": "1.2.3.4",
      "port": 123,
      "key": "Sup3rS3kr3tK3y",
      "relays": [
        {
          "relay": 1,
          "name": "testRelayOneOne",
          "enable": "on",
          "disable": "off"
        }
      ],
      "inputs": [
        {
          "input": 1,
          "name": "testInputOneOne"
        },
      ]
    },
    {
      "name": "testDeviceTwo",
      "model": "vm204",
      "site": "testSite",
      "protocol": "https",
      "address": "1.2.3.4",
      "port": 123,
      "key": "Sup3rS3kr3tK3y",
      "relays": [
        {
          "relay": 1,
          "name": "testRelayTwoOne",
          "enable": "on",
          "disable": "off"
        }
      ],
      "inputs": [
        {
          "input": 1,
          "name": "testInputTwoOne"
        },
      ]
    }
  ]
})
