from json import JSONEncoder
from time import sleep
from modules.base.module import Module
from modules.base.cpu_cluster import CPUCluster

class System_N2(Module):
  def __init__(self):
    super().__init__()

    self.homeassistant_discovery_type = "sensor"
    self.homeassistant_unique_id = "system"

    self.clusters = [CPUCluster(self, 0), CPUCluster(self, 2)]

  @property
  def discovery_config(self) -> object:
    config = []

    for cluster in self.clusters:
      config.append(cluster.DISCOVERY_CONFIG_CUR)
      config.append(cluster.DISCOVERY_CONFIG_MAX)
      config.append(cluster.DISCOVERY_CONFIG_MIN)

    return config

  def send_discovery(self) -> None:
    for cluster in self.clusters:
      self.client.publish(cluster.DISCOVERY_TOPIC_CUR, JSONEncoder().encode(cluster.DISCOVERY_CONFIG_CUR), retain=True)
      self.client.publish(cluster.DISCOVERY_TOPIC_MAX, JSONEncoder().encode(cluster.DISCOVERY_CONFIG_MAX), retain=True)
      self.client.publish(cluster.DISCOVERY_TOPIC_MIN, JSONEncoder().encode(cluster.DISCOVERY_CONFIG_MIN), retain=True)

  def run(self) -> None:
    super().run()

    while True:
      if hasattr(self, "client") and self.client.is_connected():
        output = {}

        ## Get frequencies per cluster ##
        for cluster in self.clusters:
          output.update(cluster.get_values())

        ## MQTT Publish ##
        self.client.publish(self.get_real_topic("system/state"), JSONEncoder().encode(output))

      sleep(10)
