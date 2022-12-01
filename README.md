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
Each API method implemented has the ability to pass an expanded dictionary as keyword args (AKA [kwargs](https://realpython.com/python-kwargs-and-args/)), while some specific API methods have arguments that are optional or required (or a combination of).

Keyword arguments passed in to an API method in this package are treated as arguments to pass on to the underlying `requests` calls; this is useful for overriding the global session settings such as timeouts for individual API calls, or if you have different authentication/header needs for specific API calls.

An example using the `devices` endpoint:
```
>>> from pprint import pprint
>>> from simplemdmapi import devices
>>>
>>> # An example to list all devices (this method paginates the devices endpoint and returns a reconstructed
>>> # dictionary representing the objects returned).
>>> pprint(devices.list_all())
{'data': [{'attributes': {[redacted]}],
 'has_more': False}
>>>
>>> # An example to search all the devices for a specific serial number using the optional 'search' argument.
>>> pprint(devices.list_all(search="[serial]"))
{'data': [{'attributes': {[redacted]}],
 'has_more': False}
>>>
>>> # An example to search all the devices for a specific serial number using the optional 'search' argument
>>> # and include secret custom attributes.
>>> pprint(devices.list_all(search="C07DD03ZPJH7", include_secret_custom_attributes=True))
{'data': [{'attributes': {[redacted]}],
 'has_more': False}
>>>
>>> # An example to search all the devices for a specific serial number using the optional 'search' argument
>>> # and include secret custom attributes that also passes on an expanded dictionary as keyword arguments
>>> # that are used to override various `requests.session` parameters.
>>> pprint(devices.list_all(search="C07DD03ZPJH7", include_secret_custom_attributes=True, **{"timeout": (1, 100)})
{'data': [{'attributes': {[redacted]}],
 'has_more': False}
>>>
>>> # An example of restarting a specific device.
>>> devices.restart(device_id="420")
<Response [202]>
```
