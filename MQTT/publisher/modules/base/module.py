import const
from abc import ABCMeta, abstractmethod, abstractproperty
from json import JSONEncoder
from threading import Thread
from paho.mqtt.client import Client

class Module(Thread, metaclass=ABCMeta):
  def __init__(self) -> None:
    Thread.__init__(self)
    self.daemon = True

    self.homeassistant_discovery_type = "binary_sensor"
    self.homeassistant_unique_id = "unique_id"

  def set_mqtt_client(self, client: Client) -> None:
    self.client = client

  def get_real_topic(self, topic: str) -> str:
    return "{}{}".format(const.ROOT_TOPIC, topic)

  @property
  def homeassistant_real_unique_id(self) -> str:
    return "{}_{}".format(const.DEVICE_NAME_SHORT, self.homeassistant_unique_id)

  @property
  def homeassistant_discovery_topic(self) -> str:
    return "{}{}".format(
      const.HOMEASSISTANT_DISCOVERY_ROOT_TOPIC,
      "{}/{}/config".format(self.homeassistant_discovery_type, self.homeassistant_real_unique_id)
    )

  @abstractproperty
  def discovery_config(self) -> object:
    return {
      "name": "Unconfigured device",
    }

  def send_discovery(self) -> None:
    self.client.publish(
      self.homeassistant_discovery_topic,
      JSONEncoder().encode(self.discovery_config),
      retain=True)

  @abstractmethod
  def run(self) -> None:
    print("Module '{}' thread started".format(self.__class__.__name__))
