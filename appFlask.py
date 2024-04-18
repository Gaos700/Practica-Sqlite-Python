from flask import Flask, request, render_template, redirect, url_for, flash
import time
import sqlite3

conexion = sqlite3.connect('test.bd') #conectamos con la base de datos
cursor = conexion.cursor() #creamos un cursor para ejecutar comandos sql

app = Flask(__name__, static_folder='static', template_folder='templates') #creamos la aplicacion flask

app.secret_key = 'chibakutensei' #clave secreta para las sesiones para que funciones "flash"

admin = {"goat" : "rasengan"} #diccionario con el usuario y contraseña del administrador

@app.route('/home')
def hello_world():
    conexion = sqlite3.connect('test.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT p.id, p.nombre, p.descripcion, c.nombre, t.nombre FROM productos p JOIN colores c ON p.id_color = c.id JOIN tallas t ON p.id_talla = t.id')
    productos = cursor.fetchall()
    print(productos)

    return render_template('home.html', products = productos)

@app.route('/login', methods=['GET','POST']) #ruta para el login con los metodos GET y POST    
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username'] #obtiene el usuario del formulario
        password = request.form['password'] #obtiene la contraseña del formulario
        if user in admin and admin[user] == password:
            return redirect(url_for('hello_world')) #redirige la rut a def hello_world
        else:
            error = 'Clave Incorrecta'
            return render_template('login.html', error = error)
    else:
        return render_template('login.html', error = error) #renderiza el template login.html
@app.route('/add_product', methods = ['POST']) #ruta para agregar productos con el metdo post
def add_product():
    conexion = sqlite3.connect('test.db') #conectamos con la base de datos
    cursor = conexion.cursor() #creamos un cursor para ejecutar comandos sql
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        color = request.form['color']
        talla = request.form['talla']
        cursor.execute('SELECT id FROM colores WHERE nombre = ?', (color,))
        id_color = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM tallas WHERE nombre = ?', (talla,))
        id_talla = cursor.fetchone()[0]
        cursor.execute('INSERT INTO productos (nombre, descripcion, id_color, id_talla) VALUES (?,?,?,?)', (nombre, descripcion, id_color, id_talla,))
        conexion.commit()
        print('Datos ingresados correctamente')

        flash('Datos ingresados correctamente') #mensaje de exito
        return redirect(url_for('hello_world')) #redirige a la ruta hello_world
@app.route('/edit/<id>') #ruta para editar productos
def edit_product(id):
    conexion = sqlite3.connect('test.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM  productos WHERE id = ?', (id,))
    producto = cursor.fetchall()
    conexion.commit()
    return render_template('editform.html', product = producto[0])

@app.route('/update/<id>', methods= ['POST'])
def update_product(id):
    conexion = sqlite3.connect('test.db')
    cursor = conexion.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        color = request.form['color']
        talla = request.form['talla']
        cursor.execute('SELECT id FROM colores WHERE nombre = ?', (color,))
        id_color = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM tallas WHERE nombre = ?', (talla,))
        id_talla = cursor.fetchone()[0]
        cursor.execute('''UPDATE productos SET nombre =?, descripcion = ?, id_color = ?, id_talla = ? WHERE id = ?''', (nombre, descripcion, id_color, id_talla, id, ))
        conexion.commit()
        flash('Datos actualizados correctamente, espere mientras redirigimos a la pagina principal')
        time.sleep(3)
        return redirect(url_for('hello_world'))



@app.route('/delete/<string:id>') #la ruta es /delete + <string:id> que te devuelve el id que manda el mismo boton {{producto.0}}
def delete_product(id): #Ingresamos el id a la funcion para operar con el
    conexion = sqlite3.connect('test.db')
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM  productos WHERE id= ?', (id, ))
    conexion.commit()
    return redirect(url_for('hello_world'))


if __name__ == '__main__':

    app.run(debug=True) #corre la aplicacion