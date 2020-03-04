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

```Gherkin
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

_Et voilá_. We have coded the tests for our first scenario.

### Running our first test

As pytest-bdd is a plugin for pytest module, the way we run our test is as follows:

```sh
python -m pytest step_1/test
```

Even though pytest execution can be launched u

Pytest will [discover test modules](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery) within the tests directory and perform the checks as declared in our step definition functions.



[behave-lib]: https://behave.readthedocs.io/en/latest/
[pytest-bdd-lib]: https://pytest-bdd.readthedocs.io/en/stable/
[lettuce-lib]: http://lettuce.it/tutorial/simple.html
[BDD]: https://en.wikipedia.org/wiki/Behavior-driven_development
[Gherkin]: https://cucumber.io/docs/gherkin/
[TDD]: https://en.wikipedia.org/wiki/Test-driven_development