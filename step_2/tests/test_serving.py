import pytest
from pytest_bdd import parsers, scenarios, given, when, then

from salty import Shaker

scenarios('../features/serving.feature')


@given(parsers.cfparse("A Salt Shaker with {doses:d} doses"))
def salt_shaker(doses):
    yield Shaker(doses)


@pytest.fixture
@when("I shake it once")
def served(salt_shaker):
    yield salt_shaker.shake()


@then(parsers.cfparse("{expected_served:d} salt dose falls on my plate"))
def served_doses(served, expected_served):
    assert served == expected_served


@then("It's empty!")
def its_empty(salt_shaker):
    assert salt_shaker.remaining == 0
