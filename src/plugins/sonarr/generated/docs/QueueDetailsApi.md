# sonarr_api.QueueDetailsApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_queue_details_get**](QueueDetailsApi.md#api_v3_queue_details_get) | **GET** /api/v3/queue/details | 


# **api_v3_queue_details_get**
> List[QueueResource] api_v3_queue_details_get(series_id=series_id, episode_ids=episode_ids, include_series=include_series, include_episode=include_episode)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.queue_resource import QueueResource
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
    api_instance = sonarr_api.QueueDetailsApi(api_client)
    series_id = 56 # int |  (optional)
    episode_ids = [56] # List[int] |  (optional)
    include_series = False # bool |  (optional) (default to False)
    include_episode = False # bool |  (optional) (default to False)

    try:
        api_response = api_instance.api_v3_queue_details_get(series_id=series_id, episode_ids=episode_ids, include_series=include_series, include_episode=include_episode)
        print("The response of QueueDetailsApi->api_v3_queue_details_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueueDetailsApi->api_v3_queue_details_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**|  | [optional] 
 **episode_ids** | [**List[int]**](int.md)|  | [optional] 
 **include_series** | **bool**|  | [optional] [default to False]
 **include_episode** | **bool**|  | [optional] [default to False]

### Return type

[**List[QueueResource]**](QueueResource.md)

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

