from flask import Flask, request, jsonify
from app import app
from config import get_db_connection
from datetime import datetime


@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_producto, p.nombre, p.precio_minorista, p.precio_mayorista, p.descripcion, f.nombre_familia 
            FROM app_producto p 
            JOIN app_familiaproducto f ON p.familia_id = f.id_familia
        """)
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/producto', methods=['POST'])
def create_producto():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO app_producto (nombre, precio, descripcion, familia_id)
            VALUES (?, ?, ?, ?)
        """, (data['nombre'], data['precio'], data.get('descripcion', ''), data['familia_id']))
        conn.commit()
        return jsonify({'message': 'Producto creado correctamente'}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/stock', methods=['GET'])
def get_stock():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.nombre_local, p.nombre, s.cantidad
            FROM app_stock s
            JOIN app_producto p ON s.producto_id = p.id_producto
            JOIN app_local l ON s.local_id = l.id_local
        """)
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/stock/agregar', methods=['POST'])
def agregar_o_actualizar_stock():
    try:
        data = request.json
        producto_id = data['producto_id']
        local_id = data['local_id']
        cantidad = int(data['cantidad'])

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el producto existe
        cursor.execute("SELECT 1 FROM app_producto WHERE id_producto = ?", (producto_id,))
        if not cursor.fetchone():
            return jsonify({'error': f'Producto con id {producto_id} no existe'}), 400

        # Verificar si el local existe
        cursor.execute("SELECT 1 FROM app_local WHERE id_local = ?", (local_id,))
        if not cursor.fetchone():
            return jsonify({'error': f'Local con id {local_id} no existe'}), 400

        # Verificar si ya hay stock para esa combinación
        cursor.execute("""
            SELECT cantidad FROM app_stock
            WHERE producto_id = ? AND local_id = ?
        """, (producto_id, local_id))
        resultado = cursor.fetchone()

        if resultado:
            nueva_cantidad = resultado['cantidad'] + cantidad
            cursor.execute("""
                UPDATE app_stock
                SET cantidad = ?
                WHERE producto_id = ? AND local_id = ?
            """, (nueva_cantidad, producto_id, local_id))
            mensaje = f'Stock actualizado. Nueva cantidad: {nueva_cantidad}.'
        else:
            cursor.execute("""
                INSERT INTO app_stock (producto_id, local_id, cantidad)
                VALUES (?, ?, ?)
            """, (producto_id, local_id, cantidad))
            mensaje = 'Stock agregado correctamente.'

        conn.commit()
        return jsonify({'message': mensaje}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/stock/reducir', methods=['POST'])
def reducir_stock():
    try:
        data = request.json
        producto_id = data['producto_id']
        local_id = data['local_id']
        cantidad = int(data['cantidad'])

        if cantidad <= 0:
            return jsonify({'error': 'La cantidad a reducir debe ser mayor que cero'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar existencia del producto
        cursor.execute("SELECT 1 FROM app_producto WHERE id_producto = ?", (producto_id,))
        if not cursor.fetchone():
            return jsonify({'error': f'Producto con id {producto_id} no existe'}), 400

        # Verificar existencia del local
        cursor.execute("SELECT 1 FROM app_local WHERE id_local = ?", (local_id,))
        if not cursor.fetchone():
            return jsonify({'error': f'Local con id {local_id} no existe'}), 400

        # Verificar existencia del stock
        cursor.execute("""
            SELECT cantidad FROM app_stock
            WHERE producto_id = ? AND local_id = ?
        """, (producto_id, local_id))
        resultado = cursor.fetchone()

        if not resultado:
            return jsonify({'error': 'No hay stock registrado para este producto en este local'}), 404

        cantidad_actual = resultado['cantidad']
        if cantidad_actual < cantidad:
            return jsonify({'error': f'Stock insuficiente. Solo hay {cantidad_actual} unidades disponibles'}), 400

        nueva_cantidad = cantidad_actual - cantidad
        cursor.execute("""
            UPDATE app_stock
            SET cantidad = ?
            WHERE producto_id = ? AND local_id = ?
        """, (nueva_cantidad, producto_id, local_id))

        conn.commit()
        return jsonify({'message': f'Stock reducido. Nueva cantidad: {nueva_cantidad}'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODOS PARA Consultar Stock / control stock
@app.route('/stock/producto/<int:producto_id>', methods=['GET'])
def consultar_stock_producto(producto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.nombre AS producto, p.stock_minimo, l.nombre_local, s.cantidad
            FROM app_stock s
            JOIN app_producto p ON s.producto_id = p.id_producto
            JOIN app_local l ON s.local_id = l.id_local
            WHERE p.id_producto = ?
        """, (producto_id,))
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'message': 'No se encontró stock para este producto'}), 404

        data = []
        for row in rows:
            alerta = row["cantidad"] < row["stock_minimo"]
            data.append({
                "producto": row["producto"],
                "local": row["nombre_local"],
                "cantidad": row["cantidad"],
                "stock_minimo": row["stock_minimo"],
                "alerta": alerta
            })

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODO PARA Consultar productos B2C
@app.route('/producto/b2c/<int:producto_id>', methods=['GET'])
def obtener_producto_por_id_b2c(producto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener datos del producto
        cursor.execute("""
            SELECT p.id_producto, p.nombre, p.precio_minorista, p.descripcion, 
                    p.stock_minimo, f.nombre_familia
            FROM app_producto p
            JOIN app_familiaproducto f ON p.familia_id = f.id_familia
            WHERE p.id_producto = ?
        """, (producto_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({'message': f'Producto con id {producto_id} no encontrado'}), 404
        data = dict(row)

        # Obtener stock por local (aunque sea 0)
        cursor.execute("""
            SELECT l.nombre_local, COALESCE(s.cantidad, 0) AS cantidad
            FROM app_local l
            LEFT JOIN app_stock s ON l.id_local = s.local_id AND s.producto_id = ?
        """, (producto_id,))
        stock_rows = cursor.fetchall()
        data['stock_por_local'] = [dict(stock) for stock in stock_rows]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODO PARA Consultar productos B2B
@app.route('/producto/b2b/<int:producto_id>', methods=['GET'])
def obtener_producto_por_id_b2b(producto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener datos del producto
        cursor.execute("""
            SELECT p.id_producto, p.nombre, p.precio_mayorista, p.descripcion, 
                    p.stock_minimo, f.nombre_familia
            FROM app_producto p
            JOIN app_familiaproducto f ON p.familia_id = f.id_familia
            WHERE p.id_producto = ?
        """, (producto_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({'message': f'Producto con id {producto_id} no encontrado'}), 404
        data = dict(row)

        # Obtener stock por local (aunque sea 0)
        cursor.execute("""
            SELECT l.nombre_local, COALESCE(s.cantidad, 0) AS cantidad
            FROM app_local l
            LEFT JOIN app_stock s ON l.id_local = s.local_id AND s.producto_id = ?
        """, (producto_id,))
        stock_rows = cursor.fetchall()
        data['stock_por_local'] = [dict(stock) for stock in stock_rows]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODO PARA BORRAR PRODUCTO
@app.route('/producto/<int:id_producto>', methods=['DELETE'])
def delete_producto(id_producto):
    ...

# MÉTODOS PARA EL CARRITO
# MÉTODO PARA CREAR CARRITO
@app.route('/carrito/crear', methods=['POST'])
def crear_carrito():
    try:
        data = request.json
        rut = data.get('usuario_rut')
        tipo_cliente = data.get('tipo_cliente', 'b2c')  # por defecto B2C

        if not rut or tipo_cliente not in ['b2b', 'b2c']:
            return jsonify({'error': 'usuario_rut y tipo_cliente válidos son requeridos'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si ya tiene un carrito abierto
        cursor.execute("""
            SELECT id_carrito FROM app_carrito
            WHERE usuario_rut = ? AND estado = 'abierto'
            ORDER BY fecha_creacion DESC LIMIT 1
        """, (rut,))
        carrito_existente = cursor.fetchone()

        if carrito_existente:
            return jsonify({
                'message': 'Ya tienes un carrito abierto',
                'id_carrito': carrito_existente['id_carrito']
            }), 200

        # Crear nuevo carrito
        fecha_creacion = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO app_carrito (usuario_rut, fecha_creacion, estado, tipo_cliente)
            VALUES (?, ?, 'abierto', ?)
        """, (rut, fecha_creacion, tipo_cliente))
        conn.commit()

        nuevo_id = cursor.lastrowid
        return jsonify({
            'message': 'Carrito creado exitosamente',
            'id_carrito': nuevo_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODO PARA AGREGAR PRODUCTOS AL CARRITO
@app.route('/carrito/<int:carrito_id>/agregar_producto', methods=['POST'])
def agregar_producto_a_carrito(carrito_id):
    try:
        data = request.json
        producto_id = data.get('producto_id')
        cantidad_nueva = int(data.get('cantidad', 1))

        if not producto_id or cantidad_nueva <= 0:
            return jsonify({'error': 'producto_id y cantidad deben ser válidos'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que el carrito esté abierto y recuperar tipo_cliente
        cursor.execute("""
            SELECT tipo_cliente FROM app_carrito
            WHERE id_carrito = ? AND estado = 'abierto'
        """, (carrito_id,))
        carrito = cursor.fetchone()
        if not carrito:
            return jsonify({'error': f'Carrito {carrito_id} no existe o no está abierto'}), 404
        tipo_cliente = carrito['tipo_cliente']

        # Verificar que el producto exista y obtener el precio correcto
        if tipo_cliente == 'b2b':
            cursor.execute("SELECT precio_mayorista FROM app_producto WHERE id_producto = ?", (producto_id,))
        else:
            cursor.execute("SELECT precio_minorista FROM app_producto WHERE id_producto = ?", (producto_id,))
        producto = cursor.fetchone()
        if not producto:
            return jsonify({'error': f'Producto {producto_id} no existe'}), 404

        precio_unitario = producto[0]

        # Verificar stock total disponible
        cursor.execute("""
            SELECT SUM(cantidad) as stock_disponible
            FROM app_stock
            WHERE producto_id = ?
        """, (producto_id,))
        stock_data = cursor.fetchone()
        stock_disponible = stock_data['stock_disponible'] if stock_data['stock_disponible'] else 0

        # Verificar si ya está en el carrito
        cursor.execute("""
            SELECT id_item, cantidad FROM app_carrito_item
            WHERE carrito_id = ? AND producto_id = ?
        """, (carrito_id, producto_id))
        item_existente = cursor.fetchone()

        if item_existente:
            cantidad_anterior = item_existente['cantidad']
            nueva_cantidad_total = cantidad_anterior + cantidad_nueva

            if nueva_cantidad_total > stock_disponible:
                return jsonify({
                    'error': f'Stock insuficiente. Total disponible: {stock_disponible}. Ya tienes {cantidad_anterior} en el carrito.'
                }), 400

            # Actualizar la cantidad del producto en el carrito
            cursor.execute("""
                UPDATE app_carrito_item
                SET cantidad = ?
                WHERE id_item = ?
            """, (nueva_cantidad_total, item_existente['id_item']))

            subtotal_anterior = cantidad_anterior * precio_unitario
            subtotal_nuevo = nueva_cantidad_total * precio_unitario
            diferencia_total = subtotal_nuevo - subtotal_anterior

            mensaje = f'Cantidad actualizada a {nueva_cantidad_total}'
        else:
            if cantidad_nueva > stock_disponible:
                return jsonify({
                    'error': f'Stock insuficiente. Total disponible: {stock_disponible}.'
                }), 400

            subtotal_nuevo = cantidad_nueva * precio_unitario
            diferencia_total = subtotal_nuevo

            cursor.execute("""
                INSERT INTO app_carrito_item (carrito_id, producto_id, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            """, (carrito_id, producto_id, cantidad_nueva, precio_unitario))

            mensaje = 'Producto agregado al carrito'

        # ✅ Recalcular total del carrito desde los ítems
        cursor.execute("""
            SELECT SUM(cantidad * precio_unitario) AS total FROM app_carrito_item
            WHERE carrito_id = ?
        """, (carrito_id,))
        nuevo_total = cursor.fetchone()['total'] or 0

        cursor.execute("""
            UPDATE app_carrito
            SET total_carrito = ?
            WHERE id_carrito = ?
        """, (nuevo_total, carrito_id))

        conn.commit()
        return jsonify({'message': mensaje}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODO PARA QUITAR PRODUCTOS DEL CARRITO
@app.route('/carrito/<int:carrito_id>/quitar_producto', methods=['POST'])
def quitar_producto_del_carrito(carrito_id):
    try:
        data = request.json
        producto_id = data.get('producto_id')
        cantidad_quitar = int(data.get('cantidad', 1))

        if not producto_id or cantidad_quitar <= 0:
            return jsonify({'error': 'producto_id y cantidad deben ser válidos'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar que el producto esté en el carrito
        cursor.execute("""
            SELECT id_item, cantidad FROM app_carrito_item
            WHERE carrito_id = ? AND producto_id = ?
        """, (carrito_id, producto_id))
        item = cursor.fetchone()

        if not item:
            return jsonify({'error': f'Producto {producto_id} no está en el carrito'}), 404

        cantidad_actual = item['cantidad']
        id_item = item['id_item']

        if cantidad_quitar >= cantidad_actual:
            # Eliminar el producto del carrito
            cursor.execute("""
                DELETE FROM app_carrito_item
                WHERE id_item = ?
            """, (id_item,))
            mensaje = 'Producto eliminado completamente del carrito'
        else:
            # Reducir la cantidad
            nueva_cantidad = cantidad_actual - cantidad_quitar
            cursor.execute("""
                UPDATE app_carrito_item
                SET cantidad = ?
                WHERE id_item = ?
            """, (nueva_cantidad, id_item))
            mensaje = f'Se redujo la cantidad del producto a {nueva_cantidad}'

        # Recalcular el total del carrito
        cursor.execute("""
            SELECT SUM(cantidad * precio_unitario) AS total
            FROM app_carrito_item
            WHERE carrito_id = ?
        """, (carrito_id,))
        nuevo_total = cursor.fetchone()['total'] or 0

        cursor.execute("""
            UPDATE app_carrito
            SET total_carrito = ?
            WHERE id_carrito = ?
        """, (nuevo_total, carrito_id))

        conn.commit()
        return jsonify({'message': mensaje, 'total_carrito_actualizado': nuevo_total}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# MÉTODO PARA VER CARRITO
@app.route('/carrito/<int:carrito_id>', methods=['GET'])
def ver_carrito(carrito_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el carrito existe
        cursor.execute("""
            SELECT id_carrito, usuario_rut, tipo_cliente, estado, fecha_creacion, total_carrito
            FROM app_carrito
            WHERE id_carrito = ?
        """, (carrito_id,))
        carrito = cursor.fetchone()
        if not carrito:
            return jsonify({'error': f'Carrito {carrito_id} no existe'}), 404

        carrito_data = dict(carrito)

        # Obtener productos en el carrito
        cursor.execute("""
            SELECT 
                p.nombre AS nombre_producto,
                ci.producto_id,
                ci.cantidad,
                ci.precio_unitario,
                (ci.cantidad * ci.precio_unitario) AS subtotal
            FROM app_carrito_item ci
            JOIN app_producto p ON p.id_producto = ci.producto_id
            WHERE ci.carrito_id = ?
        """, (carrito_id,))
        productos = [dict(row) for row in cursor.fetchall()]

        carrito_data["productos"] = productos

        return jsonify(carrito_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)