from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps
from flask_cors import CORS
from Cliente import Cliente
import pymysql
from datetime import datetime
from Producto import Producto
cliente = Cliente()


app = Flask(__name__)
CORS(app) # Esto permite cualquier origen
# o si querés más control:
# CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = cliente.get_jwt_secret("credencialesJWT.txt")

jwt = JWTManager(app)

def role_required(role_name):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_data = get_jwt_identity()
            if not user_data or user_data['rol'] != role_name:
                print(user_data)
                return jsonify({'message': 'Acceso denegado, rol insuficiente'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route("/api")
@jwt_required()
def route():
    cliente_actual = get_jwt_identity()
    print(cliente_actual)
    return "Home"

@app.route("/api/login", methods=["POST"])
def iniciarSesion():
    data = request.get_json()
    email = data.get("email")
    contrasena = data.get("contrasena")
    cliente.setEmail(email)
    cliente.setContrasena(contrasena)
    user = cliente.iniciarSesion()
    return user

@app.route("/api/signup", methods=["POST"])
def registrarse():
    data = request.get_json()
    cliente.setNombre(data.get("nombre"))
    cliente.setApellido(data.get("apellido"))
    cliente.setEmail(data.get("email"))
    cliente.setContrasena(data.get("contrasena"))
    cliente.setTelefono(data.get("telefono"))
    #cliente.setDireccion(data.get("direccion"))
    estado = cliente.validarFormatoCredenciales()
    return estado

#Funcinalida obtener prod
@app.route('/api/productos/<int:id_producto>', methods=['GET'])
def detalle_producto(id_producto):
    producto = Producto()  # <- se instancia
    producto_detalle = producto.obtener_detalle_producto(id_producto)
    return jsonify(producto_detalle)

@app.route('/api/productos', methods=['GET'])
def mostrar_productos():
    producto = Producto()  # <- se instancia
    productos = producto.obtener_productos()
    return jsonify(productos)

#Funcinalidad alta baja y modif
# Alta
@app.route('/api/productos', methods=['POST'])
def alta_producto():
    datos = request.form
    print(request)
    producto = Producto()
    nombre= datos.get("nombre")
    descripcion=datos.get("descripcion")
    precio=datos.get("precio")
    stock=datos.get("stock")
    categoria=datos.get("categoria")
    imagenes= request.files.getlist("imagenes")
    return jsonify(producto.alta(nombre, descripcion, precio, stock, categoria, imagenes))

# Modificación
@app.route('/api/productos/<int:id_producto>', methods=['PUT'])
def modificar_producto(id_producto):
    datos = request.json
    producto = Producto(
        id_producto=id_producto,
        nombre=datos.get("nombre"),
        descripcion=datos.get("descripcion"),
        precio=datos.get("precio"),
        stock=datos.get("stock"),
        categoria=datos.get("categoria"),
        imagen=datos.get("imagen")
    )
    return jsonify(producto.modificar())

# Baja
@app.route('/api/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    producto = Producto(id_producto=id_producto)
    return jsonify(producto.baja())


#Funcionalidad comprar prod
@app.route('/api/comprar', methods=['POST'])
def comprar_producto():
    datos = request.json
    id_producto = datos.get("id_producto")
    id_cliente = datos.get("id_cliente")
    cantidad = datos.get("cantidad")

    producto = Producto(id_producto=id_producto)
    resultado = producto.comprar(id_cliente, cantidad)
    return jsonify(resultado)

@app.route('/api/productos/categorias', methods=['GET'])
def ver_categorias():
    producto = Producto()
    resultado = producto.mostrar_categorias()
    print(resultado)
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)


