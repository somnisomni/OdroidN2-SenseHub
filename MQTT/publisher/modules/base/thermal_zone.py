import const
from modules.base.module import Module

class ThermalZoneSysfileInfo:
  def __init__(self, zone_num: int):
    self.temp_sysfile = "/sys/class/thermal/thermal_zone{}/temp".format(zone_num)
    self.type_sysfile = "/sys/class/thermal/thermal_zone{}/type".format(zone_num)

class ThermalZone:
  __discovery_config_common = {
    "device_class": "temperature",
    "unit_of_measurement": "°C",
    "entity_category": "diagnostic",
    "state_class": "measurement",
    "expire_after": 20
  }

  def __init__(self, caller_module: Module, zone_num: int, zone_name: str = None):
    self.ZONE_NUM = zone_num
    self.SYSFILE_INFO = ThermalZoneSysfileInfo(zone_num)

    self.DISCOVERY_TOPIC = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_thermalzone{}".format(zone_num))
    self.DISCOVERY_CONFIG = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG.update({
        "name": "{} System {}".format(const.DEVICE_NAME, zone_name if zone_name else "Thermal Zone #{}".format(zone_num)),
        "unique_id": caller_module.homeassistant_real_unique_id + "_thermalzone{}".format(zone_num),
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ " + "value_json.thermalzone{}".format(zone_num) + " }}",
    })

  def get_values(self) -> dict:
    key = "thermalzone{}".format(self.ZONE_NUM)
    output = {}
    output[key] = {}

    try:
      with open(self.SYSFILE_INFO.temp_sysfile, "r") as tempCall:
        output[key] = int(tempCall.read().strip()) / 1000
    except:
      print("Failed to get temperature for thermal zone #{}!".format(self.ZONE_NUM))

    return output
