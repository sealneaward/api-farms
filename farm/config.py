from farm._config_section import ConfigSection
from farm.constant import local_dir
REAL_PATH = local_dir

logs = ConfigSection("logs")
logs.dir = "%s/%s" % (REAL_PATH, "logs")

config = ConfigSection("config")
config.dir = "%s/%s" % (REAL_PATH, "config")
