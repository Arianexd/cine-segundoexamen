from pydantic import BaseModel

class ClienteCreate(BaseModel):
    nombre: str
    correo: str
    telefono: str

class PeliculaCreate(BaseModel):
    titulo: str
    duracion: int
    genero: str

class SalaCreate(BaseModel):
    nombre: str
    capacidad: int

class FuncionCreate(BaseModel):
    id_pelicula: int
    id_sala: int
    horario: str
    precio: float
    asientos_disponibles: int

class ReservaCreate(BaseModel):
    id_cliente: int
    id_funcion: int
    cantidad_asientos: int

class PagoCreate(BaseModel):
    id_reserva: int
    metodo_pago: str
    estado: str

class ResenaCreate(BaseModel):
    id_cliente: int
    id_pelicula: int
    calificacion: int
    comentario: str