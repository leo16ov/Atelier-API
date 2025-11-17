import pymysql
import bcrypt
from ConnectionDB import ConnectionDB

class UsuarioGestion(ConnectionDB):

    def __init__(self):
        self.getCursor()

    def _buscarUsuario(self, email, contrasena):
        try:
            self._cursor.callproc("sp_obtener_usuario_por_email", (email,))
            usuario = self._cursor.fetchone()
            if usuario:
                vid_usuario, vemail, vcontrasena, vnombre, vapellido, vtelefono, vrol = usuario
                
                if bcrypt.checkpw(contrasena.encode('utf-8'), vcontrasena.encode('utf-8')):
                    return {"id": vid_usuario, "nombre": vnombre,"apellido": vapellido,
                            "email": vemail ,"telefono": vtelefono, "rol": vrol}
                return {}
            return{}
        except pymysql.MySQLError as e:
            print("ERROR",e)
            return {}
        

