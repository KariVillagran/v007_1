from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import Session

app = FastAPI()

class RegistroProducto(BaseModel):
    codigoproducto: str
    marca: str
    codigo: str
    nombre: str
    categoria: str
    precio: float

class InteractuarProducto(BaseModel):
    idproducto: int
    codigoproducto: str
    marca: str
    codigo: str
    nombre: str
    categoria: str
    precio: float

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#crear producto
@app.post("/registroproducto/", tags=['Productos'], status_code=status.HTTP_201_CREATED)
async def crear_producto(registro:RegistroProducto, db:db_dependency):
    db_producto = models.Productos(**registro.dict())
    db.add(db_producto)
    db.commit()
    return "El producto fue creado existosamente"

#listar productos
@app.get("/listarproductos/", tags=['Productos'], status_code=status.HTTP_200_OK)
async def listar_productos(db:db_dependency):
    registros = db.query(models.Productos).all()
    return registros

#consultar producto por codigo
@app.get("/consultarproducto/{codigo_producto}", tags=['Productos'], status_code=status.HTTP_200_OK)
async def consultar_productos_por_codigo(codigo_producto, db:db_dependency):
    registro = db.query(models.Productos).filter(models.Productos.codigoproducto==codigo_producto).first()
    if registro is None:
        HTTPException(status_code=404, detail="Producto no encontrado")
    return registro

#borrar un producto
@app.delete("/borrarproducto/{id_producto}", tags=['Productos'], status_code=status.HTTP_200_OK)
async def eliminar_producto(id_producto, db:db_dependency):
    producto_eliminado = db.query(models.Productos).filter(models.Productos.idproducto==id_producto).first()
    if producto_eliminado is None:
        HTTPException(status_code=404, detail="No se puede borrar el producto o no existe")
    db.delete(producto_eliminado)
    db.commit()
    return "Producto borrado exitosamente"

#actualizar producto
@app.post("/actualizarproducto/", tags=['Productos'], status_code=status.HTTP_200_OK)
async def update_producto(producto:InteractuarProducto, db:db_dependency):
    actualizar_producto = db.query(models.Productos).filter(models.Productos.idproducto==producto.idproducto).first()
    if actualizar_producto is None:
        HTTPException(status_code=404, detail="No se encontro el producto")
        return "No se encontro el producto"
    actualizar_producto.codigoproducto = producto.codigoproducto
    actualizar_producto.marca = producto.marca
    actualizar_producto.codigo = producto.codigo
    actualizar_producto.nombre = producto.nombre
    actualizar_producto.precio = producto.precio
    actualizar_producto.categoria = producto.categoria
    db.commit()
    return "El producto se actualizo exitosamente"



