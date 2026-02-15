# sonarr_api.QueueApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_queue_bulk_delete**](QueueApi.md#api_v3_queue_bulk_delete) | **DELETE** /api/v3/queue/bulk | 
[**api_v3_queue_get**](QueueApi.md#api_v3_queue_get) | **GET** /api/v3/queue | 
[**api_v3_queue_id_delete**](QueueApi.md#api_v3_queue_id_delete) | **DELETE** /api/v3/queue/{id} | 


# **api_v3_queue_bulk_delete**
> api_v3_queue_bulk_delete(remove_from_client=remove_from_client, blocklist=blocklist, skip_redownload=skip_redownload, change_category=change_category, queue_bulk_resource=queue_bulk_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.queue_bulk_resource import QueueBulkResource
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
    api_instance = sonarr_api.QueueApi(api_client)
    remove_from_client = True # bool |  (optional) (default to True)
    blocklist = False # bool |  (optional) (default to False)
    skip_redownload = False # bool |  (optional) (default to False)
    change_category = False # bool |  (optional) (default to False)
    queue_bulk_resource = sonarr_api.QueueBulkResource() # QueueBulkResource |  (optional)

    try:
        api_instance.api_v3_queue_bulk_delete(remove_from_client=remove_from_client, blocklist=blocklist, skip_redownload=skip_redownload, change_category=change_category, queue_bulk_resource=queue_bulk_resource)
    except Exception as e:
        print("Exception when calling QueueApi->api_v3_queue_bulk_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **remove_from_client** | **bool**|  | [optional] [default to True]
 **blocklist** | **bool**|  | [optional] [default to False]
 **skip_redownload** | **bool**|  | [optional] [default to False]
 **change_category** | **bool**|  | [optional] [default to False]
 **queue_bulk_resource** | [**QueueBulkResource**](QueueBulkResource.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_queue_get**
> QueueResourcePagingResource api_v3_queue_get(page=page, page_size=page_size, sort_key=sort_key, sort_direction=sort_direction, include_unknown_series_items=include_unknown_series_items, include_series=include_series, include_episode=include_episode, series_ids=series_ids, protocol=protocol, languages=languages, quality=quality, status=status)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.download_protocol import DownloadProtocol
from sonarr_api.models.queue_resource_paging_resource import QueueResourcePagingResource
from sonarr_api.models.queue_status import QueueStatus
from sonarr_api.models.sort_direction import SortDirection
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
    api_instance = sonarr_api.QueueApi(api_client)
    page = 1 # int |  (optional) (default to 1)
    page_size = 10 # int |  (optional) (default to 10)
    sort_key = 'sort_key_example' # str |  (optional)
    sort_direction = sonarr_api.SortDirection() # SortDirection |  (optional)
    include_unknown_series_items = False # bool |  (optional) (default to False)
    include_series = False # bool |  (optional) (default to False)
    include_episode = False # bool |  (optional) (default to False)
    series_ids = [56] # List[int] |  (optional)
    protocol = sonarr_api.DownloadProtocol() # DownloadProtocol |  (optional)
    languages = [56] # List[int] |  (optional)
    quality = [56] # List[int] |  (optional)
    status = [sonarr_api.QueueStatus()] # List[QueueStatus] |  (optional)

    try:
        api_response = api_instance.api_v3_queue_get(page=page, page_size=page_size, sort_key=sort_key, sort_direction=sort_direction, include_unknown_series_items=include_unknown_series_items, include_series=include_series, include_episode=include_episode, series_ids=series_ids, protocol=protocol, languages=languages, quality=quality, status=status)
        print("The response of QueueApi->api_v3_queue_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QueueApi->api_v3_queue_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**|  | [optional] [default to 1]
 **page_size** | **int**|  | [optional] [default to 10]
 **sort_key** | **str**|  | [optional] 
 **sort_direction** | [**SortDirection**](.md)|  | [optional] 
 **include_unknown_series_items** | **bool**|  | [optional] [default to False]
 **include_series** | **bool**|  | [optional] [default to False]
 **include_episode** | **bool**|  | [optional] [default to False]
 **series_ids** | [**List[int]**](int.md)|  | [optional] 
 **protocol** | [**DownloadProtocol**](.md)|  | [optional] 
 **languages** | [**List[int]**](int.md)|  | [optional] 
 **quality** | [**List[int]**](int.md)|  | [optional] 
 **status** | [**List[QueueStatus]**](QueueStatus.md)|  | [optional] 

### Return type

[**QueueResourcePagingResource**](QueueResourcePagingResource.md)

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

# **api_v3_queue_id_delete**
> api_v3_queue_id_delete(id, remove_from_client=remove_from_client, blocklist=blocklist, skip_redownload=skip_redownload, change_category=change_category)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
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
    api_instance = sonarr_api.QueueApi(api_client)
    id = 56 # int | 
    remove_from_client = True # bool |  (optional) (default to True)
    blocklist = False # bool |  (optional) (default to False)
    skip_redownload = False # bool |  (optional) (default to False)
    change_category = False # bool |  (optional) (default to False)

    try:
        api_instance.api_v3_queue_id_delete(id, remove_from_client=remove_from_client, blocklist=blocklist, skip_redownload=skip_redownload, change_category=change_category)
    except Exception as e:
        print("Exception when calling QueueApi->api_v3_queue_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **remove_from_client** | **bool**|  | [optional] [default to True]
 **blocklist** | **bool**|  | [optional] [default to False]
 **skip_redownload** | **bool**|  | [optional] [default to False]
 **change_category** | **bool**|  | [optional] [default to False]

### Return type

void (empty response body)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

