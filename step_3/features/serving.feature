Feature: Serving
  As a hungry diner,
  I want to add some salt to my plate
  To Make my food tastier

  Scenario: Single Service
    Given A Salt Shaker with 100 doses
    When I shake the shaker 1 times
    Then 1 salt doses falls on my plate

  Scenario: Empty shaker
    Given A Salt Shaker with 0 doses
    When I shake the shaker 1 times
    Then 0 salt doses falls on my plate
    And The shaker contains 0 doses

  Scenario: Serve multiple times
    Given A Salt Shaker with <doses> doses
    When I shake the shaker <shakes> times
    Then <expected_served> salt doses fall on my plate
    And The shaker contains <expected_remaining> doses


    Examples:
      | doses | shakes | expected_remaining | expected_served |
      | 20    | 10     | 10                 | 10              |
      | 50    | 10     | 40                 | 10              |
      | 20    | 20     | 0                  | 20              |
      | 3     | 2      | 1                  | 2               |
      | 3     | 5      | 0                  | 3               |