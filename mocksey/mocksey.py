import types


def assert_equal(expected, actual, message=''):
    assert expected == actual, message


class MockseyObject(object):

    def __init__(self):
        self.expected_functions = {}
        self.actual_functions = {}

    def __repr__(self):
        return "Mock%s" % self.__class__.__name__

    def __getattr__(self, called_function):
        if called_function in self.expected_functions:
            def function(*args, **kwargs):
                # if called_function not in self.actual_functions:
                #     self.actual_functions[called_function] = {'count': 0}
                self.actual_functions[called_function] = self.actual_functions.get(called_function, {'count': -1})
                self.actual_functions[called_function]['count'] += 1
                count = self.actual_functions[called_function]['count']
                # self.actual_functions[called_function]['count'] = count
                # self.actual_functions[called_function][count] = {
                #     'args': args,
                #     'kwargs': kwargs,
                # }
                if 'return' in self.expected_functions[called_function]:
                    # import pdb; pdb.set_trace()
                    return self.expected_functions[called_function]['return'].get(count, self.expected_functions[called_function]['return'].get('*', None))
            return function
        else:
            def unexpected_function(*args, **kwargs):
                #We may want to add a flag to do strict checks here where it fails if this function is called
                #...not now though
                pass
            return unexpected_function
        return self.properties[called_function]

    def run_asserts(self, assert_equal=assert_equal):
        for function_name, function_data in self.expected_functions.iteritems():
            if function_data.get('count', 0) > 0:
                expected = self.expected_functions[function_name]['count']
                actual = self.actual_functions.get(function_name, {'count': 0})['count']
                assert_equal(expected, actual, "Mocksey expected %s to be called %d times, but it was called %d." % (function_name, expected, actual))

    def expect_once(self, func, args='*', kwargs='*'):
        self.expect_call_count(func, 1)

    def expect_call_count(self, func, count):
        self.expected_functions[func] = self.expected_functions.get(func, {'count': 0})
        self.expected_functions[func]['count'] = count

    def returns(self, function, return_value):
        self.returns_at('*', function, return_value)

    def returns_at(self, count, func, retval):
        self.expected_functions[func] = self.expected_functions.get(func, {'count': 0})
        self.expected_functions[func]['return'][count] = retval


def generate_mock(subject):

    mock = MockseyObject()
    mock.__class__.__name__ = subject.__name__
    for attr in dir(subject):
        if len(attr) > 1 and attr[1] != '_':
            val = getattr(subject, attr)
            if callable(val):
                mock.expected_functions[attr] = {'return': {'*': None}}
                # import pdb; pdb.set_trace()
                # bind(mock, val, attr)
                # setattr(mock.__class__, attr, val.__get__(mock, mock.__class__))
                types.MethodType(val, mock, MockseyObject)
            else:
                setattr(mock, attr, val)
    return mock
