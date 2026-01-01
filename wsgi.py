"""
WSGI entry point para Gunicorn/Render.
Inicializa la BD una sola vez al startup, antes de que Gunicorn levante los workers.
"""
from app import app, create_tables_and_admin

if __name__ != "__main__":
    # Solo ejecutar cuando lo importa Gunicorn (no en tests ni en debug local)
    with app.app_context():
        print("[INIT] Initializing database tables and admin user...")
        try:
            create_tables_and_admin()
            print("[OK] Database initialization complete")
        except Exception as e:
            print(f"[ERROR] Database initialization failed: {e}")
            raise
