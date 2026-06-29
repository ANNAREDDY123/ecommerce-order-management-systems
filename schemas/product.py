from pydantic import BaseModel


class ProductCreate(BaseModel):

    name: str

    description: str

    price: float

    stock: int

    category: str

    is_active: bool = True
