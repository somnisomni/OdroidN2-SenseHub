import const
from modules.base.module import Module

class MemoryInfo:
  __discovery_config_common = {
    "device_class": "data_size",
    "unit_of_measurement": "MiB",
    "entity_category": "diagnostic",
    "state_class": "measurement",
    "expire_after": 20
  }

  def __init__(self, caller_module: Module):
    self.DISCOVERY_TOPIC_TOTAL = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_memory_total")
    self.DISCOVERY_CONFIG_TOTAL = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_TOTAL.update({
        "name": "{} System Memory Total".format(const.DEVICE_NAME),
        "unique_id": caller_module.homeassistant_real_unique_id + "_memory_total",
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ value_json.memory.total }}",
    })

    self.DISCOVERY_TOPIC_AVAILABLE = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_memory_available")
    self.DISCOVERY_CONFIG_AVAILABLE = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_AVAILABLE.update({
        "name": "{} System Memory Available".format(const.DEVICE_NAME),
        "unique_id": caller_module.homeassistant_real_unique_id + "_memory_available",
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ value_json.memory.available }}",
    })

    self.DISCOVERY_TOPIC_USED = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_memory_used")
    self.DISCOVERY_CONFIG_USED = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_USED.update({
        "name": "{} System Memory Used".format(const.DEVICE_NAME),
        "unique_id": caller_module.homeassistant_real_unique_id + "_memory_used",
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ value_json.memory.used }}",
    })

    self.DISCOVERY_TOPIC_SWAP_TOTAL = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_memory_swap_total")
    self.DISCOVERY_CONFIG_SWAP_TOTAL = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_SWAP_TOTAL.update({
        "name": "{} System Swap Memory Total".format(const.DEVICE_NAME),
        "unique_id": caller_module.homeassistant_real_unique_id + "_memory_swap_total",
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ value_json.memory.swap_total }}",
    })

    self.DISCOVERY_TOPIC_SWAP_FREE = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_memory_swap_free")
    self.DISCOVERY_CONFIG_SWAP_FREE = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_SWAP_FREE.update({
        "name": "{} System Swap Memory Free".format(const.DEVICE_NAME),
        "unique_id": caller_module.homeassistant_real_unique_id + "_memory_swap_free",
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ value_json.memory.swap_free }}",
    })

    self.DISCOVERY_TOPIC_SWAP_USED = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_memory_swap_used")
    self.DISCOVERY_CONFIG_SWAP_USED = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_SWAP_USED.update({
        "name": "{} System Swap Memory Used".format(const.DEVICE_NAME),
        "unique_id": caller_module.homeassistant_real_unique_id + "_memory_swap_used",
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ value_json.memory.swap_used }}",
    })

  def get_values(self) -> dict:
    output = {
      "total": -1,
      "available": -1,
      "used": -1,
      "swap_total": -1,
      "swap_free": -1,
      "swap_used": -1
    }

    try:
      meminfo = []

      with open("/proc/meminfo", "r") as meminfoCall:
        meminfo = meminfoCall.readlines()

      for line in meminfo:
        if line.startswith("MemTotal"):
          output["total"] = round(int(line.split()[1]) / 1024, 2)
        elif line.startswith("MemAvailable"):
          output["available"] = round(int(line.split()[1]) / 1024, 2)
        elif line.startswith("SwapTotal"):
          output["swap_total"] = round(int(line.split()[1]) / 1024, 2)
        elif line.startswith("SwapFree"):
          output["swap_free"] = round(int(line.split()[1]) / 1024, 2)
    except:
      print("Failed to get memory info from '/proc/meminfo'!")

    output["used"] = output["total"] - output["available"]
    output["swap_used"] = output["swap_total"] - output["swap_free"]

    return { "memory": output }
