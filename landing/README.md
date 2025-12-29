# Landing Comite de Torax

Sitio informativo estatico que presenta al comite y enlaza a la aplicacion Flask principal.

## Estructura

- `index.html`: landing simple con los objetivos, descripcion y un boton hacia la app (`http://localhost:5000` por defecto). Cambia el vinculo al dominio final.

## Uso

Puedes subir este HTML a cualquier hosting estatico (Netlify, GitHub Pages, S3 + CloudFront, etc.) o servirlo desde el mismo servidor Nginx que hospede la app.

Si usas Nginx:

```
server {
    listen 80;
    server_name landing.comite;
    root /var/www/landing;
    index index.html;
}
```

<<<<<<< HEAD
El sitio publico puede ser accesible para pacientes o colegas, mientras que la app requiere login y permanece en otra URL (p. ej. `app.comite`). Ajusta los estilos y contenido segun lo necesites.
=======
El sitio publico puede ser accesible para pacientes o colegas, mientras que la app requiere login y permanece en otra URL (p. ej. `app.comite`). Ajusta los estilos y contenido segun lo necesites.
>>>>>>> ca39a71e6698f6d4ec1a9a65577646ea83648565
