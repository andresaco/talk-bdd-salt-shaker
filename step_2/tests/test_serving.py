from pytest_bdd import parsers, scenarios, given, when, then

from salty import Shaker

scenarios("../features/serving.feature")


@given(parsers.parse("A Salt Shaker with {doses:d} doses"), target_fixture="shaker")
def salt_shaker(doses):
    yield Shaker(doses)


@when("I shake it once", target_fixture="served")
def served(shaker):
    yield shaker.shake()


@then(parsers.parse("{expected_served:d} salt dose falls on my plate"))
def served_doses(served, expected_served):
    assert served == expected_served


@then("It's empty!")
def its_empty(shaker):
    assert shaker.remaining == 0
