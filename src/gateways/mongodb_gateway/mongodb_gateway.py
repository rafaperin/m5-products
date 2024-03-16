import uuid
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from src.entities.models.product_entity import product_factory, Product
from src.interfaces.gateways.product_gateway_interface import IProductGateway
from src.external.mongo_database import Product as ProductDB


class MongoDBProductRepository(IProductGateway):
    @staticmethod
    def to_entity(product: dict) -> Product:
        product = product_factory(
            product["product_id"],
            product["name"],
            product["description"],
            product["category"],
            product["price"],
            product["image_url"]
        )
        return product

    def get_by_id(self, product_id: uuid.UUID) -> Optional[Product]:
        result = ProductDB.find_one({'product_id': str(product_id)})

        if result:
            return self.to_entity(result)
        else:
            return None

    def get_all(self) -> List[Product]:
        products = []
        result = ProductDB.find()

        for product in result:
            products.append(self.to_entity(product))
        return products

    def get_all_by_category(self, category: str) -> List[Product]:
        products = []
        result = ProductDB.find({"category": category})

        for product in result:
            products.append(self.to_entity(product))
        return products

    def create(self, obj_in: Product) -> Product:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)

        new_product = ProductDB.insert_one(obj_in_data)
        product = ProductDB.find_one({'_id': new_product.inserted_id})
        result = self.to_entity(product)

        return result

    def update(self, obj_in: Product) -> Product:
        obj_data = jsonable_encoder(obj_in, by_alias=False)

        ProductDB.find_one_and_update({"product_id": obj_in.product_id}, {"$set": obj_data})
        result = ProductDB.find_one({"product_id": obj_in.product_id})

        updated_product = self.to_entity(result)
        return updated_product

    def remove(self, product_id: uuid.UUID) -> None:
        ProductDB.delete_one({"product_id": str(product_id)})
