import uuid
from typing import Optional, List

from src.utils.utils import CamelModel


class ProductDTO(CamelModel):
    product_id: uuid.UUID
    name: str
    description: Optional[str]
    category: str
    price: float
    image_url: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "product_id": "00000000-0000-0000-0000-000000000000",
                "name": "Lanche 1",
                "description": "Lanche daora",
                "category": "Lanche",
                "price": "9.99",
                "image_url": "https://blog.letskuk.com.br/lanches-gourmet"
            }
        }


class CreateProductDTO(CamelModel):
    name: str
    description: Optional[str]
    category: str
    price: float
    image_url: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Lanche 1",
                "description": "Lanche daora",
                "category": "Lanche",
                "price": "9.99",
                "image_url": "https://blog.letskuk.com.br/lanches-gourmet"
            }
        }


class ChangeProductDTO(CamelModel):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    image_url: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Lanche 1",
                "description": "Lanche daora",
                "category": "Lanche",
                "price": "9.99",
                "image_url": "https://blog.letskuk.com.br/lanches-gourmet"
            }
        }


class ProductDTOResponse(CamelModel):
    result: ProductDTO


class ProductDTOListResponse(CamelModel):
    result: List[ProductDTO]
