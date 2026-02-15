# sonarr_api.EpisodeApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_episode_get**](EpisodeApi.md#api_v3_episode_get) | **GET** /api/v3/episode | 
[**api_v3_episode_id_get**](EpisodeApi.md#api_v3_episode_id_get) | **GET** /api/v3/episode/{id} | 
[**api_v3_episode_id_put**](EpisodeApi.md#api_v3_episode_id_put) | **PUT** /api/v3/episode/{id} | 
[**api_v3_episode_monitor_put**](EpisodeApi.md#api_v3_episode_monitor_put) | **PUT** /api/v3/episode/monitor | 


# **api_v3_episode_get**
> List[EpisodeResource] api_v3_episode_get(series_id=series_id, season_number=season_number, episode_ids=episode_ids, episode_file_id=episode_file_id, include_series=include_series, include_episode_file=include_episode_file, include_images=include_images)

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
    api_instance = sonarr_api.EpisodeApi(api_client)
    series_id = 56 # int |  (optional)
    season_number = 56 # int |  (optional)
    episode_ids = [56] # List[int] |  (optional)
    episode_file_id = 56 # int |  (optional)
    include_series = False # bool |  (optional) (default to False)
    include_episode_file = False # bool |  (optional) (default to False)
    include_images = False # bool |  (optional) (default to False)

    try:
        api_response = api_instance.api_v3_episode_get(series_id=series_id, season_number=season_number, episode_ids=episode_ids, episode_file_id=episode_file_id, include_series=include_series, include_episode_file=include_episode_file, include_images=include_images)
        print("The response of EpisodeApi->api_v3_episode_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EpisodeApi->api_v3_episode_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**|  | [optional] 
 **season_number** | **int**|  | [optional] 
 **episode_ids** | [**List[int]**](int.md)|  | [optional] 
 **episode_file_id** | **int**|  | [optional] 
 **include_series** | **bool**|  | [optional] [default to False]
 **include_episode_file** | **bool**|  | [optional] [default to False]
 **include_images** | **bool**|  | [optional] [default to False]

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

# **api_v3_episode_id_get**
> EpisodeResource api_v3_episode_id_get(id)

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
    api_instance = sonarr_api.EpisodeApi(api_client)
    id = 56 # int | 

    try:
        api_response = api_instance.api_v3_episode_id_get(id)
        print("The response of EpisodeApi->api_v3_episode_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EpisodeApi->api_v3_episode_id_get: %s\n" % e)
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

# **api_v3_episode_id_put**
> EpisodeResource api_v3_episode_id_put(id, episode_resource=episode_resource)

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
    api_instance = sonarr_api.EpisodeApi(api_client)
    id = 56 # int | 
    episode_resource = sonarr_api.EpisodeResource() # EpisodeResource |  (optional)

    try:
        api_response = api_instance.api_v3_episode_id_put(id, episode_resource=episode_resource)
        print("The response of EpisodeApi->api_v3_episode_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EpisodeApi->api_v3_episode_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **episode_resource** | [**EpisodeResource**](EpisodeResource.md)|  | [optional] 

### Return type

[**EpisodeResource**](EpisodeResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json, text/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_episode_monitor_put**
> api_v3_episode_monitor_put(include_images=include_images, episodes_monitored_resource=episodes_monitored_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.episodes_monitored_resource import EpisodesMonitoredResource
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
    api_instance = sonarr_api.EpisodeApi(api_client)
    include_images = False # bool |  (optional) (default to False)
    episodes_monitored_resource = sonarr_api.EpisodesMonitoredResource() # EpisodesMonitoredResource |  (optional)

    try:
        api_instance.api_v3_episode_monitor_put(include_images=include_images, episodes_monitored_resource=episodes_monitored_resource)
    except Exception as e:
        print("Exception when calling EpisodeApi->api_v3_episode_monitor_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **include_images** | **bool**|  | [optional] [default to False]
 **episodes_monitored_resource** | [**EpisodesMonitoredResource**](EpisodesMonitoredResource.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

