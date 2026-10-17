from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
from sqlalchemy.exc import IntegrityError

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Cine Premium - Arquitectura Modular")

# ENDPOINTS - POST 

@app.post("/clientes/", status_code=201)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.ClienteDB(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.post("/peliculas/", status_code=201)
def crear_pelicula(pelicula: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    db_pelicula = models.PeliculaDB(**pelicula.dict())
    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

@app.post("/salas/", status_code=201)
def crear_sala(sala: schemas.SalaCreate, db: Session = Depends(get_db)):
    db_sala = models.SalaDB(**sala.dict())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala

@app.post("/funciones/", status_code=201)
def crear_funcion(funcion: schemas.FuncionCreate, db: Session = Depends(get_db)):
    db_funcion = models.FuncionDB(**funcion.dict())
    db.add(db_funcion)
    db.commit()
    db.refresh(db_funcion)
    return db_funcion

@app.post("/pagos/", status_code=201)
def registrar_pago(pago: schemas.PagoCreate, db: Session = Depends(get_db)):
    db_pago = models.PagoDB(**pago.dict())
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    return db_pago

@app.post("/resenas/", status_code=201)
def crear_resena(resena: schemas.ResenaCreate, db: Session = Depends(get_db)):
    db_resena = models.ResenaDB(**resena.dict())
    db.add(db_resena)
    db.commit()
    db.refresh(db_resena)
    return db_resena


@app.post("/reservas/", status_code=201)
def crear_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    funcion = db.query(models.FuncionDB).filter(models.FuncionDB.id == reserva.id_funcion).first()
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    
    if funcion.asientos_disponibles < reserva.cantidad_asientos:
        raise HTTPException(status_code=400, detail="Asientos insuficientes")
    
    total = funcion.precio * reserva.cantidad_asientos
    funcion.asientos_disponibles -= reserva.cantidad_asientos
    
    nueva_reserva = models.ReservaDB(
        id_cliente=reserva.id_cliente,
        id_funcion=reserva.id_funcion,
        cantidad_asientos=reserva.cantidad_asientos,
        total_pagar=total
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

# ENDPOINTS - GET 

@app.get("/peliculas/")
def listar_peliculas(db: Session = Depends(get_db)):
    return db.query(models.PeliculaDB).all()

@app.get("/peliculas/{pelicula_id}")
def obtener_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.PeliculaDB).filter(models.PeliculaDB.id == pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

@app.get("/reservas/")
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(models.ReservaDB).all()

# ENDPOINTS - PUT 

@app.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: int, cliente_actualizado: schemas.ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    cliente.nombre = cliente_actualizado.nombre
    cliente.correo = cliente_actualizado.correo
    cliente.telefono = cliente_actualizado.telefono
    
    db.commit()
    db.refresh(cliente)
    return cliente

# ENDPOINTS - DELETE 

@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(models.ReservaDB).filter(models.ReservaDB.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    funcion = db.query(models.FuncionDB).filter(models.FuncionDB.id == reserva.id_funcion).first()
    if funcion:
        funcion.asientos_disponibles += reserva.cantidad_asientos
        
    db.delete(reserva)
    db.commit()
    return {"mensaje": "Reserva cancelada exitosamente y asientos devueltos"}
@app.get("/clientes/")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.ClienteDB).all()

@app.get("/salas/")
def listar_salas(db: Session = Depends(get_db)):
    return db.query(models.SalaDB).all()

@app.get("/funciones/")
def listar_funciones(db: Session = Depends(get_db)):
    return db.query(models.FuncionDB).all()

@app.get("/pagos/")
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(models.PagoDB).all()

@app.get("/resenas/")
def listar_resenas(db: Session = Depends(get_db)):
    return db.query(models.ResenaDB).all()

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    try:
        db.delete(cliente)
        db.commit()
        return {"mensaje": "Cliente eliminado exitosamente"}
    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=400, detail="No se puede eliminar: el cliente tiene reservas o reseñas asociadas.")

@app.delete("/peliculas/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.PeliculaDB).filter(models.PeliculaDB.id == pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    try:
        db.delete(pelicula)
        db.commit()
        return {"mensaje": "Película eliminada exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se puede eliminar: la película tiene funciones programadas.")