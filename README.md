# simplemdmapi
A Python implementation of the SimpleMDM API. This is a work in progress and is not meant for production use at this time.

# Requires
### Python:
Tested on Python 3.10.4, but should only require Python 3.9+

### Packages:
Requires the `requests` package, >= v2.27.1.


# Usage
Clone the repo and copy the `simplemdmpy` folder to your relevant Python packages folder.
Set an environment variable `SIMPLETOKEN` to the file path of a plain text file where the token
is the first line of the file (alternatively the token can be set as the value of the environment
variable, but this is not recommended).

### Proxies
If you have special proxy settings that need to be passed in to `requests`, simpley create a file
named `proxies.py` and create a variable `proxy_settings` with a dictionary containing the key value pairs of
the proxy settings required.
For example:
```
proxy_settings = {"http": "http://example.org",
                  "https": "https://example.org}
```
This `proxies.py` file is not version controlled, so will not cause problems with git updates.

### Package use
```
from simplemdmapi import (account,
                          apps,
                          managed_app_configs,
                          assignment_groups,
                          custom_attributes,
                          device_groups,
                          devices,
                          enrollments,
                          installed_apps,
                          logs,
                          profiles,
                          dep_servers,
                          push_certifcatess)
from pprint import pformat

# Example of printing all device objects.
print(pformat(devices.list_all()))

# Example of uploading an app binary using the 'apps' API endpoint.
apps.create(params={"name": "macOS Big Sur 11.6.6"},
            files={"binary": "/tmp/macOS_BigSurInstaller.pkg"})

# Example of updating an app binary using the 'apps' API endpoint and
# overriding the default timeout value that the underlying 'requests'
# method uses.
apps.update(params={"name": "macOS Big Sur 11.6.6"},
           files={"binary": "/tmp/macOS_BigSurInstaller.pkg"},
           **{"timeout": (5, 60)})
```

Each API call has a `params` argument and a `**kwargs` argument (with several API call's that upload files having an additional `files` argument).

The `params` argument are the parameters to be passed into the API per the SimpleMDM API documentation, while the `**kwargs` argument can simply be
a dictionary of arguments to pass on to the underlying `requests` call. An example of this would be overriding the default timeout value.

There are also several API calls that take file uploads. This is handled by the `files` argument which is a dictionary containing a key that corresponds to the required key for the API (for example, `binary`, `mobileconfig`, or `file`), with the corresponding value for that key being the file path.
This `files` dictionary is then passed on to the underlying `requests` call and handled appropriately for uploading.
