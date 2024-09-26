import pytest
from pytest_bdd import scenarios, given, when, then

from salty import Shaker

scenarios("../features/serving.feature")


@pytest.fixture
def shaker():
    return Shaker()


@given("A Salt Shaker", target_fixture="shaker")
def salt_shaker(shaker):
    return shaker


@when("I shake it once", target_fixture="served_doses")
def served(shaker):
    yield shaker.shake()


@then("A salt dose falls on my plate")
def doses_serve(served_doses):
    assert served_doses == 1
