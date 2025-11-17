from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = 'producto'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(550), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(255))

    solicitudes = db.relationship('SolicitudCompra', backref='producto', lazy=True)

class SolicitudCompra(db.Model):
    __tablename__ = 'solicitud_compra'

    id_solicitud = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    id_cliente = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Enum('pendiente', 'aceptada', 'rechazada'), default='pendiente')
    fecha = db.Column(db.DateTime, server_default=db.func.now())
