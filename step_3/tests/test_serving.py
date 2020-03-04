import pytest
from pytest_bdd import parsers, scenarios, given, when, then

from salty import Shaker

CONVERTERS = dict(doses=int, shakes=int, expected_remaining=int, expected_served=int)

scenarios('../features/serving.feature', example_converters=CONVERTERS)


@given("A Salt Shaker with <doses> doses")
@given(parsers.cfparse("A Salt Shaker with {doses:d} doses"))
def salt_shaker(doses):
    yield Shaker(doses)


@pytest.fixture
@when(parsers.parse("I shake the shaker {shakes:d} times"))
@when("I shake the shaker <shakes> times")
def served(salt_shaker, shakes):
    doses = 0
    for i in range(0, shakes):
        doses += salt_shaker.shake()
    yield doses


@then(parsers.cfparse("{expected_served:d} salt doses falls on my plate"))
@then("<expected_served> salt doses fall on my plate")
def served_doses(served, expected_served):
    assert served == expected_served


@then(parsers.parse("The shaker contains {expected_remaining:d} doses"))
@then("The shaker contains <expected_remaining> doses")
def check_remaining(salt_shaker, expected_remaining):
    assert salt_shaker.remaining == expected_remaining
