from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.cart import Cart
from models.product import Product

from schemas.cart import CartCreate

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/add")
def add_to_cart(
    cart: CartCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == cart.product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if not product.is_active:

        raise HTTPException(
            status_code=400,
            detail="Inactive product"
        )

    if cart.quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    if cart.quantity > product.stock:

        raise HTTPException(
            status_code=400,
            detail="Quantity exceeds stock"
        )

    item = Cart(
        user_id=cart.user_id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )

    db.add(item)

    db.commit()

    return {
        "message":
        "Product added to cart"
    }


@router.get("/")
def get_cart(
    db: Session = Depends(get_db)
):

    return db.query(Cart).all()


@router.delete("/remove/{product_id}")
def remove_cart(
    product_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(Cart).filter(
        Cart.product_id == product_id
    ).first()

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item)

    db.commit()

    return {
        "message":
        "Item removed"
    }
