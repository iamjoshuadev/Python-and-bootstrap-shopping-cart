from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Cambia esto por una clave segura

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tienda_telefono'

mysql = MySQL(app)

@app.route('/')
def index():
    # Obtener todos los productos de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto")
    productos = cur.fetchall()
    cur.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    producto_id = request.form['id']
    cantidad = request.form['cantidad']

    # Obtener información del producto seleccionado
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE id = %s", (producto_id,))
    producto = cur.fetchone()

    # Obtener el carrito de la sesión o inicializarlo si no existe
    carrito = session.get('carrito', [])

    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item['id'] == producto[0]:
            # Si el producto ya está en el carrito, actualizar la cantidad
            item['cantidad'] += int(cantidad)
            flash('Producto Agregao al carrito con exito')
            break
    else:
        # Si el producto no está en el carrito, agregarlo
        carrito.append({
            'id': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'cantidad': int(cantidad)
        })
    flash('Producto Agregao al carrito con exito')
    # Actualizar el carrito en la sesión
    session['carrito'] = carrito

    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    # Mostrar los productos en el carrito de compras
    carrito = session.get('carrito', [])
    return render_template('carrito.html', carrito=carrito)

@app.route('/vaciar')
def vaciar():
    # Vaciar el carrito de compras
    session.pop('carrito', None)
    flash('Producto eliminado con exito')
    return redirect(url_for('carrito'))

if __name__ == '__main__':
    app.run(debug=True)
