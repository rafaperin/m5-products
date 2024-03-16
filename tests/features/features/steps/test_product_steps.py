import json

import pytest

from pytest_bdd import scenario, given, then, when
from starlette import status
from starlette.testclient import TestClient

from src.app import app
from tests.utils.product_helper import ProductHelper


client = TestClient(app)


@pytest.fixture
def generate_product_dto():
    return ProductHelper.generate_product_request()


@pytest.fixture
def generate_multiple_product_dtos():
    return ProductHelper.generate_multiple_products()


@pytest.fixture
def generate_update_product_dto():
    return ProductHelper.generate_updated_product_data()


@pytest.fixture
def request_product_creation(generate_product_dto):
    product = generate_product_dto
    req_body = {
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "image_url": product.image_url,
    }
    headers = {}
    response = client.post("/products", json=req_body, headers=headers)

    resp_json = json.loads(response.content)
    result = resp_json["result"]
    product_id = result["productId"]

    yield response
    # Teardown - Removes the customer from the database
    client.delete(f"/products/{product_id}", headers=headers)


@pytest.fixture
def request_multiple_products_creation(generate_multiple_product_dtos):
    products_list = generate_multiple_product_dtos
    product_ids_list = []
    headers = {}

    for product in products_list:
        req_body = {
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "image_url": product.image_url,
        }
        response = client.post("/products", json=req_body, headers=headers)

        resp_json = json.loads(response.content)
        result = resp_json["result"]
        product_id = result["productId"]
        product_ids_list.append(product_id)
    yield product_ids_list
    # Teardown - Removes the customer from the database
    for product_id in product_ids_list:
        client.delete(f"/products/{product_id}", headers=headers)


@pytest.fixture
def create_product_without_teardown(generate_product_dto):
    product = generate_product_dto
    req_body = {
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "image_url": product.image_url,
    }
    headers = {}
    response = client.post("/products", json=req_body, headers=headers)
    print("aaaa"  +str(response.content))
    yield response.content


# Scenario: Create a new product


@scenario('../product.feature', 'Create a new product')
def test_create_product():
    pass


@given('I submit a new product data', target_fixture='i_request_to_create_a_new_product_impl')
def i_request_to_create_a_new_product_impl(generate_product_dto, request_product_creation):
    response = request_product_creation
    return response


@then('the product should be created successfully')
def the_product_should_be_created_successfully_impl(i_request_to_create_a_new_product_impl, generate_product_dto):
    product = generate_product_dto
    resp_json = json.loads(i_request_to_create_a_new_product_impl.content)
    result = resp_json["result"]

    assert result["name"] == product.name
    assert result["description"] == product.description
    assert result["category"] == product.category
    assert result["price"] == product.price
    assert result["imageUrl"] == product.image_url


# Scenario: Get product by category

@scenario('../product.feature', 'Get product by category')
def test_get_product_by_category():
    pass


@given('there are products with a specific category', target_fixture='product_with_given_category')
def customer_with_given_category(request_product_creation):
    product = request_product_creation
    return product


@when('I request to get the products by category', target_fixture='request_product_by_category')
def request_product_by_category(product_with_given_category):
    product_response = product_with_given_category
    resp_json = json.loads(product_response.content)
    product_category = resp_json["result"]["category"]

    headers = {}
    response = client.get(f"/products/category/{product_category}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    return response.content


@then('I should receive the products details by category')
def receive_given_product(request_product_by_category, generate_product_dto):
    product = generate_product_dto
    resp_json = json.loads(request_product_by_category)
    result = resp_json["result"]

    for item in result:
        assert item["name"] == product.name
        assert item["description"] == product.description
        assert item["category"] == product.category
        assert item["price"] == product.price
        assert item["imageUrl"] == product.image_url


# Scenario: Get product by ID

@scenario('../product.feature', 'Get product by ID')
def test_get_product_by_id():
    pass


@given('there is a product with a specific ID', target_fixture='product_with_given_id')
def product_with_given_id(request_product_creation):
    response = request_product_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["productId"]


@when('I request to get the product by ID', target_fixture='request_product_by_id')
def request_product_by_id(product_with_given_id):
    product_id = product_with_given_id
    headers = {}
    response = client.get(f"/products/id/{product_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the product details by ID')
def receive_correct_product(product_with_given_id, request_product_by_id, generate_product_dto):
    product_id = product_with_given_id
    product = generate_product_dto
    resp_json = json.loads(request_product_by_id)
    result = resp_json["result"]

    assert result["productId"] == product_id
    assert result["name"] == product.name
    assert result["description"] == product.description
    assert result["category"] == product.category
    assert result["price"] == product.price
    assert result["imageUrl"] == product.image_url


# Scenario: Get all products

@scenario('../product.feature', 'Get all products')
def test_get_all_products():
    pass


@given('there are existing products in the system', target_fixture='existing_products_in_db')
def existing_customers_in_db(request_multiple_products_creation):
    products_id_list = request_multiple_products_creation
    return products_id_list


@when('I request to get all products', target_fixture='request_all_products')
def request_all_products():
    headers = {}
    response = client.get(f"/products/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive a list of products')
def receive_correct_customer(existing_products_in_db, request_all_products):
    products_id_list = existing_products_in_db
    response = request_all_products
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert type(result) == list

    for item in result:
        assert item["productId"] in products_id_list


# Scenario: Update customer data

@scenario('../product.feature', 'Update product data')
def test_update_customer():
    pass


@given('there is a registered product', target_fixture='existing_product')
def existing_product(request_product_creation):
    response = request_product_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result


@when('I request to update a product', target_fixture='request_product_update')
def request_product_update(existing_product, generate_update_product_dto):
    product = existing_product
    product_id = product["productId"]

    updated_product = generate_update_product_dto
    req_body = {
        "name": updated_product.name,
        "description": updated_product.description,
        "category": updated_product.category,
        "price": updated_product.price,
        "image_url": updated_product.image_url
    }

    headers = {}
    response = client.put(f"/products/{product_id}", json=req_body, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the product data is successfully updated')
def receive_correct_product(request_product_update, generate_update_product_dto):
    updated_product = generate_update_product_dto

    response = request_product_update
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert result["name"] == updated_product.name
    assert result["description"] == updated_product.description
    assert result["category"] == updated_product.category
    assert result["price"] == updated_product.price
    assert result["imageUrl"] == updated_product.image_url


# Scenario: Remove a customer

@scenario('../product.feature', 'Remove a product')
def test_remove_product():
    pass


@given('there is a product on database with specific id', target_fixture='existing_product_to_remove')
def existing_product_to_remove(create_product_without_teardown):
    product = create_product_without_teardown
    return product


@when('I request to remove a product', target_fixture='request_product_update')
def request_product_delete(existing_product_to_remove):
    response = existing_product_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    product_id = result["productId"]

    headers = {}
    response = client.delete(f"/products/{product_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the product data is successfully removed')
def receive_correct_product(existing_product_to_remove):
    response = existing_product_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    product_id = result["productId"]

    headers = {}
    response = client.get(f"/products/id/{product_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
