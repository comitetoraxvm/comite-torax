"""
WSGI entry point para Gunicorn/Render.
No inicializa la BD aquí - se hace en la primera request (thread-safe).
"""
from app import app

# El app ya está listo. La inicialización de BD sucede en app.before_first_request
# o en el primer endpoint que se toque. Ver app.py para los detalles.
