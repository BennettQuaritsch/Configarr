# ModelField


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**unit** | **str** |  | [optional] 
**help_text** | **str** |  | [optional] 
**help_text_warning** | **str** |  | [optional] 
**help_link** | **str** |  | [optional] 
**value** | **object** |  | [optional] 
**type** | **str** |  | [optional] 
**advanced** | **bool** |  | [optional] 
**select_options** | [**List[SelectOption]**](SelectOption.md) |  | [optional] 
**select_options_provider_action** | **str** |  | [optional] 
**section** | **str** |  | [optional] 
**hidden** | **str** |  | [optional] 
**privacy** | [**PrivacyLevel**](PrivacyLevel.md) |  | [optional] 
**placeholder** | **str** |  | [optional] 
**is_float** | **bool** |  | [optional] 

## Example

```python
from sonarr_api.models.model_field import ModelField

# TODO update the JSON string below
json = "{}"
# create an instance of ModelField from a JSON string
model_field_instance = ModelField.from_json(json)
# print the JSON string representation of the object
print(ModelField.to_json())

# convert the object into a dict
model_field_dict = model_field_instance.to_dict()
# create an instance of ModelField from a dict
model_field_from_dict = ModelField.from_dict(model_field_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


