import pytest
from pytest_bdd import scenarios, given, when, then

from salty import Shaker

scenarios('../features/serving.feature')

@given("A Salt Shaker")
def salt_shaker():
    yield Shaker()

@pytest.fixture
@when("I shake it once")
def served(salt_shaker):
    yield salt_shaker.shake()

@then("A salt dose falls on my plate")
def doses_serve(served):
    assert served == 1