from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column,relationship
# from .order_product_association import order_product_association_table
from .base import Base


if TYPE_CHECKING:
    from .order import Order
    from .order_product_association import OrderProductAssociation

class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    orders:Mapped[list["Order"]] = relationship(secondary="order_product_association",back_populates='products') 
    orders_details:Mapped[list["OrderProductAssociation"]] = relationship(back_populates='product')
