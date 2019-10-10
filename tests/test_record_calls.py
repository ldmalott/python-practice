from python_practice.record_calls import record_calls


def test_record_calls():

    @record_calls
    def greet(name):
        """Greet someone by their name."""
        print(f"Hello {name}")

    assert greet.__doc__ == """Greet someone by their name."""
    assert len(greet.calls) == 0

    greet('levi')
    assert len(greet.calls) == 1
    assert greet.calls[0].args == ('levi',)
    assert greet.calls[0].kwargs == {}
    assert greet.calls[0].exception == None
    assert greet.calls[0].return_value == None


    greet(name='daniel')
    assert len(greet.calls) == 2
    assert greet.calls[1].args == ()
    assert greet.calls[1].kwargs == {'name': 'daniel'}
    assert greet.calls[1].exception == None
    assert greet.calls[1].return_value == None


def test_record_call_exception():
    @record_calls
    def throw(msg):
        raise Exception(msg)

    try:
        throw('hi')
    except Exception as exc:
        assert len(throw.calls) == 1
        assert throw.calls[0].args == ('hi',)
        assert throw.calls[0].kwargs == {}
        assert throw.calls[0].return_value == None
        assert exc == throw.calls[0].exception


def test_record_calls_return_values():
    @record_calls
    def add(x):
        return x + 1

    y = add(1)
    assert len(add.calls) == 1

    call = add.calls[0]
    assert call.args == (1,)
    assert call.kwargs == {}
    assert call.exception == None
    assert call.return_value == 2 == y


