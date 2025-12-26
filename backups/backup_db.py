import os
import shutil
import datetime

# Carpeta base del proyecto (donde está app.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta a la base de datos ORIGINAL (dentro de "instance")
DB_PATH = os.path.join(BASE_DIR, "instance", "comite.db")

# Carpeta donde vamos a guardar los backups (dentro de "backups")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Crear carpeta de backups si no existe
os.makedirs(BACKUP_DIR, exist_ok=True)

# Nombre del archivo de backup con fecha y hora
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_filename = f"comite_backup_{timestamp}.db"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Comprobar que la base existe
if not os.path.exists(DB_PATH):
    print("⚠️ No se encontró la base de datos en:", DB_PATH)
else:
    # Copiar la base
    shutil.copy2(DB_PATH, backup_path)
    print("✅ Backup creado:", backup_path)