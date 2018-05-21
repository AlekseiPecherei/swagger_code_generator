import requests
import json

# content = requests.get("http://172.30.1.75:8082/streaming-api/v2/api-docs")
content = requests.get("http://music.dev.nurtelecom.intech-global.com/streaming-api/v2/api-docs")
swagger = json.loads(content.content.decode('utf-8'))


def read_parameters(field):
    temp = []
    for f in field:
        temp.append([
            f.get('in'),
            f.get('name'),
            f.get('type'),
            f.get('required')
        ])
    return temp


def read_controllers():
    result = {}
    paths = swagger['paths']
    for key, value in paths.items():
        for k, v in value.items():
            name = v['tags'][0]

            if 'parameters' in v:
                parameters = read_parameters(v['parameters'])
                temp = [k, key, v['operationId'], parameters]
            else:
                temp = [k, key, v['operationId']]

            if name not in result:
                result[name] = []
            result[name].append(temp)
    return result


def print_results(parsed_dict):
    for key, value in parsed_dict.items():
        print(key)
        for temp in value:
            print(temp[0], temp[1], ' ')
            if temp[2] in temp:
                print(temp[2])
                # print()
            if len(temp) == 4:
                for temp_2 in temp[3]:
                    print(temp_2)
                print()
        print()


bar = read_controllers()
print_results(bar)
# print(bar)
