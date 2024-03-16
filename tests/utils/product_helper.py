from typing import List

from src.entities.models.product_entity import Product
from src.entities.schemas.product_dto import CreateProductDTO, ChangeProductDTO


class ProductHelper:

    @staticmethod
    def generate_product_request() -> CreateProductDTO:
        return CreateProductDTO(
            name="Bacon",
            description="Duas fatias de bacon",
            category="Acompanhamento",
            price=9.99,
            image_url=""
        )

    @staticmethod
    def generate_multiple_products() -> List[CreateProductDTO]:
        products_list = []
        product1 = CreateProductDTO(
            name="Bacon",
            description="Duas fatias de bacon",
            category="Acompanhamento",
            price=9.99,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )

        product2 = CreateProductDTO(
            name="Hamburguer gourmet",
            description="Lanche gourmet com refrigerante",
            category="Lanche",
            price=35.50,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )
        products_list.append(product1)
        products_list.append(product2)
        return products_list

    @staticmethod
    def generate_updated_product_data() -> ChangeProductDTO:
        return ChangeProductDTO(
            name="Hamburguer gourmet",
            description="Lanche gourmet sem refrigerante",
            category="Lanche",
            price=20.00,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )

    @staticmethod
    def generate_product_entity() -> Product:
        return Product.create(
            name="Hamburguer gourmet",
            description="Lanche gourmet com refrigerante",
            category="Lanche",
            price=35.50,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )

    @staticmethod
    def generate_updated_product_entity() -> Product:
        return Product.create(
            name="Hamburguer gourmet gostoso",
            description="Lanche gourmet sem refrigerante",
            category="Lanche",
            price=35.50,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )

    @staticmethod
    def generate_multiple_product_entities() -> List[Product]:
        products_list = []
        product1 = Product.create(
            name="Hamburguer gourmet",
            description="Lanche gourmet com refrigerante",
            category="Lanche",
            price=35.50,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )

        product2 = Product.create(
            name="Bacon",
            description="Duas fatias de bacon",
            category="Lanche",
            price=9.99,
            image_url="https://blog.letskuk.com.br/lanches-gourmet"
        )
        products_list.append(product1)
        products_list.append(product2)
        return products_list
