# sonarr_api.ImportListApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_importlist_action_name_post**](ImportListApi.md#api_v3_importlist_action_name_post) | **POST** /api/v3/importlist/action/{name} | 
[**api_v3_importlist_bulk_delete**](ImportListApi.md#api_v3_importlist_bulk_delete) | **DELETE** /api/v3/importlist/bulk | 
[**api_v3_importlist_bulk_put**](ImportListApi.md#api_v3_importlist_bulk_put) | **PUT** /api/v3/importlist/bulk | 
[**api_v3_importlist_get**](ImportListApi.md#api_v3_importlist_get) | **GET** /api/v3/importlist | 
[**api_v3_importlist_id_delete**](ImportListApi.md#api_v3_importlist_id_delete) | **DELETE** /api/v3/importlist/{id} | 
[**api_v3_importlist_id_get**](ImportListApi.md#api_v3_importlist_id_get) | **GET** /api/v3/importlist/{id} | 
[**api_v3_importlist_id_put**](ImportListApi.md#api_v3_importlist_id_put) | **PUT** /api/v3/importlist/{id} | 
[**api_v3_importlist_post**](ImportListApi.md#api_v3_importlist_post) | **POST** /api/v3/importlist | 
[**api_v3_importlist_schema_get**](ImportListApi.md#api_v3_importlist_schema_get) | **GET** /api/v3/importlist/schema | 
[**api_v3_importlist_test_post**](ImportListApi.md#api_v3_importlist_test_post) | **POST** /api/v3/importlist/test | 
[**api_v3_importlist_testall_post**](ImportListApi.md#api_v3_importlist_testall_post) | **POST** /api/v3/importlist/testall | 


# **api_v3_importlist_action_name_post**
> api_v3_importlist_action_name_post(name, import_list_resource=import_list_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    name = 'name_example' # str | 
    import_list_resource = sonarr_api.ImportListResource() # ImportListResource |  (optional)

    try:
        api_instance.api_v3_importlist_action_name_post(name, import_list_resource=import_list_resource)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_action_name_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **import_list_resource** | [**ImportListResource**](ImportListResource.md)|  | [optional] 

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

# **api_v3_importlist_bulk_delete**
> api_v3_importlist_bulk_delete(import_list_bulk_resource=import_list_bulk_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_bulk_resource import ImportListBulkResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    import_list_bulk_resource = sonarr_api.ImportListBulkResource() # ImportListBulkResource |  (optional)

    try:
        api_instance.api_v3_importlist_bulk_delete(import_list_bulk_resource=import_list_bulk_resource)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_bulk_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **import_list_bulk_resource** | [**ImportListBulkResource**](ImportListBulkResource.md)|  | [optional] 

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

# **api_v3_importlist_bulk_put**
> ImportListResource api_v3_importlist_bulk_put(import_list_bulk_resource=import_list_bulk_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_bulk_resource import ImportListBulkResource
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    import_list_bulk_resource = sonarr_api.ImportListBulkResource() # ImportListBulkResource |  (optional)

    try:
        api_response = api_instance.api_v3_importlist_bulk_put(import_list_bulk_resource=import_list_bulk_resource)
        print("The response of ImportListApi->api_v3_importlist_bulk_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_bulk_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **import_list_bulk_resource** | [**ImportListBulkResource**](ImportListBulkResource.md)|  | [optional] 

### Return type

[**ImportListResource**](ImportListResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_importlist_get**
> List[ImportListResource] api_v3_importlist_get()

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)

    try:
        api_response = api_instance.api_v3_importlist_get()
        print("The response of ImportListApi->api_v3_importlist_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ImportListResource]**](ImportListResource.md)

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

# **api_v3_importlist_id_delete**
> api_v3_importlist_id_delete(id)

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
    api_instance = sonarr_api.ImportListApi(api_client)
    id = 56 # int | 

    try:
        api_instance.api_v3_importlist_id_delete(id)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

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

# **api_v3_importlist_id_get**
> ImportListResource api_v3_importlist_id_get(id)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    id = 56 # int | 

    try:
        api_response = api_instance.api_v3_importlist_id_get(id)
        print("The response of ImportListApi->api_v3_importlist_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**ImportListResource**](ImportListResource.md)

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

# **api_v3_importlist_id_put**
> ImportListResource api_v3_importlist_id_put(id, force_save=force_save, import_list_resource=import_list_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    id = 56 # int | 
    force_save = False # bool |  (optional) (default to False)
    import_list_resource = sonarr_api.ImportListResource() # ImportListResource |  (optional)

    try:
        api_response = api_instance.api_v3_importlist_id_put(id, force_save=force_save, import_list_resource=import_list_resource)
        print("The response of ImportListApi->api_v3_importlist_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **force_save** | **bool**|  | [optional] [default to False]
 **import_list_resource** | [**ImportListResource**](ImportListResource.md)|  | [optional] 

### Return type

[**ImportListResource**](ImportListResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_importlist_post**
> ImportListResource api_v3_importlist_post(force_save=force_save, import_list_resource=import_list_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    force_save = False # bool |  (optional) (default to False)
    import_list_resource = sonarr_api.ImportListResource() # ImportListResource |  (optional)

    try:
        api_response = api_instance.api_v3_importlist_post(force_save=force_save, import_list_resource=import_list_resource)
        print("The response of ImportListApi->api_v3_importlist_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **force_save** | **bool**|  | [optional] [default to False]
 **import_list_resource** | [**ImportListResource**](ImportListResource.md)|  | [optional] 

### Return type

[**ImportListResource**](ImportListResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_importlist_schema_get**
> List[ImportListResource] api_v3_importlist_schema_get()

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)

    try:
        api_response = api_instance.api_v3_importlist_schema_get()
        print("The response of ImportListApi->api_v3_importlist_schema_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_schema_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ImportListResource]**](ImportListResource.md)

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

# **api_v3_importlist_test_post**
> api_v3_importlist_test_post(force_test=force_test, import_list_resource=import_list_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.import_list_resource import ImportListResource
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
    api_instance = sonarr_api.ImportListApi(api_client)
    force_test = False # bool |  (optional) (default to False)
    import_list_resource = sonarr_api.ImportListResource() # ImportListResource |  (optional)

    try:
        api_instance.api_v3_importlist_test_post(force_test=force_test, import_list_resource=import_list_resource)
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_test_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **force_test** | **bool**|  | [optional] [default to False]
 **import_list_resource** | [**ImportListResource**](ImportListResource.md)|  | [optional] 

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

# **api_v3_importlist_testall_post**
> api_v3_importlist_testall_post()

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
    api_instance = sonarr_api.ImportListApi(api_client)

    try:
        api_instance.api_v3_importlist_testall_post()
    except Exception as e:
        print("Exception when calling ImportListApi->api_v3_importlist_testall_post: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

