import subprocess
from time import sleep
import const
from modules.base.module import Module

class Ping(Module):
  def __init__(self, name: str, ip: str) -> None:
    super().__init__()

    self.name = name
    self.ip = ip
    self.homeassistant_discovery_type = "binary_sensor"
    self.homeassistant_unique_id = "ping_{}".format(name.replace(" ", "-"))

  @property
  def discovery_config(self) -> object:
    return {
      "name": "{} Ping ({})".format(const.DEVICE_NAME, self.name),
      "unique_id": self.homeassistant_real_unique_id,
      "state_topic": self.get_real_topic("ping/{}/state".format(self.name.replace(" ", "-"))),
      "payload_on": "OK",
      "payload_off": "NOT_OK",
    }

  def run(self) -> None:
    super().run()

    while True:
      if hasattr(self, "client") and self.client.is_connected():
        if subprocess.run(["ping", "-c", "1", "-w", "10", self.ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
          self.client.publish(self.get_real_topic("ping/{}/state".format(self.name.replace(" ", "-"))), "OK")
        else:
          self.client.publish(self.get_real_topic("ping/{}/state".format(self.name.replace(" ", "-"))), "NOT_OK")

      sleep(30)
