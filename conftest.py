def pytest_configure(config):
    from fandango.beartype import activate_beartype

    activate_beartype()
