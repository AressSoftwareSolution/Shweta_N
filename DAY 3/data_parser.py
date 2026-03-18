import json

data={"name":"arya","id":123}

## Convert python into json
## serialization
json_data=json.dumps(data)
print(json_data)
## deserialization
parsed=json.loads(json_data)
print(parsed)

import xml.etree.ElementTree as etm

xml_data='''
<person>
    <name>John</name>
    <age>25</age>
</person>
'''

root= etm.fromstring(xml_data)
print(root.find("name").text)


import yaml
## python into yaml
yaml_data=yaml.dump(data)
print(yaml_data)
parsed_yaml=yaml.safe_load(yaml_data)
print(parsed_yaml)


import pickle
## python to pickle 
# Serialize
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Deserialize
with open("data.pkl", "rb") as f:
    loaded = pickle.load(f)
print(loaded)



## convertion 
## yaml to json


## convertion 
## yaml to json

parsed = yaml.safe_load(yaml_data) 
json_str = json.dumps(parsed)
print(json_str)

##json to yaml

parsed= json.loads(json_data)
yaml_str=yaml.dump(parsed)
print(yaml_str)