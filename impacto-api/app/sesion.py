"""Quién es el usuario de cada pedido, a partir del token de Supabase que manda la app.

La cuenta es opcional (docs/cuentas.md): `usuario_opcional` devuelve None si no hay sesión,
y `usuario_requerido` responde 401 si la ruta necesita una cuenta.
"""

from dataclasses import dataclass

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app import supabase

_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class Usuario:
    id: str
    correo: str
    verificado: bool
    nombre: str | None


def _validar(credenciales: HTTPAuthorizationCredentials | None) -> Usuario | None:
    if credenciales is None:
        return None
    try:
        datos = supabase.usuario_desde_token(credenciales.credentials)
    except supabase.SinConfiguracion:
        raise HTTPException(status_code=503, detail="Las cuentas no están configuradas en este servidor")
    if datos is None:
        raise HTTPException(status_code=401, detail="Tu sesión venció. Vuelve a iniciar sesión.")
    return Usuario(
        id=datos["id"],
        correo=datos.get("email", ""),
        verificado=bool(datos.get("email_confirmed_at")),
        nombre=(datos.get("user_metadata") or {}).get("nombre"),
    )


def usuario_opcional(credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> Usuario | None:
    return _validar(credenciales)


def usuario_requerido(credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> Usuario:
    usuario = _validar(credenciales)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Necesitas iniciar sesión.")
    return usuario
