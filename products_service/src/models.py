from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text) 
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    user_id = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)

    product_links = relationship("ProductPhoto", back_populates="photo")


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)

    product = relationship("Product", backref="photo_links")
    photo = relationship("Photo", back_populates="product_links")
