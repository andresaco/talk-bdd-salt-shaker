Feature: Serving
  As a hungry diner, 
  I want to add some salt to my plate
  To Make my food tastier

  Scenario: Single Service
    Given A Salt Shaker with 100 doses
    When I shake it once
    Then 1 salt dose falls on my plate

  Scenario: Empty shaker
    Given A Salt shaker with 0 doses
    When I shake it once
    Then 0 salt dose falls on my plate
    And It's empty!