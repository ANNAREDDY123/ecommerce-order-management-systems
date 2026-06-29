from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    total_amount = Column(Float)

    order_status = Column(
        String,
        default="Pending"
    )
