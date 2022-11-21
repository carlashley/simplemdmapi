from .models.account import Account
from .models.apps import Apps, ManagedAppConfigs
from .models.assignment_groups import AssignmentGroups
from .models.custom_attributes import CustomAttributes
from .models.device_groups import DeviceGroups
from .models.devices import ManagedDevices
from .models.enrollments import Enrollments
from .models.installed_apps import InstalledApps
from .models.logs import Logs
from .models.profiles import CustomConfigProfiles, Profiles
from .models.servers import DEPServers, PushCertificates

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
