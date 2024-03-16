Feature: Product Management

  Scenario: Create a new product
    Given I submit a new product data
    Then the product should be created successfully

  Scenario: Get product by category
    Given there are products with a specific category
    When I request to get the products by category
    Then I should receive the products details by category

  Scenario: Get product by ID
    Given there is a product with a specific ID
    When I request to get the product by ID
    Then I should receive the product details by ID

  Scenario: Get all products
    Given there are existing products in the system
    When I request to get all products
    Then I should receive a list of products

  Scenario: Update product data
    Given there is a registered product
    When I request to update a product
    Then the product data is successfully updated

  Scenario: Remove a product
    Given there is a product on database with specific id
    When I request to remove a product
    Then the product data is successfully removed
