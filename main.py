import json

import requests

# content = requests.get("http://172.30.1.75:8082/streaming-api/v2/api-docs")
content = requests.get("http://music.dev.nurtelecom.intech-global.com/streaming-api/v2/api-docs")
# content = requests.get("http://music.dev.nurtelecom.intech-global.com/v2/api-docs")
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
            temp = {
                'type': k,
                'path': key,
                'name': v['operationId']
            }
            if 'parameters' in v:
                parameters = read_parameters(v['parameters'])
                temp['parameters'] = parameters

            if name not in result:
                result[name] = []
            result[name].append(temp)
    return result


def print_annotation_path(req_type, req_path):
    print('@' + req_type.upper() + '("' + req_path + '")')


def print_request_name(req_name):
    index = req_name.find('Using')
    print('fun ' + req_name[:index])


def print_request_parameters(req_param_list):
    if 'parameters' in req_param_list:
        query = '('
        for params in req_param_list['parameters']:
            if params[0] == 'body':
                continue

            query += '@'
            query += params[0].title()

            name = params[1]
            name = name[0].lower() + name[1:]
            query += '("' + params[1] + '") ' + name + ': '

            need_capitalize = params[2] == 'string' or params[2] == 'boolean'
            if need_capitalize:
                query += params[2].title()
            elif params[2] == 'integer':
                query += 'Long'
            else:
                query += params[2]

            if not params[3]:
                query += '? = null'

            query += ',\n'

        query = query[:-2]
        query += ')'
        print(query)
    else:
        print('()')


def print_results(parsed_dict):
    for key, value in parsed_dict.items():
        print(key)
        print()
        for temp in value:
            print_annotation_path(temp['type'], temp['path'])
            print_request_name(temp['name'])
            print_request_parameters(temp)
            print()
        print()


bar = read_controllers()
print_results(bar)
