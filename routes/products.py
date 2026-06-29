from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.product import Product

from schemas.product import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    if product.price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Price must be greater than zero"
        )

    if product.stock < 0:

        raise HTTPException(
            status_code=400,
            detail="Stock cannot be negative"
        )

    existing = db.query(Product).filter(
        Product.name == product.name
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Product already exists"
        )

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        is_active=product.is_active
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return new_product


@router.get("/")
def get_products(
    category: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Product)

    if category:

        query = query.filter(
            Product.category == category
        )

    total = query.count()

    products = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": products
    }


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    db_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not db_product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock = product.stock
    db_product.category = product.category
    db_product.is_active = product.is_active

    db.commit()

    return {
        "message":
        "Product updated"
    }


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.is_active = False

    db.commit()

    return {
        "message":
        "Product deactivated"
    }
