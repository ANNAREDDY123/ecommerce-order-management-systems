from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.order import Order
from models.cart import Cart
from models.product import Product

from schemas.order import OrderCreate

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    cart_items = db.query(Cart).filter(
        Cart.user_id == order.customer_id
    ).all()

    if not cart_items:

        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = 0

    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product.stock < item.quantity:

            raise HTTPException(
                status_code=400,
                detail="Out of stock"
            )

        total += product.price * item.quantity

        product.stock -= item.quantity

    new_order = Order(
        customer_id=order.customer_id,
        total_amount=total,
        order_status="Confirmed"
    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    return new_order


@router.get("/")
def get_orders(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Order)

    if status:

        query = query.filter(
            Order.order_status == status
        )

    total = query.count()

    orders = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": orders
    }


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order
