from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class ClienteDB(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    telefono = Column(String)

class PeliculaDB(Base):
    __tablename__ = "peliculas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    duracion = Column(Integer)
    genero = Column(String)

class SalaDB(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    capacidad = Column(Integer)

class FuncionDB(Base):
    __tablename__ = "funciones"
    id = Column(Integer, primary_key=True, index=True)
    id_pelicula = Column(Integer, ForeignKey("peliculas.id"))
    id_sala = Column(Integer, ForeignKey("salas.id"))
    horario = Column(String)
    precio = Column(Float)
    asientos_disponibles = Column(Integer)

class ReservaDB(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    id_funcion = Column(Integer, ForeignKey("funciones.id"))
    cantidad_asientos = Column(Integer)
    total_pagar = Column(Float)

class PagoDB(Base):
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True, index=True)
    id_reserva = Column(Integer, ForeignKey("reservas.id"))
    metodo_pago = Column(String) # QR, Tarjeta, Efectivo
    estado = Column(String) # Pagado, Pendiente

class ResenaDB(Base):
    __tablename__ = "resenas"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    id_pelicula = Column(Integer, ForeignKey("peliculas.id"))
    calificacion = Column(Integer) # 1 a 5
    comentario = Column(String)