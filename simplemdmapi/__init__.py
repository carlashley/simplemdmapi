from .account import Account
from .apps import Apps, ManagedAppConfigs
from .assignment_groups import AssignmentGroups
from .custom_attributes import CustomAttributes
from .device_groups import DeviceGroups
from .devices import ManagedDevices
from .enrollments import Enrollments
from .installed_apps import InstalledApps
from .logs import Logs
from .profiles import CustomConfigProfiles
from .servers import DEPServers, PushCertificates

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
profiles = CustomConfigProfiles()
dep_servers = DEPServers()
push_certifcatess = PushCertificates()
