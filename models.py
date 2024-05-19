from sqlalchemy import String, Integer, Column, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Productos(Base):
    __tablename__="productos"

    idproducto = Column(Integer, primary_key=True, index=True)
    codigoproducto = Column(String(100))
    marca = Column(String(100))
    codigo = Column(String(100))
    nombre = Column(String(100))
    categoria = Column(String(100))
    precio = Column(Float)

class OrdenCompra(Base):
    __tablename__="ordencompra"

    idorden = Column(Integer, primary_key=True, index=True)
    producto_id = Column(String(100))
    nombre_cliente = Column(String(100))
    cantidad_productos = Column(Integer)
    total = Column(Float)

    # Relación con Producto
    #producto_id = Column(Integer, ForeignKey('productos.idproducto'))
    #producto = relationship("Producto", back_populates="ordencompra")