from ConnectionDB import ConnectionDB
from random import sample
import json, os

class ProductoGestion(ConnectionDB):
   
    def obtener_producto(self, id_producto):
        producto = {}
        try:
            self.getCursor()
            self._cursor.execute("""
                SELECT id_producto, nombre, descripcion, precio,
                       stock, categoria
                FROM Producto 
                WHERE id_producto = %s
            """, (id_producto,))
            
            fila = self._cursor.fetchone()

            if not fila:
                return None
            producto = {
                "id_producto": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "precio": fila[3],
                "stock": fila[4],
                "categoria": fila[5],
            }
            self._cursor.callproc("sp_obtener_rutas_imagenes", (id_producto,))
            rutas = self._cursor.fetchall()

            # Convertir lista de tuplas en lista simple
            producto["imagenes"] = [r[0] for r in rutas]

        except Exception as e:
            print(f"Error al obtener productos: {e}")
        finally:
            self.closeConnection()

        return producto

    #Funcionalidad obtener prod
    def obtener_todos(self):
        productos = []
        try:
            self.getCursor()
            self._cursor.callproc("sp_ver_productos")
            productos = self._cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener productos: {e}")
        finally:
            self.closeConnection()
        return productos

    #Funcionalidad alta,baja y modif
    # Alta (insertar producto)
    def stringAleatorio(self):
        #Generando string aleatorio
        string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
        longitud         = 20
        secuencia        = string_aleatorio.upper()
        resultado_aleatorio  = sample(secuencia, longitud)
        string_aleatorio     = "".join(resultado_aleatorio)
        return string_aleatorio
    
    def insertar(self, nombre, descripcion, precio, stock, categoria, imagenes):
        try:
            imagenes_data = []
            for img in imagenes:
                extension = os.path.splitext(img.filename)[1]
                ruta = "static/imagenes/"+self.stringAleatorio()+ extension
                img.save(ruta)
                imagenes_data.append({
                    "ruta": ruta,
                    "mime_type": img.mimetype,
                    "peso": len(img.read())
                })
                img.seek(0)  # por si hay que leerla otra vez

            self.getCursor()
            return self._cursor.callproc("sp_registrar_producto", (nombre, descripcion, precio, stock, 
                       categoria, json.dumps(imagenes_data)))
        except Exception as e:
            return f"Error al insertar producto: {e}"
        finally:
            self.closeConnection()

    # Modificación (update producto)
    def actualizar(self, producto):
        try:
            with self.conexion.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE producto
                    SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria=%s, imagen=%s
                    WHERE id_producto=%s
                """, (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.categoria, producto.imagen, producto.id_producto))
                self.conexion.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            self.conexion.close()

    # Baja (delete producto)
    def eliminar(self, id_producto):
        try:
            self.getCursor()
            self._cursor.callproc("sp_obtener_rutas_imagenes", (id_producto,))

            for (ruta,) in self._cursor.fetchall():
                if os.path.exists(ruta):
                    os.remove(ruta)

            self._cursor.callproc("sp_eliminar_producto", (id_producto,))
            return True
        
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            self.closeConnection()

    # Funcionalidad  comprar prod
    def registrar_compra(self, id_producto, cantidad, id_cliente):
        try:
            with self.conexion.connection.cursor() as cursor:
                # Insertamos una nueva solicitud en estado "pendiente"
                cursor.execute("""
                    INSERT INTO solicitud_compra (id_producto, id_cliente, cantidad, estado)
                    VALUES (%s, %s, %s, 'pendiente')
                """, (id_producto, id_cliente, cantidad))
                self.conexion.connection.commit()
                return True
        except Exception as e:
            print(f"Error al registrar compra: {e}")
            return False
        finally:
            self.conexion.close()

    def obtener_categorias(self):
        try:
            self.getCursor()
            self._cursor.callproc("sp_ver_categorias")
            resultado = self._cursor.fetchall()
            categorias = []
            for fila in resultado:
                for categoria in fila:
                    categorias.append(categoria)
            return categorias
        except Exception as e:
            return f"Error al obtener categorias: {e}"
        finally:
            self.closeConnection()
