# simplemdmapi
A Python implementation of the SimpleMDM API inspired by the https://github.com/macadmins/simpleMDMpy implementation. This is a work in progress and while it can be used in production, do so under advisement that not _every_ API endpoint implementation has been tested thoroughly.

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

### Environment Values
- `SIMPLEMDM_CONNECT_TIMEOUT` number of seconds for connection timeout; defaults to `5`
- `SIMPLEMDM_READ_TIMEOUT` number of seconds for read timeout; defaults to `15`
- `SIMEMDM_MAX_RETRIES` maximum number of retries; defaults to `3`
- `SIMPLEMDM_RETRY_BACKOFF` number of backoff seconds between each retry (this exponentially increases each retry); defaults to `1`
- `SIMPLEMDM_RESULTS_PAGINATION` maxumum number of objects per "page" returned in a pagination request; defaults to `200`
- `SIMPLEMDM_SLEEP_WAIT` number of seconds (int or float representation) to sleep between each request (to avoid API rate limiting); defaults to `1.0`
- `SIMPLEMDM_TOKEN` actual token string for authentication or path to a plain text file containing the token string (on a single line); defaults to `/var/root/simplemdm_token`

### Basic Use
```
from simplemdmapi.endpoints import Apps, Devices

# To create an instance of the devices endpoint using the SIMPLEMDM_TOKEN environment variable:
d = Devices()
# Starred expression expands the generator object from a paginated method.
devices = [*d.list_all(include_awaiting_enrollment=True, search="Mike's iPhone")]

# Non paginated methods return the requests.Response object for custom processing/error handling.
new_device = mdm_devices.create(name="Joe's Mac", group_id=420)
print(new_device.status_code)

lost_mode_on = mdm_devices.enable_lost_mode(device_id=420)
lost_mode_off = mdm_devices.disable_lost_mode(device_id=420)


# You can specify a specific token string or token path if you don't want the token
# stored in an environment variable, or you simply need to override the environment
# variable with a different token.
d = Devices(tkn="R7cCCc4959877DBE6b6c63a8eb1bfe3bfb545fa8fe5AA8b1b2c13e4a7c1c0d1c4d4")

# A file path (the token must be in a plain text file on the first line).
# It is strongly recommended that this file path only be readable by the user/service
# account that this package is used by.
a = Apps(tkn="/Users/Shared/supersecret/simpletoken")
print(apps.retrieve("19347392").json())
```


### Paginated methods
Typically the `.list_all()` methods are paginated and will return a dictionary object, while most other methods will return the response object instead. This is done so that error handling can be customised within your own use cases.

These other methods are also paginated and will therefore return a dictionary object and not a response object:
| Endpoint  | Method |
| --- | ---- |
| `Apps` | `list_installs` |
| `Devices` | `list_applications` |
| `Devices` | `list_users` |
