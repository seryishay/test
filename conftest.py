from const import *

def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")


def pytest_generate_tests(metafunc):
    if "param1" in metafunc.fixturenames:
        if metafunc.config.getoption("all"):
            end = PARAM_MAX - 1
        else:
            end = 1
        metafunc.parametrize("param1", range(end))