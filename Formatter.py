from abc import ABC, abstractmethod


def filter_class(full_definition):
    last_splash = full_definition.rfind('/')
    return full_definition[last_splash + 1:]


class AbstractFormatter(ABC):
    def __init__(self):
        self.rx_type = self.get_rx_type()

    @abstractmethod
    def get_rx_type(self):
        pass

    def print(self, responses):
        is_type_completable = 'schema' not in responses
        if is_type_completable:
            print(':Completable')
        else:
            self.print_as_sequence(responses['schema'])

    def print_as_sequence(self, param):
        if 'type' in param:
            has_list = param['type'] == 'array'
            if has_list:
                result = self.read_as_list(param)
            else:
                result = self.read_as_object(param)
        else:
            result = self.read_as_dto(param)
        print(result)

    def read_as_list(self, param):
        items_ = param['items']
        temp = ':' + self.rx_type + '<List<'
        if 'type' in items_:
            temp += items_['type'].title()
        elif '$ref' in items_:
            full_definition = items_['$ref']
            splash_ = filter_class(full_definition)
            temp += splash_
        else:
            raise Exception('A very specific bad thing happened')
        temp += '>>'
        return temp

    def read_as_object(self, param):
        title = param['type'].title()
        return ':' + self.rx_type + '<' + title + '>'

    def read_as_dto(self, param):
        full_definition = param['$ref']
        splash_ = filter_class(full_definition)
        result = ':' + self.rx_type + '<' + splash_ + '>'
        return result


class SingleFormatter(AbstractFormatter):
    def get_rx_type(self):
        return 'Single'


class FlowableFormatter(AbstractFormatter):
    def get_rx_type(self):
        return 'Flowable'
