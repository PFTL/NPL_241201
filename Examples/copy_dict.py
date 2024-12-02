import copy
import yaml

with open('Examples/config.yml', 'r') as f:
    var1 = yaml.load(f, Loader=yaml.FullLoader)

print(var1)
var2 = copy.deepcopy(var1)

var1['Scan']['start'] = 2.5

print(var1)
print(var2)