from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.payment import Payment
from models.order import Order

from schemas.payment import PaymentCreate

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/{order_id}")
def make_payment(
    order_id: int,
    payment: PaymentCreate,
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

    existing = db.query(Payment).filter(
        Payment.order_id == order_id
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Payment already exists"
        )

    if payment.amount != order.total_amount:

        raise HTTPException(
            status_code=400,
            detail="Amount mismatch"
        )

    new_payment = Payment(
        order_id=order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        payment_status="Success"
    )

    db.add(new_payment)

    db.commit()

    db.refresh(new_payment)

    return new_payment


@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment
