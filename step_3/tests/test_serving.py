import pytest
from pytest_bdd import parsers, scenarios, given, when, then

from salty import Shaker

scenarios("../features/serving.feature")


@pytest.fixture
def shaker():
    return Shaker()


@given(
    parsers.parse("A Salt Shaker with {doses} doses"),
    converters=dict(doses=int),
    target_fixture="shaker",
)
def salt_shaker(doses):
    yield Shaker(doses)


@pytest.fixture
@when(
    parsers.parse("I shake the shaker {shakes} times"),
    converters=dict(shakes=int),
    target_fixture="shakes",
)
def served(shaker, shakes):
    doses = 0
    for i in range(0, shakes):
        doses += shaker.shake()
    yield doses


@then(
    parsers.parse("{expected_served} salt doses fall on my plate"),
    converters=dict(expected_served=int),
)
def served_doses(shakes, expected_served):
    assert shakes == expected_served


@then(
    parsers.parse("The shaker contains {expected_remaining} doses"),
    converters=dict(expected_remaining=int),
)
def check_remaining(shaker, expected_remaining):
    assert shaker.remaining == expected_remaining
