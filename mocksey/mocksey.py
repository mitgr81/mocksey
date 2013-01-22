class MockseyObject(object):

    def __repr__(self):
        return "Mock%s" % self.__class__.__name__

    def stub_method(self):
        pass


def generate_mock(subject):

    mock = MockseyObject()
    mock.__class__.__name__ = subject.__name__
    for attr in dir(subject):
        if len(attr) > 1 and attr[1] != '_':
            val = getattr(subject, attr)
            if callable(val):
                val = mock.stub_method
            setattr(mock, attr, val)
    return mock
