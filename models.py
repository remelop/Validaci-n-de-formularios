"""models.py
Contiene las clases Product e Inventory.
Inventory mantiene un diccionario interno para acceso rápido y sincroniza con SQLite.
"""
from dataclasses import dataclass, asdict
import sqlite3
from typing import Dict, List, Optional

@dataclass
class Product:
    id: int
    nombre: str
    cantidad: int
    precio: float

    def to_dict(self):
        return asdict(self)

class Inventory:
    def __init__(self, db_path: str = 'inventory.db'):
        self.db_path = db_path
        # Diccionario: clave=id, valor=Product
        self._products: Dict[int, Product] = {}
        self._connect_db()
        self._ensure_table()
        self._load_from_db()

    def _connect_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def _ensure_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def _load_from_db(self):
        self.cursor.execute('SELECT id, nombre, cantidad, precio FROM products')
        rows = self.cursor.fetchall()
        for r in rows:
            p = Product(id=r['id'], nombre=r['nombre'], cantidad=r['cantidad'], precio=r['precio'])
            self._products[p.id] = p

    # ---------- Operaciones en memoria + DB ----------
    def add_product(self, product: Product) -> bool:
        """Añade un producto. Retorna True si se añadió, False si ya existía el id."""
        if product.id in self._products:
            return False
        self._products[product.id] = product
        self._insert_db(product)
        return True

    def _insert_db(self, product: Product):
        self.cursor.execute(
            'INSERT INTO products(id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)',
            (product.id, product.nombre, product.cantidad, product.precio)
        )
        self.conn.commit()

    def remove_product_by_id(self, product_id: int) -> bool:
        """Elimina un producto por id. Retorna True si se eliminó, False si no existe."""
        if product_id not in self._products:
            return False
        del self._products[product_id]
        self.cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        self.conn.commit()
        return True

    def update_quantity(self, product_id: int, cantidad: int) -> bool:
        """Actualiza la cantidad de un producto. Retorna True si OK."""
        p = self._products.get(product_id)
        if not p:
            return False
        p.cantidad = cantidad
        self.cursor.execute('UPDATE products SET cantidad = ? WHERE id = ?', (cantidad, product_id))
        self.conn.commit()
        return True

    def update_price(self, product_id: int, precio: float) -> bool:
        """Actualiza el precio de un producto. Retorna True si OK."""
        p = self._products.get(product_id)
        if not p:
            return False
        p.precio = precio
        self.cursor.execute('UPDATE products SET precio = ? WHERE id = ?', (precio, product_id))
        self.conn.commit()
        return True

    def search_by_name(self, nombre_substr: str) -> List[Product]:
        """Busca productos que contengan la cadena en su nombre (case-insensitive)."""
        q = nombre_substr.lower()
        return [p for p in self._products.values() if q in p.nombre.lower()]

    def list_all(self) -> List[Product]:
        """Retorna todos los productos como lista."""
        return list(self._products.values())

    def get_product(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def close(self):
        self.conn.close()
