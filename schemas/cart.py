from pydantic import BaseModel


class CartCreate(BaseModel):

    user_id: int

    product_id: int

    quantity: int
