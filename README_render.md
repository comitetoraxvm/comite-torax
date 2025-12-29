# Despliegue en Render con recordatorios

Esta app usa Flask + SQLite. Para que Render pueda enviar correos y ejecutar recordatorios diarios (`reminders.py`), configurá lo siguiente:

## Variables de entorno
Usá estas env vars tanto en el servicio web como en el cron/worker:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=comitetoraxvm@gmail.com
MAIL_PASSWORD=APP_PASSWORD_16_DIGITOS
MAIL_DEFAULT_SENDER=comitetoraxvm@gmail.com

DATABASE_URL=sqlite:///comite.db   # o tu URL de DB en Render
PYTHONIOENCODING=utf-8
SECRET_KEY=alguna_clave_segura
```

> `MAIL_PASSWORD`: usa la App Password de Gmail (16 caracteres). No uses tu password normal.

## Servicio Web
Desplegá el servicio web con el comando:
```
python app.py
```
(o bien usar gunicorn si preferís: `gunicorn -w 2 -b 0.0.0.0:5000 app:app`)

## Cron Job / Worker diario
Crear un Cron Job en Render que ejecute 1 vez al día:
```
python reminders.py
```
asegurándote de usar las mismas variables de entorno (MAIL_*, DATABASE_URL, etc.).

## Recordatorios
`reminders.py` envía correos cuando la fecha de control (screening base o controles de seguimiento) coincide con el día actual. Destinatarios:
- Email del paciente (si está cargado).
- Email adicional (“secretaría”) en Screening.
- Email del médico que creó al paciente (si lo tiene).

## Archivos y adjuntos
- Subidas se guardan en `/uploads` (ver `UPLOAD_DIR` en app.py).
- Ajustá el almacenamiento según tu plan de Render si necesitas volumen persistente.

