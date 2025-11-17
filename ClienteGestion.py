import pymysql
import bcrypt
from ConnectionDB import ConnectionDB

class ClienteGestion(ConnectionDB):

    def registrarCliente(self, nombre, apellido, telefono, email, contrasena):
        try:
            self.getCursor()
            hashed_pwd = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            self._cursor.callproc("sp_registrar_cliente",(nombre, apellido, telefono, email, hashed_pwd))
            # Aca se llama al SP que registra al cliente en la DB y se le pasan los parametros que
            # llegan de la clase Cliente
            return True
        except pymysql.IntegrityError:
            return False  
        except pymysql.MySQLError:  
            return False
        finally:
            self.closeConnection()
    
    #def validarAntiguedad(id_Cliente):
