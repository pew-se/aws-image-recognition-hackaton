import json

json_path = 'response.json'

with open(json_path, 'rb') as text:
    textContent = text.read()

#print(textContent)

jsonData = json.loads(textContent)
#print(jsonData['Labels'])

labels = jsonData['Labels']

for item in labels:
    if len(item['Instances']) != 0:
        print(item)