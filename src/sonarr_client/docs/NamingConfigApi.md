# sonarr_api.NamingConfigApi

All URIs are relative to *http://localhost:8989*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v3_config_naming_examples_get**](NamingConfigApi.md#api_v3_config_naming_examples_get) | **GET** /api/v3/config/naming/examples | 
[**api_v3_config_naming_get**](NamingConfigApi.md#api_v3_config_naming_get) | **GET** /api/v3/config/naming | 
[**api_v3_config_naming_id_get**](NamingConfigApi.md#api_v3_config_naming_id_get) | **GET** /api/v3/config/naming/{id} | 
[**api_v3_config_naming_id_put**](NamingConfigApi.md#api_v3_config_naming_id_put) | **PUT** /api/v3/config/naming/{id} | 


# **api_v3_config_naming_examples_get**
> api_v3_config_naming_examples_get(rename_episodes=rename_episodes, replace_illegal_characters=replace_illegal_characters, colon_replacement_format=colon_replacement_format, custom_colon_replacement_format=custom_colon_replacement_format, multi_episode_style=multi_episode_style, standard_episode_format=standard_episode_format, daily_episode_format=daily_episode_format, anime_episode_format=anime_episode_format, series_folder_format=series_folder_format, season_folder_format=season_folder_format, specials_folder_format=specials_folder_format, id=id, resource_name=resource_name)

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
    api_instance = sonarr_api.NamingConfigApi(api_client)
    rename_episodes = True # bool |  (optional)
    replace_illegal_characters = True # bool |  (optional)
    colon_replacement_format = 56 # int |  (optional)
    custom_colon_replacement_format = 'custom_colon_replacement_format_example' # str |  (optional)
    multi_episode_style = 56 # int |  (optional)
    standard_episode_format = 'standard_episode_format_example' # str |  (optional)
    daily_episode_format = 'daily_episode_format_example' # str |  (optional)
    anime_episode_format = 'anime_episode_format_example' # str |  (optional)
    series_folder_format = 'series_folder_format_example' # str |  (optional)
    season_folder_format = 'season_folder_format_example' # str |  (optional)
    specials_folder_format = 'specials_folder_format_example' # str |  (optional)
    id = 56 # int |  (optional)
    resource_name = 'resource_name_example' # str |  (optional)

    try:
        api_instance.api_v3_config_naming_examples_get(rename_episodes=rename_episodes, replace_illegal_characters=replace_illegal_characters, colon_replacement_format=colon_replacement_format, custom_colon_replacement_format=custom_colon_replacement_format, multi_episode_style=multi_episode_style, standard_episode_format=standard_episode_format, daily_episode_format=daily_episode_format, anime_episode_format=anime_episode_format, series_folder_format=series_folder_format, season_folder_format=season_folder_format, specials_folder_format=specials_folder_format, id=id, resource_name=resource_name)
    except Exception as e:
        print("Exception when calling NamingConfigApi->api_v3_config_naming_examples_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rename_episodes** | **bool**|  | [optional] 
 **replace_illegal_characters** | **bool**|  | [optional] 
 **colon_replacement_format** | **int**|  | [optional] 
 **custom_colon_replacement_format** | **str**|  | [optional] 
 **multi_episode_style** | **int**|  | [optional] 
 **standard_episode_format** | **str**|  | [optional] 
 **daily_episode_format** | **str**|  | [optional] 
 **anime_episode_format** | **str**|  | [optional] 
 **series_folder_format** | **str**|  | [optional] 
 **season_folder_format** | **str**|  | [optional] 
 **specials_folder_format** | **str**|  | [optional] 
 **id** | **int**|  | [optional] 
 **resource_name** | **str**|  | [optional] 

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

# **api_v3_config_naming_get**
> NamingConfigResource api_v3_config_naming_get()

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.naming_config_resource import NamingConfigResource
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
    api_instance = sonarr_api.NamingConfigApi(api_client)

    try:
        api_response = api_instance.api_v3_config_naming_get()
        print("The response of NamingConfigApi->api_v3_config_naming_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NamingConfigApi->api_v3_config_naming_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**NamingConfigResource**](NamingConfigResource.md)

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

# **api_v3_config_naming_id_get**
> NamingConfigResource api_v3_config_naming_id_get(id)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.naming_config_resource import NamingConfigResource
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
    api_instance = sonarr_api.NamingConfigApi(api_client)
    id = 56 # int | 

    try:
        api_response = api_instance.api_v3_config_naming_id_get(id)
        print("The response of NamingConfigApi->api_v3_config_naming_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NamingConfigApi->api_v3_config_naming_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**NamingConfigResource**](NamingConfigResource.md)

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

# **api_v3_config_naming_id_put**
> NamingConfigResource api_v3_config_naming_id_put(id, naming_config_resource=naming_config_resource)

### Example

* Api Key Authentication (apikey):
* Api Key Authentication (X-Api-Key):

```python
import sonarr_api
from sonarr_api.models.naming_config_resource import NamingConfigResource
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
    api_instance = sonarr_api.NamingConfigApi(api_client)
    id = 'id_example' # str | 
    naming_config_resource = sonarr_api.NamingConfigResource() # NamingConfigResource |  (optional)

    try:
        api_response = api_instance.api_v3_config_naming_id_put(id, naming_config_resource=naming_config_resource)
        print("The response of NamingConfigApi->api_v3_config_naming_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NamingConfigApi->api_v3_config_naming_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **naming_config_resource** | [**NamingConfigResource**](NamingConfigResource.md)|  | [optional] 

### Return type

[**NamingConfigResource**](NamingConfigResource.md)

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

