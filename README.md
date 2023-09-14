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

### Use
```
from simplemdmap.endpoints.devices import Devices


mdm_devices = Devices()


enrolled_devices = [*mdm_devices.list_all(include_awaiting_enrollment=True, search="Mike's iPhone")]


new_device = mdm_devices.create(name="Joe's Mac", group_id=420)
print(new_device.status_code)
```
