from flask import jsonify
from Usuario import Usuario
from ClienteGestion import ClienteGestion
import re

class Cliente(Usuario):
    _direccion = ""
    _telefono = ""
    __clienteGestion = ClienteGestion()

    def setDireccion(self, direccion):
        self._direccion = direccion
    def setTelefono(self, telefono):
        self._telefono = telefono

    def validarFormatoCredenciales(self): 
        valid_pwd = len(self._email)>=13 and len(self._contrasena)>=8
        valid_email = "@gmail.com" in self._email[len(self._email)-10:len(self._email)]
        valid_name = len(self._nombre)>=3 and len(self._nombre)<=30 
        valid_telefono = bool(re.match(r'^11\d{8}$', self._telefono))
        if valid_pwd and valid_email and valid_name and valid_telefono: #Se valida el formato de todas las credenciales
            estadoRegistroCliente = self.__clienteGestion.registrarCliente(self._nombre, self._apellido,
                                                self._telefono, self._email, self._contrasena)
            
            if estadoRegistroCliente:
                return jsonify({"message": "El usuario se registro exitosamente"}), 201
            return jsonify({"error": "No se pudo registrar el usuario"}), 409

        return jsonify({"error": "El formato de las credenciales no son validas"}), 422
    