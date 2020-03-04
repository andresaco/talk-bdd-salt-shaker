bdd-salt-shaker
===============

Let's develop a Salt shaker using BDD and Python!

This repository contains a humble introduction to [Behaviour-Driven development][BDD] with Python. The source code including tests within this repository will help you understanding the basics for BDD development by developing a simple program.

## What is BDD?

Behaviour Driven Development (BDD) is a process where software is developed starting from the functional definition of the product. This means that no only technical staff is involved in the process from the beginning, but also QA and Business participants may join this process in order to provide a better approach to our product.

To describe how the product should work, it may be difficult for non-technical staff to write things like tests for describing the expected behaviour. Instead, there are some DSLs like [Gherkin] that help formalise the scenarios that describe our product scope.

In practice, BDD is an extension of [Test-Driven Development][TDD] as both processes start by defining tests firsts. From the tests, developers shall implement the product so the tests are executed successfully without errors. TDD also differs from BDD in their target scope. TDD may include tests at any level (unit, integration, acceptance), and BDD is mainly scoped at Acceptance Testing, due to its behavioural approach.

Our First BDD project: Salt Shaker
----------------------------------

![Shaker][shaker_img]

This repository contains a simple project aimed at better understanding how BDD works... a Salt Shaker!

Your favourite restaurant asks you to develop a salt shaker that contains by default an amount of salt doses. This shaker shall help customers to perform a single action:

* __Serve salt__: Drop a salt dose on their favourite meal.

Just like there are customer that don't put salt on their plates, there are others that love salty plates, so think of scenarios where users take more than one dose from their plates.

... just one more thing. Don't think on features like "Refilling the shaker" or stuff like that. Only think in __Serving__

[shaker_img]: https://static.thenounproject.com/png/41717-200.png

Source code repository
----------------------

