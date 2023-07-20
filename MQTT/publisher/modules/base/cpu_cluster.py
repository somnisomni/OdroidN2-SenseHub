import const
from modules.base.module import Module

class CPUClusterSysfileInfo:
  def __init__(self, policy_num: int):
    self.curfreq_sysfile = "/sys/devices/system/cpu/cpufreq/policy{}/scaling_cur_freq".format(policy_num)
    self.minfreq_sysfile = "/sys/devices/system/cpu/cpufreq/policy{}/scaling_min_freq".format(policy_num)
    self.maxfreq_sysfile = "/sys/devices/system/cpu/cpufreq/policy{}/scaling_max_freq".format(policy_num)

class CPUCluster:
  __discovery_config_common = {
    "device_class": "frequency",
    "unit_of_measurement": "MHz",
    "entity_category": "diagnostic",
    "state_class": "measurement",
    "expire_after": 20
  }

  def __init__(self, caller_module: Module, policy_num: int):
    self.CLUSTER_NUM = policy_num
    self.SYSFILE_INFO = CPUClusterSysfileInfo(policy_num)

    self.DISCOVERY_TOPIC_CUR = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_cpufreq{}_current".format(policy_num))
    self.DISCOVERY_CONFIG_CUR = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_CUR.update({
        "name": "{} System CPU Cluster #{} Current Frequency".format(const.DEVICE_NAME, policy_num),
        "unique_id": caller_module.homeassistant_real_unique_id + "_cpufreq{}_current".format(policy_num),
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ " + "value_json.cpufreq{}.current".format(policy_num) + " }}",
    })

    self.DISCOVERY_TOPIC_MAX = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_cpufreq{}_max".format(policy_num))
    self.DISCOVERY_CONFIG_MAX = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_MAX.update({
        "name": "{} System CPU Cluster #{} Max Frequency".format(const.DEVICE_NAME, policy_num),
        "unique_id": caller_module.homeassistant_real_unique_id + "_cpufreq{}_max".format(policy_num),
        "state_topic": caller_module.get_real_topic("system/state"),
        "value_template": "{{ " + "value_json.cpufreq{}.max".format(policy_num) + " }}",
    })

    self.DISCOVERY_TOPIC_MIN = caller_module.homeassistant_discovery_topic.replace(caller_module.homeassistant_unique_id, "system_cpufreq{}_min".format(policy_num))
    self.DISCOVERY_CONFIG_MIN = dict(self.__discovery_config_common)
    self.DISCOVERY_CONFIG_MIN.update({
        "name": "{} System CPU Cluster #{} Min Frequency".format(const.DEVICE_NAME, policy_num),
        "state_topic": caller_module.get_real_topic("system/state"),
        "unique_id": caller_module.homeassistant_real_unique_id + "_cpufreq{}_min".format(policy_num),
        "value_template": "{{ " + "value_json.cpufreq{}.min".format(policy_num) + " }}",
    })

  def get_values(self) -> dict:
    key = "cpufreq{}".format(self.CLUSTER_NUM)
    output = {}
    output[key] = {}

    try:
      with open(self.SYSFILE_INFO.curfreq_sysfile, "r") as curFreqCall:
        output[key]["current"] = int(curFreqCall.read().strip()) // 1000
    except:
      print("Failed to get current CPU frequency for cluster #{}!".format(self.CLUSTER_NUM))

    try:
      with open(self.SYSFILE_INFO.maxfreq_sysfile, "r") as maxFreqCall:
        output[key]["max"] = int(maxFreqCall.read().strip()) // 1000
    except:
      print("Failed to get max CPU frequency for cluster #{}!".format(self.CLUSTER_NUM))

    try:
      with open(self.SYSFILE_INFO.minfreq_sysfile, "r") as minFreqCall:
        output[key]["min"] = int(minFreqCall.read().strip()) // 1000
    except:
      print("Failed to get min CPU frequency for cluster #{}!".format(self.CLUSTER_NUM))

    return output
