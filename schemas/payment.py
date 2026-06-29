from pydantic import BaseModel


class PaymentCreate(BaseModel):

    amount: float

    payment_method: str
