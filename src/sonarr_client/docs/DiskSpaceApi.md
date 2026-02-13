# sonarr_api.DiskSpaceApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_diskspace_get**](DiskSpaceApi.md#api_v3_diskspace_get) | **GET** /api/v3/diskspace | 


# **api_v3_diskspace_get**
> List[DiskSpaceResource] api_v3_diskspace_get()

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.disk_space_resource import DiskSpaceResource
from sonarr_api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8989
# See configuration.py for a list of all supported configuration parameters.
configuration = sonarr_api.Configuration(
    host = "http://localhost:8989"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apikey
configuration.api_key['apikey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apikey'] = 'Bearer'

# Configure API key authorization: X-Api-Key
configuration.api_key['X-Api-Key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Api-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with sonarr_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = sonarr_api.DiskSpaceApi(api_client)

    try:
        api_response = api_instance.api_v3_diskspace_get()
        print("The response of DiskSpaceApi->api_v3_diskspace_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DiskSpaceApi->api_v3_diskspace_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[DiskSpaceResource]**](DiskSpaceResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

