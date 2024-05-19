from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import Session

app = FastAPI()

class RegistrarOrden(BaseModel):
    producto_id: str
    nombre_cliente: str
    cantidad_productos: int
    total: float

class InteractuarOrden(BaseModel):
    idorden: int
    producto_id: str
    nombre_cliente: str
    cantidad_productos: int
    total: float

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#crear orden
@app.post("/registroorden/", tags=['Ordenes'], status_code=status.HTTP_201_CREATED)
async def crear_orden(registro:RegistrarOrden, db:db_dependency):
    db_orden = models.OrdenCompra(**registro.dict())
    db.add(db_orden)
    db.commit()
    return "La orden fue creada existosamente"

#listar ordenes
@app.get("/listarordenes/", tags=['Ordenes'], status_code=status.HTTP_200_OK)
async def listar_ordenes(db:db_dependency):
    registros = db.query(models.OrdenCompra).all()
    return registros

#consultar orden por id
@app.get("/consultarorden/{id_orden}", tags=['Ordenes'], status_code=status.HTTP_200_OK)
async def consultar_orden_por_id(id_orden, db:db_dependency):
    registro = db.query(models.OrdenCompra).filter(models.OrdenCompra.idorden==id_orden).first()
    if registro is None:
        HTTPException(status_code=404, detail="Orden no encontrado")
    return registro

#borrar una orden
@app.delete("/borrarorden/{id_orden}", tags=['Ordenes'], status_code=status.HTTP_200_OK)
async def eliminar_producto(id_orden, db:db_dependency):
    orden_eliminada = db.query(models.OrdenCompra).filter(models.OrdenCompra.idorden==id_orden).first()
    if orden_eliminada is None:
        HTTPException(status_code=404, detail="No se puede borrar la orden o no existe")
    db.delete(orden_eliminada)
    db.commit()
    return "Orden borrado exitosamente"

#actualizar orden
@app.post("/actualizarorden/", tags=['Ordenes'], status_code=status.HTTP_200_OK)
async def update_orden(orden:InteractuarOrden, db:db_dependency):
    actualizar_orden = db.query(models.OrdenCompra).filter(models.OrdenCompra.idorden==orden.idorden).first()
    if actualizar_orden is None:
        HTTPException(status_code=404, detail="No se encontro la orden de compra")
        return "No se encontro la orden de compra"
    actualizar_orden.id_producto = orden.producto_id
    actualizar_orden.nombre_cliente = orden.nombre_cliente
    actualizar_orden.cantidad_productos = orden.cantidad_productos
    actualizar_orden.total = orden.total
    db.commit()
    return "La orden de compra se actualizo exitosamente"