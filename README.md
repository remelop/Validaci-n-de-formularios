# Inventario en Python (POO + SQLite)

Proyecto entregable que implementa:
- Clase `Product` con atributos: id, nombre, cantidad, precio.
- Clase `Inventory` que usa un diccionario interno para búsquedas rápidas y sincroniza con SQLite.
- Interfaz de consola interactiva (`main.py`) para añadir, eliminar, actualizar, buscar y listar productos.
- Base de datos SQLite (`inventory.db`) creada automáticamente en la primera ejecución.

## Estructura del proyecto
- models.py         -> Contiene las clases Product e Inventory (lógica y persistencia SQLite).
- main.py           -> Menú interactivo por consola.
- requirements.txt  -> Dependencias (vacío; solo stdlib).
- .gitignore        -> Ignora la base de datos y __pycache__.
- README.md         -> Este archivo.

## Cómo ejecutar
1. Clona el repositorio o descarga el ZIP y descomprímelo.
2. Abre una terminal en la carpeta `inventory_app`.
3. (Opcional) Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate    # linux/mac
   venv\Scripts\activate     # windows
   ```
4. Ejecuta:
   ```bash
   python main.py
   ```

## Cómo usa colecciones y SQLite
- Se utiliza un **diccionario** (`self._products`) en `Inventory` donde la clave es el `id` del producto. Esto permite operaciones de lectura, actualización y borrado en **O(1)** promedio por id.
- Para búsquedas por nombre se itera sobre los valores del diccionario (se puede mejorar con índices o una estructura invertida si la colección crece mucho).
- La base de datos SQLite (`products` table) actúa como persistencia. Al inicializar, `Inventory` carga en memoria los productos desde SQLite y mantiene sincronización inmediata (cada cambio en memoria es también actualizado en la DB) para garantizar consistencia simple.

## Notas
- El proyecto está escrito para Python 3.8+ y solo usa la librería estándar (`sqlite3`).
- El archivo `inventory.db` será creado automaticamente en la carpeta del proyecto la primera vez que ejecute el programa.
