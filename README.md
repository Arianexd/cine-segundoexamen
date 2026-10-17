# Sistema de Gestión de Cine - Backend & API Gateway

Backend modularizado bajo arquitectura de microservicios para la administración de salas, funciones y reservas de cine. Desarrollado con FastAPI, PostgreSQL, Nginx y Docker Compose.

---

## 🛠️ Tecnologías Empleadas

* **Lenguaje:** Python 3.11
* **Framework:** FastAPI
* **ORM & Modelado:** SQLAlchemy, Pydantic
* **Base de Datos:** PostgreSQL 15
* **Proxy Inverso:** Nginx (Alpine)
* **Contenedores:** Docker & Docker Compose
* **Control de Versiones:** Git Flow (`main` / `develop`)

---

## 🏛️ Estructura del Proyecto

```text
cine-segundoexamen/
├── docker-compose.yml
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
└── gateway/
    ├── Dockerfile
    └── nginx.conf

## Esquema de Base de Datos 
clientes: Datos personales y contacto (id, nombre, correo, telefono).

peliculas: Catálogo de películas (id, titulo, duracion, genero).

salas: Salas físicas del complejo y capacidad (id, nombre, capacidad).

funciones: Horarios y precios asociados a una película y sala (id, id_pelicula, id_sala, horario, precio, asientos_disponibles).

reservas: Transacción de boletos adquiridos (id, id_cliente, id_funcion, cantidad_asientos, total).

pagos: Registro financiero de la reserva (id, id_reserva, metodo_pago, estado).

resenas: Calificaciones y opiniones de los usuarios (id, id_cliente, id_pelicula, calificacion, comentario).

## Instrucciones de Ejecución
1. Levantar los Contenedores

docker compose up -d --build

2. Verificar Estado
Comprobar que los tres servicios se encuentren en estado Up:

docker ps

Gateway: Puerto 80 (expuesto)
API: Puerto 8000 (red interna)
DB: Puerto 5432 (red interna con healthcheck)

3. Acceso a Documentación Interactiva
Abrir en el navegador:

Swagger UI: http://localhost/docs
ReDoc: http://localhost/redoc

## Detener el Sistema

docker compose down