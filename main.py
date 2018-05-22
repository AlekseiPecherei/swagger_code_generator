import json

import requests

# content = requests.get("http://172.30.1.75:8082/streaming-api/v2/api-docs")
content = requests.get("http://music.dev.nurtelecom.intech-global.com/streaming-api/v2/api-docs")
# content = requests.get("http://music.dev.nurtelecom.intech-global.com/v2/api-docs")
swagger = json.loads(content.content.decode('utf-8'))


def read_parameters(field):
    temp = []
    for f in field:
        temp.append({
            'in': f.get('in'),
            'name': f.get('name'),
            'type': f.get('type'),
            'required': f.get('required')
        })
    return temp


def parse_req_data(req_type, path, req_data):
    parsed = {
        'type': req_type,
        'path': path,
        'name': req_data['operationId']
    }
    if 'parameters' in req_data:
        parameters = read_parameters(req_data['parameters'])
        parsed['parameters'] = parameters
    return parsed


def read_controllers():
    controllers = {}
    path_dict = swagger['paths']
    for path, path_data in path_dict.items():
        for req_type, req_data in path_data.items():
            controller_name = req_data['tags'][0]
            temp = parse_req_data(req_type, path, req_data)

            if controller_name not in controllers:
                controllers[controller_name] = []
            controllers[controller_name].append(temp)

    return controllers


def print_annotation_path(req_type, req_path):
    print('@' + req_type.upper() + '("' + req_path + '")')


def print_request_name(req_name):
    index = req_name.find('Using')
    print('fun ' + req_name[:index])


def print_request_parameters(req_param_list):
    if 'parameters' not in req_param_list:
        print('()')
    else:
        query = '('
        for params in req_param_list['parameters']:
            in_arg = params['in']
            if in_arg == 'body':
                continue

            query += '@'
            query += in_arg.title()

            name = params['name']
            name = name[0].lower() + name[1:]
            query += '("' + params['name'] + '") ' + name + ': '

            lang_type = params['type']
            need_capitalize = lang_type == 'string' or lang_type == 'boolean'
            if need_capitalize:
                query += lang_type.title()
            elif lang_type == 'integer':
                query += 'Long'
            else:
                query += lang_type

            if not params['required']:
                query += '? = null'

            query += ',\n'

        query = query[:-2]
        query += ')'
        print(query)


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
