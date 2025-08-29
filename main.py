"""main.py
Interfaz de consola para gestionar el inventario.
"""
from models import Product, Inventory
import sys

def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Por favor ingrese un número entero válido.')

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Por favor ingrese un número decimal válido.')

def menu():
    inv = Inventory()
    try:
        while True:
            print('\n--- MENÚ INVENTARIO ---')
            print('1. Añadir producto')
            print('2. Eliminar producto por ID')
            print('3. Actualizar cantidad')
            print('4. Actualizar precio')
            print('5. Buscar productos por nombre')
            print('6. Mostrar todos los productos')
            print('7. Mostrar producto por ID')
            print('0. Salir')
            opc = input('Seleccione una opción: ').strip()

            if opc == '1':
                pid = input_int('ID (entero único): ')
                name = input('Nombre: ').strip()
                qty = input_int('Cantidad: ')
                price = input_float('Precio: ')
                prod = Product(id=pid, nombre=name, cantidad=qty, precio=price)
                ok = inv.add_product(prod)
                if ok:
                    print('Producto añadido correctamente.')
                else:
                    print('Error: ya existe un producto con ese ID.')

            elif opc == '2':
                pid = input_int('ID del producto a eliminar: ')
                ok = inv.remove_product_by_id(pid)
                if ok:
                    print('Producto eliminado.')
                else:
                    print('No existe producto con ese ID.')

            elif opc == '3':
                pid = input_int('ID del producto a actualizar cantidad: ')
                qty = input_int('Nueva cantidad: ')
                ok = inv.update_quantity(pid, qty)
                print('Cantidad actualizada.' if ok else 'Producto no encontrado.')

            elif opc == '4':
                pid = input_int('ID del producto a actualizar precio: ')
                price = input_float('Nuevo precio: ')
                ok = inv.update_price(pid, price)
                print('Precio actualizado.' if ok else 'Producto no encontrado.')

            elif opc == '5':
                q = input('Ingrese texto a buscar en el nombre: ').strip()
                results = inv.search_by_name(q)
                if not results:
                    print('No se encontraron productos.')
                else:
                    print(f'Se encontraron {len(results)} producto(s):')
                    for p in results:
                        print(f'ID:{p.id} | {p.nombre} | Cant:{p.cantidad} | Precio:{p.precio}')

            elif opc == '6':
                allp = inv.list_all()
                if not allp:
                    print('Inventario vacío.')
                else:
                    print(f'Total productos: {len(allp)}')
                    for p in allp:
                        print(f'ID:{p.id} | {p.nombre} | Cant:{p.cantidad} | Precio:{p.precio}')

            elif opc == '7':
                pid = input_int('ID del producto: ')
                p = inv.get_product(pid)
                if p:
                    print(f'ID:{p.id} | {p.nombre} | Cant:{p.cantidad} | Precio:{p.precio}')
                else:
                    print('Producto no encontrado.')

            elif opc == '0':
                print('Saliendo...')
                break
            else:
                print('Opción inválida. Intente de nuevo.')
    finally:
        inv.close()

if __name__ == '__main__':
    menu()
