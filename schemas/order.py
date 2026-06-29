from pydantic import BaseModel


class OrderCreate(BaseModel):

    customer_id: int
