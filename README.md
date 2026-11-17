# AC Hotel Punta Cana · landing

Sitio estático (HTML, CSS y JavaScript sin dependencias). No necesita compilación.

- Celular y tableta (menos de 1280 px de ancho): versión móvil.
- Computadora (1280 px o más): versión de escritorio.

## Estructura

```
index.html            página principal (incluye las dos versiones)
favicon.ico
vercel.json           cabeceras de seguridad y caché
assets/css/site.css   estilos, tokens de marca y fuentes
assets/js/app.js      fechas (hora de República Dominicana) e interactividad
assets/img/           imágenes optimizadas (WebP)
assets/fonts/         Cormorant Garamond, Montserrat y Work Sans (licencia OFL)
```

## Para actualizar

- Los eventos de temporada se ocultan solos al día siguiente de su fecha (atributo `data-until`).
- La tarjeta «Próximo en la agenda» se calcula sola en `assets/js/app.js` (lista `agendaAll`).
- Las imágenes y fuentes se guardan en caché una semana: si cambias una foto, súbela con otro nombre.
