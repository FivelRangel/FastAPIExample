from fastapi import FastAPI
import aiomysql

app = FastAPI()

# Credenciales de la base de datos obtenidas desde Railway
DATABASE_CONFIG = {
    "host": "viaduct.proxy.rlwy.net",
    "port": 56533,
    "user": "root",
    "password": "gCGB-CeCch3CDG5Cc262GB1h4HHbGedB",
    "db": "railway",
}

# Función para conectar a la base de datos
async def connect_to_db():
    return await aiomysql.connect(
        host=DATABASE_CONFIG["host"],
        port=DATABASE_CONFIG["port"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        db=DATABASE_CONFIG["db"],
    )

# Middleware para conectar a la base de datos antes de procesar la solicitud
@app.on_event("startup")
async def startup():
    app.state.pool = await connect_to_db()

# Middleware para cerrar la conexión a la base de datos después de procesar la solicitud
@app.on_event("shutdown")
async def shutdown():
    app.state.pool.close()
    await app.state.pool.wait_closed()

# Ruta para realizar consultas a la base de datos
@app.get("/custom/{item_id}")
async def read_custom_item(item_id: int):
    async with app.state.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM custom WHERE id = %s", (item_id,))
            row = await cursor.fetchone()
            if row:
                # Ajusta aquí los campos según tu tabla 'custom'
                return {"item_id": row[0], "item_name": row[1]}  # Ejemplo: ID y nombre
            return {"message": "Item not found"}
