class MockseyObject(object):
    pass


def generate_mock(subject):

    mock = MockseyObject()
    mock.__class__.__name__ = subject.__name__
    return mock
