# Comité Torax – Historia Clínica Web

[![Run tests](https://github.com/comitetoraxvm/comite-torax/actions/workflows/pytest.yml/badge.svg)](https://github.com/comitetoraxvm/comite-torax/actions/workflows/pytest.yml)

Aplicación Flask que permite a un pequeño grupo de médicos registrar pacientes, consultas y estudios de patología torácica. Incluye autenticación, aprobación de usuarios, ficha clínica estandarizada, filtros avanzados, consentimiento informado, auditoría y respaldos automáticos.

## Pila tecnológica

- Python 3.11+/Flask
- Flask-Login, Flask-WTF, SQLAlchemy (SQLite o Postgres)
- HTML/CSS simples renderizados con Jinja2

## Requisitos

- Python ≥ 3.11
- Virtualenv recomendado

## Variables de entorno

| Variable       | Descripción                                              | Valor por defecto             |
| -------------- | -------------------------------------------------------- | ----------------------------- |
| `SECRET_KEY`   | Clave de sesión Flask/CSRF. Cambiar en producción.       | `cambia-esta-clave-por-una…` |
| `DATABASE_URL` | Cadena SQLAlchemy (Ej. `sqlite:///comite.db` / Postgres) | `sqlite:///comite.db`        |

Opcionalmente define `FLASK_APP=app.py` y `FLASK_ENV=production`.

## Configuración local

```bash
cd COMITE TORAX APP
python -m venv .venv
.venv\Scripts\activate        # Windows
python -m pip install -r requirements.txt
set SECRET_KEY=...            # o export en Linux/macOS
set DATABASE_URL=sqlite:///comite.db
set PYTHONIOENCODING=utf-8
python app.py
```

Se crea automáticamente la base `instance/comite.db`, un usuario admin (`admin` / `Admin2025!`) y un backup incremental en `backups/`.

## Características

- Registro/aprobación de usuarios (roles admin/médico).
- Ficha clínica completa con consentimiento informado, exposiciones, estudios, consultas y auditoría (`audit.log`).
- Filtros avanzados (centro, ciudad, edad, sexo, tabaquismo múltiple, patologías).
- Vista imprimible/anonimizable para reuniones.
- CSRF en todos los formularios y logging de acciones sensibles.

## Flujos de seguridad

- Contraseñas robustas (≥10 caracteres, mayúsculas/minúsculas/números/símbolos).
- Cambio de contraseña disponible en “Cambiar clave”.
- `audit.log` registra logins, cambios, impresiones y eliminaciones.
- Backups automáticos al detectar cambios en `instance/comite.db`.

## Despliegue sugerido

### Docker

```bash
docker compose build
docker compose up
```

### Manual / Gunicorn

1. Provisión de VPS o servicio (Ubuntu + Nginx) o PaaS (Render/Fly).
2. Configurar `SECRET_KEY` y `DATABASE_URL` (recomendado Postgres).
3. Instalar dependencias y ejecutar Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:8000 app:app
   ```
4. Servir vía Nginx/traefik con HTTPS.
5. Programar respaldos (`backups/`) y rotación de `audit.log`.

Para ambientes con más usuarios, migra la base a Postgres/MySQL cambiando `DATABASE_URL` y ejecutando `flask db upgrade` (o `db.create_all()` según corresponda).

## Usuarios iniciales

- Admin creado automáticamente: `admin` / `Admin2025!`. Cambia la contraseña tras el primer login.

## Mantenimiento

- Revisa `catalogs.json` para actualizar listas (centros, patologías, exposiciones).
- Supervisa `audit.log` y limpia respaldos antiguos en `backups/`.
- Actualiza `requirements.txt` y ejecuta `pip install -r requirements.txt` al incorporar nuevas dependencias.

## Próximos pasos

- Dockerfile / docker-compose para despliegue reproducible. ✅
- Exportaciones anonimizadas (CSV/PDF). ✅ (CSV incluido)
- Recuperación de contraseñas por email.
- Landing pública (`landing/`) para presentar al comité y enlazar a la app.
- Recuperación de contraseñas por email.
- Landing pública (`landing/`) para presentar al comité y enlazar a la app.

## Guía de despliegue recomendado

1. **Infraestructura**
   - VPS (Ubuntu 22.04) en DigitalOcean, Hetzner o similar, o PaaS tipo Render/Fly.
   - Configura un registro DNS: `app.comite` para la app, `www.comite` o `landing` para el sitio informativo (carpeta `landing/`).

2. **Sistema operativo**
   - Instala Docker y Docker Compose o usa `python3-pip + venv`.
   - Crea un usuario no root para correr la app.

3. **Base de datos**
   - En desarrollo puedes seguir con SQLite.
   - En producción se recomienda un Postgres gestionado (ElephantSQL, RDS, etc.). Cambia `DATABASE_URL` a `postgresql+psycopg://...`.

4. **Aplicación**
   - Copia el código al servidor (Git, rsync o SFTP).
   - Exporta variables en `/etc/environment` o usa un `.env`:
     ```
     SECRET_KEY=… (mínimo 32 caracteres aleatorios)
     DATABASE_URL=postgresql+psycopg://user:pass@host/db
     ```
   - Arranca con `docker compose up -d` o `gunicorn --workers 3 --bind 0.0.0.0:8000 app:app`.

5. **Nginx + HTTPS**
   - Instala Nginx, crea un sitio que haga proxy a `localhost:8000`.
   - Emite certificados con Let's Encrypt/Certbot.
   - Sirve la carpeta `landing/` en otro server block (puede estar en el mismo Nginx) para la landing pública.

6. **Backups y auditoría**
   - Monta `instance/` y `backups/` fuera del contenedor (ya está en `docker-compose.yml`).
   - Programa una tarea cron (o script) que copie `instance/comite.db`, `backups/` y `audit.log` a un almacenamiento externo (S3, Google Drive, etc.).
   - Revisa y rota `audit.log` periódicamente.

7. **Monitoreo y actualizaciones**
   - Mantén el sistema actualizado (`apt upgrade`, `pip install -r requirements.txt`).
   - Revisa accesos y acciones en `audit.log`.
   - Cambia la contraseña del admin inicial y crea cuentas para cada médico (aprobación vía panel admin).
