import pymysql
import bcrypt

class ConnectionDB:

    @staticmethod
    def getCredencialesBD(ruta):
        credencialesBD = {}
        try:
            with open(ruta, "r") as f:
                for linea in f:
                    clave, valor = linea.strip().split(":")
                    credencialesBD[clave] = valor
            return credencialesBD
    
        except FileNotFoundError:
            return {}
        except ValueError:
            return {}
    
    _credencialesDB = getCredencialesBD("credencialesBD.txt")
    _connectionDB = None
    _cursor = None

    def openConnection(self):
        try:
            self._connectionDB  = pymysql.connect(
                host = self._credencialesDB["DB_HOST"],
                user = self._credencialesDB["DB_USER"],
                password = self._credencialesDB["DB_PASSWORD"],
                database = self._credencialesDB["DB_NAME"]
            )
            self._cursor = self._connectionDB.cursor()

        except Exception as e:
            print("Error al abrir conexión:", e)
            self._connectionDB = None
            self._cursor = None
    
    def closeConnection(self):
        if self._cursor:
            try:
                self._cursor.close()
            except:
                pass
        if self._connectionDB:
            try:
                self._connectionDB.close()
            except:
                pass
        self._cursor = None
        self._connectionDB = None

    def getCursor(self):
        if not self._cursor:
            self.openConnection()
        return self._cursor
