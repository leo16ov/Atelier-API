from ProductoGestion import ProductoGestion
import json
class Producto:
    def __init__(self, id_producto=None, nombre=None, descripcion=None, precio=None, stock=None, categoria=None,imagenes=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.imagenes = imagenes
        self.gestion = ProductoGestion()  # 👈 instanciada como atributo

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio) if self.precio is not None else None,
            "stock": self.stock,
            "categoria": self.categoria,
            "imagenes": self.imagenes
        }

    def obtener_detalle_producto(self, id_producto):
        producto = self.gestion.obtener_producto(id_producto)

        if not producto:
            return {}

        # Ya no usamos json.loads
        print(producto)
        return producto

    def obtener_productos(self):
        resultados = self.gestion.obtener_todos()

        if len(resultados[0])== 1:
            print(resultados[0])
            return []
        productos=[]
        for fila in resultados:    
            producto = Producto(*fila).to_dict()
            producto["imagenes"] = json.loads(producto["imagenes"])
            #imagenes = []
            #for imagen in producto["imagenes"]:
            #    imagenes.append(imagen[1:len(imagen)])
            #producto["imagenes"] = imagenes
            productos.append(producto)

        return productos

    #Funcionalidad alta,baja y  modif
     # Alta
    def alta(self, nombre, descripcion, precio, stock, categoria, imagenes):
        if not all([nombre, descripcion, precio, stock, categoria]):
            print({"mensaje": "Faltan datos obligatorios"})
            return {"mensaje": "Faltan datos obligatorios"}
        if len(imagenes) == 0:
            print({"mensaje": "Las imagenes del producto deben ser obligatorias"})
            return {"mensaje": "Las imagenes del producto deben ser obligatorias"}
        mensaje = self.gestion.insertar(nombre, descripcion, precio, stock, categoria, imagenes)
        print(mensaje)
        return {"mensaje": mensaje}

    # Modificación
    def modificar(self):
        if not self.id_producto:
            return {"error": "Falta el ID del producto"}
        return {"mensaje": "Producto actualizado correctamente"} if self.gestion.actualizar(self) else {"error": "Error al actualizar producto"}

    # Baja
    def baja(self):
        if not self.id_producto:
            return {"error": "Falta el ID del producto"}
        estado = self.gestion.eliminar(self.id_producto)
        if estado:
            respuesta= {"mensaje": "Producto eliminado correctamente"}
        else:
            respuesta= {"error": "Error al eliminar producto"}
        return respuesta
    
    #Funcionalidad comprar prod
    def comprar(self, id_cliente, cantidad):
        # Validaciones básicas
        if not self.id_producto:
            return {"error": "Falta el ID del producto."}
        if not id_cliente:
            return {"error": "Falta el ID del cliente."}
        if not cantidad or cantidad <= 0:
            return {"error": "La cantidad debe ser mayor que cero."}

        exito = self.gestion.registrar_compra(self.id_producto, cantidad, id_cliente)
        if exito:
            return {"mensaje": "Compra registrada correctamente. En espera de confirmación del vendedor."}
        else:
            return {"error": "No se pudo registrar la compra."}
        
    def mostrar_categorias(self):
        categorias = self.gestion.obtener_categorias()
        if not categorias:
            return "No se encontraron categorias para mostrar"
        
        return categorias

