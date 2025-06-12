import sys
from loguru import logger

sys.tracebacklimit = 5


def pytest_make_parametrize_id(val):
    return repr(val)


def pytest_runtest_setup(item):
    logger.info(f"[SETUP]    {item.nodeid}")


def pytest_runtest_call(item):
    logger.info(f"[CALL]     {item.nodeid}")


def pytest_runtest_teardown(item, nextitem):
    logger.info(f"[TEARDOWN] {item.nodeid}")
