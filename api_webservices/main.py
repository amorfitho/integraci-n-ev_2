from flask import Flask, request, jsonify
from app import app
from config import get_db_connection


@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_producto, p.nombre, p.precio, p.descripcion, f.nombre_familia 
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

@app.route('/producto/<int:id_producto>', methods=['DELETE'])
def delete_producto(id_producto):
    ...

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()