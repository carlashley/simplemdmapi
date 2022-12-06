from .endpoints.account import Account
from .endpoints.apps import Apps, ManagedAppConfigs
from .endpoints.assignment_groups import AssignmentGroups
from .endpoints.custom_attributes import CustomAttributes
from .endpoints.device_groups import DeviceGroups
from .endpoints.devices import ManagedDevices
from .endpoints.enrollments import Enrollments
from .endpoints.installed_apps import InstalledApps
from .endpoints.logs import Logs
from .endpoints.profiles import CustomConfigProfiles, Profiles
from .endpoints.servers import DEPServers, PushCertificates

account = Account()
apps = Apps()
managed_app_configs = ManagedAppConfigs()
assignment_groups = AssignmentGroups()
custom_attributes = CustomAttributes()
device_groups = DeviceGroups()
devices = ManagedDevices()
enrollments = Enrollments()
installed_apps = InstalledApps()
logs = Logs()
custom_profiles = CustomConfigProfiles()
profiles = Profiles()
dep_servers = DEPServers()
push_certifcatess = PushCertificates()

VERSION = "0.0.20221202"
