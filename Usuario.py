from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from UsuarioGestion import UsuarioGestion


class Usuario:
    _nombre= ""
    _apellido= ""
    _email= ""
    _contrasena= ""
    _rol= ""
    _estado = 0
    __usuarioGestion= UsuarioGestion()
    
    def setNombre(self, nombre):
        self._nombre = nombre
    def setApellido(self, apellido):
        self._apellido = apellido
    def setEmail(self, email):
        self._email = email
    def setContrasena(self, contrasena):
        self._contrasena = contrasena

    def iniciarSesion(self):
        if len(self._email)>=13 and len(self._contrasena)>=8 and "@gmail.com" in self._email[len(self._email)-10:len(self._email)]:
            usuario = self.__usuarioGestion._buscarUsuario(self._email, self._contrasena)
            if usuario:
                access_token = create_access_token(identity= usuario["email"])
                return jsonify({
                    "message": "Request completed successfully",
                    "access_token": access_token,
                    "user": usuario
                    }), 200
            return jsonify({"error": "Resource not found"}), 404 
        
        return jsonify({"error": "Invalid or malformed request"}), 422
    
    def get_jwt_secret(self, ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.startswith("JWT_SECRET_KEY:"):
                        return linea.strip().split(":", 1)[1].strip()
            return None
        except FileNotFoundError:
            return None
        
