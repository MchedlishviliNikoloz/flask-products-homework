from database import db
from sqlalchemy.orm import Mapped, mapped_column

class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }