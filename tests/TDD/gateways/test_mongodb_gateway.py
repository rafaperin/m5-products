import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.entities.models.product_entity import Product, Category
from src.interfaces.gateways.product_gateway_interface import IProductGateway
from tests.utils.product_helper import ProductHelper


class MockRepository(IProductGateway):
    def get_by_id(self, product_id: uuid.UUID) -> Product:
        pass

    def get_all_by_category(self, category: str) -> List[Product]:
        pass

    def get_all(self) -> List[Product]:
        pass

    def create(self, product_in: Product) -> Product:
        pass

    def update(self, product_in: Product) -> Product:
        pass

    def remove(self, product_id: uuid.UUID) -> None:
        pass


product_repo = MockRepository()


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_product():
    return ProductHelper.generate_product_entity()


@pytest.fixture
def generate_updated_product():
    return ProductHelper.generate_updated_product_entity()


@pytest.fixture
def generate_multiple_products():
    return ProductHelper.generate_multiple_product_entities()


def test_should_allow_register_product(generate_new_product, unstub):
    product = generate_new_product

    when(product_repo).create(ANY(Product)).thenReturn(product)

    created_product = product_repo.create(product)

    verify(product_repo, times=1).create(product)

    assert type(created_product) == Product
    assert created_product is not None
    assert created_product == product
    assert product.product_id == created_product.product_id
    assert product.name == created_product.name
    assert product.description == created_product.description
    assert product.category == created_product.category
    assert product.price == created_product.price
    assert product.image_url == created_product.image_url


def test_should_allow_retrieve_product_by_id(generate_new_product, unstub):
    product = generate_new_product
    product_id = product.product_id

    when(product_repo).get_by_id(ANY(uuid.UUID)).thenReturn(product)

    retrieved_product = product_repo.get_by_id(product_id)

    verify(product_repo, times=1).get_by_id(product_id)

    assert product.product_id == retrieved_product.product_id
    assert product.name == retrieved_product.name
    assert product.description == retrieved_product.description
    assert product.category == retrieved_product.category
    assert product.price == retrieved_product.price
    assert product.image_url == retrieved_product.image_url


def test_should_allow_list_products(generate_multiple_products, unstub):
    products_list = generate_multiple_products

    when(product_repo).get_all().thenReturn(products_list)

    result = product_repo.get_all()

    verify(product_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(products_list)
    for product in products_list:
        assert product in result


def test_should_allow_list_products_by_category(generate_multiple_products, unstub):
    products_list = generate_multiple_products
    product_category = str(Category.SANDWICH.value)

    when(product_repo).get_all_by_category(ANY(str)).thenReturn(products_list)

    result = product_repo.get_all_by_category(product_category)

    verify(product_repo, times=1).get_all_by_category(product_category)

    assert type(result) == list
    assert len(result) == len(products_list)
    for product in products_list:
        assert product in result
        assert product.category == product_category


def test_should_allow_update_product(generate_new_product, generate_updated_product, unstub):
    product = generate_new_product
    product_id = product.product_id

    updated_product = generate_updated_product
    product.name = updated_product.name
    product.description = updated_product.description
    product.category = updated_product.category
    product.price = updated_product.price
    product.image_url = updated_product.image_url

    when(product_repo).update(ANY(Product)).thenReturn(product)

    created_product = product_repo.update(product)

    verify(product_repo, times=1).update(product)

    assert type(created_product) == Product
    assert created_product is not None
    assert created_product == product
    assert product.product_id == created_product.product_id
    assert product.name == created_product.name
    assert product.description == created_product.description
    assert product.category == created_product.category
    assert product.price == created_product.price
    assert product.image_url == created_product.image_url


def test_should_allow_remove_product(unstub):
    product_id = uuid.uuid4()

    when(product_repo).remove(ANY(uuid.UUID)).thenReturn()

    product_repo.remove(product_id)

    verify(product_repo, times=1).remove(product_id)


