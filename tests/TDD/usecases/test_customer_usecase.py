import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.config.errors import ResourceNotFound
from src.entities.models.product_entity import Product
from src.interfaces.gateways.product_gateway_interface import IProductGateway
from src.interfaces.use_cases.product_usecase_interface import ProductUseCaseInterface
from src.usecases.product_usecase import ProductUseCase
from tests.utils.product_helper import ProductHelper


class MockRepository(IProductGateway):
    def get_by_id(self, product_id: uuid.UUID) -> Product:
        pass

    def get_all_by_category(self, cpf: str) -> Product:
        pass

    def get_all(self) -> List[Product]:
        pass

    def create(self, product_in: Product) -> Product:
        pass

    def update(self, product_in: Product) -> Product:
        pass

    def remove(self, product_id: uuid.UUID) -> None:
        pass


class MockUsecase(ProductUseCaseInterface):
    pass


product_repo = MockRepository()
product_usecase = ProductUseCase(product_repo)


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_product():
    return ProductHelper.generate_product_entity()


@pytest.fixture
def generate_new_product_dto():
    return ProductHelper.generate_product_request()


@pytest.fixture
def generate_updated_product_dto():
    return ProductHelper.generate_updated_product_data()


@pytest.fixture
def generate_updated_product():
    return ProductHelper.generate_updated_product_entity()


@pytest.fixture
def generate_multiple_products():
    return ProductHelper.generate_multiple_product_entities()


def test_should_allow_register_product(generate_new_product_dto, unstub):
    product_dto = generate_new_product_dto
    product_entity = Product.create(
        name="Hamburguer gourmet",
        description="Lanche gourmet com refrigerante",
        category="Lanche",
        price=35.50,
        image_url="https://blog.letskuk.com.br/lanches-gourmet"
    )

    when(product_repo).create(ANY(Product)).thenReturn(product_entity)

    created_product = product_usecase.create(product_dto)

    assert created_product is not None
    assert product_dto.name == created_product.name
    assert product_dto.description == created_product.description
    assert product_dto.category == created_product.category
    assert product_dto.price == created_product.price
    assert product_dto.image_url == created_product.image_url


def test_should_allow_retrieve_product_by_id(generate_new_product_dto, unstub):
    product = generate_new_product_dto
    product_id = uuid.uuid4()

    when(product_repo).get_by_id(ANY(uuid.UUID)).thenReturn(product)

    retrieved_product = product_usecase.get_by_id(product_id)

    verify(product_repo, times=1).get_by_id(product_id)

    assert product.name == retrieved_product.name
    assert product.description == retrieved_product.description
    assert product.category == retrieved_product.category
    assert product.price == retrieved_product.price
    assert product.image_url == retrieved_product.image_url


def test_should_raise_exception_invalid_id(unstub):
    product_id = uuid.uuid4()

    when(product_repo).get_by_id(ANY(uuid.UUID)).thenReturn()

    try:
        product_usecase.get_by_id(product_id)
        assert False
    except ResourceNotFound:
        assert True

    verify(product_repo, times=1).get_by_id(product_id)


def test_should_raise_exception_invalid_category(unstub):
    product_category = "Invalid"

    when(product_repo).get_all_by_category(ANY(str)).thenReturn()

    try:
        product_usecase.get_all_by_category(product_category)
        assert False
    except Exception:
        assert True

    verify(product_repo, times=1).get_all_by_category(product_category)


def test_should_allow_retrieve_all_products_by_category(generate_new_product_dto, unstub):
    product = generate_new_product_dto
    product_category = product.category

    when(product_repo).get_all_by_category(ANY(str)).thenReturn(product)

    retrieved_product = product_usecase.get_all_by_category(product_category)

    verify(product_repo, times=1).get_all_by_category(product_category)

    assert product.name == retrieved_product.name
    assert product.description == retrieved_product.description
    assert product.category == retrieved_product.category
    assert product.price == retrieved_product.price
    assert product.image_url == retrieved_product.image_url


def test_should_allow_update_product(generate_new_product, generate_updated_product_dto, generate_updated_product, unstub):
    old_product = generate_new_product
    old_product_id = old_product.product_id
    new_product_data = generate_updated_product_dto

    old_product.name = new_product_data.name
    old_product.description = new_product_data.description
    old_product.category = new_product_data.category
    old_product.price = new_product_data.price
    old_product.image_url = new_product_data.image_url

    when(product_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_product)
    when(product_repo).update(ANY(Product)).thenReturn(old_product)

    updated_product = product_usecase.update(old_product_id, new_product_data)

    assert updated_product is not None
    assert updated_product.name == old_product.name
    assert updated_product.description == old_product.description
    assert updated_product.category == old_product.category
    assert updated_product.price == old_product.price
    assert updated_product.image_url == old_product.image_url


def test_should_allow_list_products(generate_multiple_products, unstub):
    products_list = generate_multiple_products

    when(product_repo).get_all().thenReturn(products_list)

    result = product_usecase.get_all()

    verify(product_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(products_list)
    for product in products_list:
        assert product in result


def test_should_allow_list_empty_products(generate_multiple_products, unstub):
    when(product_repo).get_all().thenReturn(list())

    result = product_usecase.get_all()

    assert result == list()
    verify(product_repo, times=1).get_all()


def test_should_allow_remove_product(unstub):
    product_id = uuid.uuid4()

    when(product_repo).remove(ANY(uuid.UUID)).thenReturn()

    product_usecase.remove(product_id)

    verify(product_repo, times=1).remove(product_id)
