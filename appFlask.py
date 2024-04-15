from flask import Flask, request, render_template, redirect, url_for, flash

import sqlite3

conexion = sqlite3.connect('test.bd') #conectamos con la base de datos
cursor = conexion.cursor() #creamos un cursor para ejecutar comandos sql

app = Flask(__name__, static_folder='static', template_folder='templates') #creamos la aplicacion flask

app.secret_key = 'chibakutensei' #clave secreta para las sesiones para que funciones "flash"

admin = {"goat" : "rasengan"} #diccionario con el usuario y contraseña del administrador

@app.route('/home')
def hello_world():
    return render_template('home.html')

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


if __name__ == '__main__':

    app.run(debug=True) #corre la aplicacion