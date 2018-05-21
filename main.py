import requests
import json


content = requests.get("http://172.30.1.75:8082/streaming-api/v2/api-docs")
# content = requests.get("http://music.dev.nurtelecom.intech-global.com/streaming-api/v2/api-docs")
swagger = json.loads(content.content.decode('utf-8'))


bar = {}
paths = swagger['paths']
for key, value in paths.items():
    for k, v in value.items():
        name = v['tags'][0]
        temp = [key, k, v['operationId']]
        if name not in bar:
            bar[name] = []
        bar[name].append(temp)

print(bar)