Along this article, a [source code repository](https://github.com/andresaco/bdd-salt-shaker) can be cloned or downloaded. Check it out! And remember that contributions are kindly accepted.

### Developer background

This article asumes readers have a minimum knowledge on software development using Python language. Topics such as modules installation and virtual environments management are not covered within this article. In case you are not familiar with them, check this article about [Python set-up for developers](https://www.datacamp.com/community/tutorials/python-developer-set-up) I wrote in Datacamp site.

Writing a Features File
-----------------------

Behavioural tests using Gherkin starts by defining feature files. These files group a single feature from our product, enclosing all the possible related scenarios. For our Shaker project, we could think on the simplest scenario:

* Shaking once the shaker will result in a salt dose on my plate.

 The simplest case, usually called [Happy Path](https://en.wikipedia.org/wiki/Happy_path) usually occurs without errors nor abnormal results. Other cases shall be considered as well, describing scenarios not covered by the happy path:
 
* Shaking the shaker more than once will result in multiple doses on my plate.
* Shaking an empty shaker will result in no dose on my plate.

Using Gherkin language, our Happy Path could be expressed as follows:

```gherkin
  Scenario: Single Service
    Given A Salt Shaker
    When I shake it once
    Then A salt dose falls on my plate
```

Don't worry about the other sections. We'll cover them along the following sections ;)

Coding test Scenarios
---------------------

For Python developers, there a some options that allow writing tests specified in Gherkin language. Among these options, the most famous are listed below:

* [behave][behave-lib]
* [pytest-bdd][pytest-bdd-lib]
* [lettuce][lettuce-lib]

For this article we will use pytest-bdd as our choice for writing the tests.

Using [pytest-bdd] we will write a module `test_serving.py` where we will write the test functions. Note that `features` and `tests` directories are separated. This means that the `*.feature` and test files are not necessarily within the same directory.

The first thing a test file shall specify is declare the feature file and the covered scenarios. We can do that through the use of the `scenario` or `scenarios` functions in pytest-bdd:

```python
from pytest_bdd import scenarios

scenarios('../features/serving.feature')
```

The code shown above declared that this module will cover all the scenarios within the `serving.feature` file. For covering specific scenarios, make use of the [`scenario`](https://pytest-bdd.readthedocs.io/en/stable/#scenario-decorator) method. Note that both methods can be used as function calls or decorators!

### Introducing Step Definitions

Once the test module is linked to the feature file, test steps are associated to code using the `given`, `when` and `then` decorators. For our example, the single serving scenario definitions are written as follows:

```python
from pytest_bdd import given, when, then

from salty import Shaker

@given("A Salt Shaker")
def salt_shaker(doses):
    yield Shaker(doses)

@pytest.fixture
@when("I shake it once")
def served(salt_shaker):
    yield salt_shaker.shake()

@then("A salt dose falls on my plate")
def doses_serve(served):
    assert served == 1
```

Note that we have written three functions, each one mapping to a step definition using the same text that describes the step in the feature file. Note that we have added another `pytest.fixture` decorator the the when function, as we will use the returned value of the when function in the final `then` step definition.

_Et voilá_. We have coded the tests for our first scenario!

### Running our first test

As pytest-bdd is a plugin for [pytest][pytest-lib] module, the way we run our test is as follows:

```sh
python -m pytest step_1/tests
```

Even though pytest execution can be launched using the pytest command, we will launch them using `python -m pytest` for adding the salty
module to the `sys.path` entries. You can read more about pytest python path settings in pytest [official documentation](https://docs.pytest.org/en/latest/pythonpath.html#invoking-pytest-versus-python-m-pytest).

When executing the previous command, pytest will [discover test modules](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery) within the tests directory and perform the checks as declared in our step definition functions. The command output is the following:

```shell script
==================== test session starts =====================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/japizarro/Personal/Talks/bdd-salt-shacker-definitive
plugins: bdd-3.2.1
collected 1 item                                                                                                                                                                     

step_1/tests/test_serving.py .                          [100%]

===================== 1 passed in 0.02s ======================
```

Out of salt! Testing the not-so-happy paths
-------------------------------------------

As mentioned above, testing the happy path only checks part of your code. It is usually required to test edge scenarios where nominal behaviour changes.

For our salt shaker module, an edge scenario could be shaking an empty shaker. The result shall be serving no dose on a food plate. We could express that feature as follows:

```gherkin
  Scenario: Empty shaker
    Given An empty salt shaker
    When I shake it once
    Then no dose falls on my plate
    And It's empty!
```

Based on the given scenario definition, we could write our tests functions as follows...

```python
@given("An empty salt shaker")
def empty_salt_shaker():
    yield Shaker(doses=0)

@then("no dose falls on my plate")
def no_dose(shake):
    assert shake == 0

@then("It's empty!")
def its_empty(empty_salt_shaker):
    assert empty_salt_shaker.remaining == 0
```

As you can see, we have not implemented the "I Shake it once" step defined, as it was previously defined for the first scenario. Furthermore, we will go over a set of improvements we can apply to our step definitions in order get a simpler version of our tests.

### Reuse step definitions

Taking into account the defined test scenarios (Single Service and Empty Shaker), there are some steps that are strictly related:

* An empty salt shaker is just a salt shaker with 0 doses of salt. For our scenarios, we could express them as follows:

```gherkin
  Scenario: Single Service
    Given A Salt Shaker with 100 doses
    When I shake it once
    Then A salt dose falls on my plate

  Scenario: Empty shaker
    Given A Salt shaker with 0 doses
    When I shake it once
    Then no dose falls on my plate
    And It's empty!
```

Now, instead of two different `given` step definitions, we have only one with a _step argument_ as follows:

```python
@given(parsers.cfparse("A Salt Shaker with {doses:d} doses"))
def salt_shaker(doses):
    yield Shaker(doses)
```

In a similar manner, the `then` step where the doses served can be check can be merged into a step with arguments. This could be the gherkin code for both scenarios:

```gherkin
  Scenario: Single Service
    Given A Salt Shaker with 100 doses
    When I shake it once
    Then 1 salt dose falls on my plate

  Scenario: Empty shaker
    Given A Salt shaker with 0 doses
    When I shake it once
    Then 0 salt dose falls on my plate
    And It's empty!
```

And so the step definitions can be reimplemented as follows:

```python
@then(parsers.cfparse("{expected_served:d} salt dose falls on my plate"))
def served_doses(served, expected_served):
    assert served == expected_served
```

Pytest-BDD provides a parser object for processing step arguments and injecting them into the functions that require them. By default these arguments are processed as String objects, but some formatting can be specified based on the [parse][pypi-parse] module. Furthermore, step arguments can consists on regular expressions or custom objects!

Check the `step_2` in the code repository to see how the tests and feature file result after these changes. As an assignment to test your knowledge of this technique, I suggest you to try adding a step to the _Single Service_ Scenario that checks the salt shaker has 99 remaining doses (hint: And The shaker has 99 units), and merge it with the "It's empty!" step defined in the _Empty shaker_ scenario.

Shake it baby! Scenario outlines
--------------------------------

Maybe not you, but when I put some salt in a plate, I shake the salt shaker more than once. We will write another scenario to describe this use case:

```gherkin
  Scenario: Serve multiple times
    Given A Salt Shaker with 100 doses
    When I shake the shaker 10 times
    Then 10 salt dose falls on my plate
    And The shaker contains 90 doses
```

Starting with the given scenario, we could write our step definitions for the given scenario with the following code:

```python
@pytest.fixture
@when(parsers.parse("I shake {shakes:d} times"))
def multi_shake(salt_shaker, shakes):
    doses = 0
    for i in range(0, shakes):
        doses += salt_shaker.shake()
    yield doses

@then(parsers.parse("The shaker contains {expected_remaining:d} doses"))
def check_remaining(salt_shaker, expected_remaining):
    assert salt_shaker.remaining == expected_remaining
```

Plus, all the serving scenarios could be merged into one single step!

```gherkin
  Scenario: Single Service
    Given A Salt Shaker with 100 doses
    When I shake the shaker 1 times
    Then 1 salt dose falls on my plate

  Scenario: Empty shaker
    Given A Salt shaker with 0 doses
    When I shake the shaker 1 times
    Then 0 salt dose falls on my plate
    And The shaker contains 00 doses

  Scenario: Serve multiple times
    Given A Salt Shaker with 100 doses
    When I shake the shaker 10 times
    Then 10 salt dose falls on my plate
    And The shaker contains 90 doses
```

The new scenario seems good, but not enough. The choice of specifying 10 shakes instead of another amount seems arbitrary. Furthermore, In case we want to add similar scenarios with different shakes, is it a good idea to just copy and paste the scenario? This task becomes tedious and repetitive, and it the long term leads to an unmantainable state. 

### Introducing Scenario Outlines

Gherkin allows to define templates for running the same scenario multiple times with different combinations of values. These templates are usually called _Scenario Outlines_.

On a given scenario, the template parameters are written between brackets `< >`. The parameter values for each tests are written inside and _Examples_ table

```gherkin
  Scenario: Serve multiple times
    Given A Salt Shaker with <doses> doses
    When I shake the shaker <serve> times
    Then <served> salt doses fall on my plate
    And The shaker contains <remain> doses

    Examples:
      | doses | serve | remain | served |
      | 20    | 10    | 10     | 10     |
      | 50    | 10    | 40     | 10     |
      | 20    | 20    | 0      | 20     |
      | 3     | 2     | 1      | 2      |
      | 3     | 5     | 0      | 3      |
```

Did you noticed that? We are testing a new edge case where more shakes than remaining doses are performed! Think about the last example ;)

Upon the Scenario definition shown above, a total of 5 tests will be executed, performing all the described checks.

Similarly to the template arguments seen in previous sections, Scenario templates require parsing the input values into proper types. Unfortunately, this case is not as simple
as reusing the parsers object seen previously. Instead, converters shall be defined within the test module for a given scenario (or for all of them).

```python
CONVERTERS = dict(doses=int, serve=int, remain=int, served=int)

scenarios('../features/serving.feature', example_converters=CONVERTERS)
```

The final code for our feature testing will be as follows:

```python
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
```

Notice that Step definition decorators had to be written twice. This is due to the regular and template Scenarios that share the same syntax. But in the real world, this is not a common thing.

When executing the tests suite the following output shall be shown:

```shell script
===================== test session starts =====================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/japizarro/Personal/Talks/bdd-salt-shacker-definitive
plugins: bdd-3.2.1
collected 7 items                                                                                                                                                                                                                                                    

step_3/tests/test_serving.py .......                    [100%]

===================== 7 passed in 0.04s ======================
```

As mentioned above, we defined 3 Scenarios, but a total of 7 test items have been executed. This is due to the Scenario outline conversion to five tests items, one per entry in the Examples table. 

[behave-lib]: https://behave.readthedocs.io/en/latest/
[pypi-parse]: https://pypi.org/project/parse/
[pytest-lib]: https://docs.pytest.org/en/latest/
[pytest-bdd-lib]: https://pytest-bdd.readthedocs.io/en/stable/
[lettuce-lib]: http://lettuce.it/tutorial/simple.html
[BDD]: https://en.wikipedia.org/wiki/Behavior-driven_development
[Gherkin]: https://cucumber.io/docs/gherkin/
[TDD]: https://en.wikipedia.org/wiki/Test-driven_development