import pytest

from api_v1.products import crud
from api_v1.products.schemas import ProductCreate, ProductUpdate
from core.models import Product


@pytest.mark.asyncio
async def test_create_and_get_product(async_session):
    product_in = ProductCreate(name="Test", description="Desc", price=100)
    created = await crud.create_product(session=async_session, product_in=product_in)

    assert isinstance(created, Product)
    assert created.name == "Test2"

    fetched = await crud.get_product(session=async_session, product_id=created.id)
    assert fetched is not None
    assert fetched.id == created.id


@pytest.mark.asyncio
async def test_update_product(async_session):
    # create
    product_in = ProductCreate(name="ToUpdate", description="Desc", price=50)
    created = await crud.create_product(session=async_session, product_in=product_in)

    # update
    update_in = ProductUpdate(name="Updated", description="New", price=75)
    updated = await crud.update_product(
        session=async_session, product=created, product_update=update_in
    )

    assert updated.name == "Updated"
    assert updated.price == 75


@pytest.mark.asyncio
async def test_delete_product(async_session):
    product_in = ProductCreate(name="ToDelete", description="Desc", price=20)
    created = await crud.create_product(session=async_session, product_in=product_in)

    await crud.delete_product(session=async_session, product=created)

    fetched = await crud.get_product(session=async_session, product_id=created.id)
    assert fetched is None
