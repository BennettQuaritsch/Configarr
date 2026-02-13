# sonarr_api.QualityDefinitionApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_qualitydefinition_get**](QualityDefinitionApi.md#api_v3_qualitydefinition_get) | **GET** /api/v3/qualitydefinition | 
[**api_v3_qualitydefinition_id_get**](QualityDefinitionApi.md#api_v3_qualitydefinition_id_get) | **GET** /api/v3/qualitydefinition/{id} | 
[**api_v3_qualitydefinition_id_put**](QualityDefinitionApi.md#api_v3_qualitydefinition_id_put) | **PUT** /api/v3/qualitydefinition/{id} | 
[**api_v3_qualitydefinition_limits_get**](QualityDefinitionApi.md#api_v3_qualitydefinition_limits_get) | **GET** /api/v3/qualitydefinition/limits | 
[**api_v3_qualitydefinition_update_put**](QualityDefinitionApi.md#api_v3_qualitydefinition_update_put) | **PUT** /api/v3/qualitydefinition/update | 


# **api_v3_qualitydefinition_get**
> List[QualityDefinitionResource] api_v3_qualitydefinition_get()

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.quality_definition_resource import QualityDefinitionResource
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
    api_instance = sonarr_api.QualityDefinitionApi(api_client)

    try:
        api_response = api_instance.api_v3_qualitydefinition_get()
        print("The response of QualityDefinitionApi->api_v3_qualitydefinition_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QualityDefinitionApi->api_v3_qualitydefinition_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[QualityDefinitionResource]**](QualityDefinitionResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_qualitydefinition_id_get**
> QualityDefinitionResource api_v3_qualitydefinition_id_get(id)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.quality_definition_resource import QualityDefinitionResource
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
    api_instance = sonarr_api.QualityDefinitionApi(api_client)
    id = 56 # int | 

    try:
        api_response = api_instance.api_v3_qualitydefinition_id_get(id)
        print("The response of QualityDefinitionApi->api_v3_qualitydefinition_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QualityDefinitionApi->api_v3_qualitydefinition_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**QualityDefinitionResource**](QualityDefinitionResource.md)

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

# **api_v3_qualitydefinition_id_put**
> QualityDefinitionResource api_v3_qualitydefinition_id_put(id, quality_definition_resource=quality_definition_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.quality_definition_resource import QualityDefinitionResource
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
    api_instance = sonarr_api.QualityDefinitionApi(api_client)
    id = 'id_example' # str | 
    quality_definition_resource = sonarr_api.QualityDefinitionResource() # QualityDefinitionResource |  (optional)

    try:
        api_response = api_instance.api_v3_qualitydefinition_id_put(id, quality_definition_resource=quality_definition_resource)
        print("The response of QualityDefinitionApi->api_v3_qualitydefinition_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QualityDefinitionApi->api_v3_qualitydefinition_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **quality_definition_resource** | [**QualityDefinitionResource**](QualityDefinitionResource.md)|  | [optional] 

### Return type

[**QualityDefinitionResource**](QualityDefinitionResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: application/json, text/json, application/*+json
 - **Accept**: text/plain, application/json, text/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_qualitydefinition_limits_get**
> QualityDefinitionLimitsResource api_v3_qualitydefinition_limits_get()

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.quality_definition_limits_resource import QualityDefinitionLimitsResource
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
    api_instance = sonarr_api.QualityDefinitionApi(api_client)

    try:
        api_response = api_instance.api_v3_qualitydefinition_limits_get()
        print("The response of QualityDefinitionApi->api_v3_qualitydefinition_limits_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling QualityDefinitionApi->api_v3_qualitydefinition_limits_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**QualityDefinitionLimitsResource**](QualityDefinitionLimitsResource.md)

### Authorization

[apikey](../README.md#apikey), [X-Api-Key](../README.md#X-Api-Key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v3_qualitydefinition_update_put**
> api_v3_qualitydefinition_update_put(quality_definition_resource=quality_definition_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.quality_definition_resource import QualityDefinitionResource
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
    api_instance = sonarr_api.QualityDefinitionApi(api_client)
    quality_definition_resource = [sonarr_api.QualityDefinitionResource()] # List[QualityDefinitionResource] |  (optional)

    try:
        api_instance.api_v3_qualitydefinition_update_put(quality_definition_resource=quality_definition_resource)
    except Exception as e:
        print("Exception when calling QualityDefinitionApi->api_v3_qualitydefinition_update_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quality_definition_resource** | [**List[QualityDefinitionResource]**](QualityDefinitionResource.md)|  | [optional] 

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

