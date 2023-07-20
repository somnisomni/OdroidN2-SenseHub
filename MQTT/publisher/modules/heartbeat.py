from time import sleep
import const
from modules.base.module import Module

class Heartbeat(Module):
  def __init__(self) -> None:
    super().__init__()

    self.homeassistant_discovery_type = "binary_sensor"
    self.homeassistant_unique_id = "heartbeat"

  @property
  def discovery_config(self) -> object:
    return {
      "name": "{} MQTT Heartbeat".format(const.DEVICE_NAME),
      "unique_id": self.homeassistant_real_unique_id,
      "state_topic": self.get_real_topic("heartbeat/state"),
      "payload_on": "OK",
      "off_delay": 35,
    }

  def run(self) -> None:
    super().run()

    while True:
      if hasattr(self, "client") and self.client.is_connected():
        self.client.publish(self.get_real_topic("heartbeat/state"), "OK")

      sleep(30)
