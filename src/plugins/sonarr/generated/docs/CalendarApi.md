# sonarr_api.CalendarApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_calendar_get**](CalendarApi.md#api_v3_calendar_get) | **GET** /api/v3/calendar | 
[**api_v3_calendar_id_get**](CalendarApi.md#api_v3_calendar_id_get) | **GET** /api/v3/calendar/{id} | 


# **api_v3_calendar_get**
> List[EpisodeResource] api_v3_calendar_get(start=start, end=end, unmonitored=unmonitored, include_series=include_series, include_episode_file=include_episode_file, include_episode_images=include_episode_images, tags=tags)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.episode_resource import EpisodeResource
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
    api_instance = sonarr_api.CalendarApi(api_client)
    start = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    end = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    unmonitored = False # bool |  (optional) (default to False)
    include_series = False # bool |  (optional) (default to False)
    include_episode_file = False # bool |  (optional) (default to False)
    include_episode_images = False # bool |  (optional) (default to False)
    tags = '' # str |  (optional) (default to '')

    try:
        api_response = api_instance.api_v3_calendar_get(start=start, end=end, unmonitored=unmonitored, include_series=include_series, include_episode_file=include_episode_file, include_episode_images=include_episode_images, tags=tags)
        print("The response of CalendarApi->api_v3_calendar_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CalendarApi->api_v3_calendar_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start** | **datetime**|  | [optional] 
 **end** | **datetime**|  | [optional] 
 **unmonitored** | **bool**|  | [optional] [default to False]
 **include_series** | **bool**|  | [optional] [default to False]
 **include_episode_file** | **bool**|  | [optional] [default to False]
 **include_episode_images** | **bool**|  | [optional] [default to False]
 **tags** | **str**|  | [optional] [default to &#39;&#39;]

### Return type

[**List[EpisodeResource]**](EpisodeResource.md)

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

# **api_v3_calendar_id_get**
> EpisodeResource api_v3_calendar_id_get(id)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.episode_resource import EpisodeResource
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
    api_instance = sonarr_api.CalendarApi(api_client)
    id = 56 # int | 

    try:
        api_response = api_instance.api_v3_calendar_id_get(id)
        print("The response of CalendarApi->api_v3_calendar_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CalendarApi->api_v3_calendar_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**EpisodeResource**](EpisodeResource.md)

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

