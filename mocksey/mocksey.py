import types
import unittest


def mocksey_assert_equal(expected, actual, message=None):
    class TestDummy(unittest.TestCase):
        def nop(self):
            pass

    asserter = TestDummy().assertEqual
    asserter.__self__.maxDiff = None

    asserter(expected, actual, message)


class MockseyObject:
    def __init__(self):
        self.expected_functions = {}
        self.called_functions = {}

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return f"Mock{self.__class__.__name__}"

    def __getattr__(self, function_name):
        if function_name in self.expected_functions:

            def function(*args, **kwargs):
                self.called_functions[function_name] = self.called_functions.get(function_name, {"count": 0})
                self.called_functions[function_name]["count"] += 1
                count = self.called_functions[function_name]["count"]

                self.called_functions[function_name][count - 1] = {"args": args, "kwargs": kwargs}
                if "return" in self.expected_functions[function_name]:
                    return self.expected_functions[function_name]["return"].get(
                        count - 1,
                        self.expected_functions[function_name]["return"].get("*", None),
                    )

            return function
        else:

            def unexpected_function(*args, **kwargs):
                # We may want to add a flag to do strict checks here where it fails if this function is called
                # ...not now though
                pass

            return unexpected_function

    def run_asserts(self, assert_equal=mocksey_assert_equal):
        for function_name, function_data in self.expected_functions.items():
            msg_head = f"Mockseyed{self.__class__.__name__} expected '{function_name}'"
            actual = self.called_functions.get(function_name, {"count": 0})["count"]
            if function_data.get("count", 0) > 0:
                expected = self.expected_functions[function_name]["count"]
                assert_equal(expected, actual, f"{msg_head} to be called {expected} times, but it was called {actual}.")
                for call in range(function_data["count"]):
                    expected_params = function_data.get(call, {"args": "*", "kwargs": "*"})
                    if expected_params["args"] != "*":
                        assert_equal(expected_params["args"], self.called_functions[function_name][call]["args"])
                    if expected_params["kwargs"] != "*":
                        assert_equal(expected_params["kwargs"], self.called_functions[function_name][call]["kwargs"])
            elif function_data.get("count", 0) == -1:
                assert_equal(0, actual, f"{msg_head} to never be called times, but it was called {actual}.")

    def expect_once(self, expected_function, args="*", kwargs="*"):
        self.expect_call_count(expected_function, 1)
        self.expect_at(expected_function, 0, args=args, kwargs=kwargs)

    def expect_at(self, expected_function, index, args="*", kwargs="*"):
        self.expected_functions[expected_function][index] = {"args": args, "kwargs": kwargs}
        self.expect_call_count(expected_function, index + 1)

    def expect_call_count(self, expected_function, count):
        self.expected_functions[expected_function] = self.expected_functions.get(expected_function, {"count": 0})
        if count == -1 or self.expected_functions[expected_function].get("count", 0) < count:
            self.expected_functions[expected_function]["count"] = count

    def expect_never(self, expected_function):
        self.expect_call_count(expected_function, -1)

    def returns(self, returning_function, return_value):
        self.returns_at("*", returning_function, return_value)

    def returns_at(self, count, returing_function, retval):
        self.expected_functions[returing_function] = self.expected_functions.get(returing_function, {"count": 0})
        self.expected_functions[returing_function]["return"][count] = retval

    def raises(self, raising_function, exception):
        def mock_raiser(*args, **kwargs):
            raise exception

        setattr(self, raising_function, mock_raiser)
        return mock_raiser


def generate_mock(subject):
    mock = MockseyObject()
    mock.__class__.__name__ = subject.__name__
    for attr in dir(subject):
        if len(attr) > 1 and attr[1] != "_":
            val = getattr(subject, attr)
            if callable(val):
                mock.expected_functions[attr] = {"return": {"*": None}}
                types.MethodType(val, mock)
            else:
                setattr(mock, attr, val)
    return mock
