# Herramientas de la landing (rama `herramientas`)

Esta rama NO se publica (vercel.json desactiva sus despliegues). Contiene lo necesario
para regenerar el sitio estático que vive en `main` (producción: ac-planes.vercel.app y modo-pink.vercel.app).

## Fuente del diseño
Artifact de Claude Design: https://claude.ai/artifact/JKi1TuFKVfD1dzLGE4Jryj
- `project/V2.dc.html` (celular, fuente principal)
- `project/Desktop.dc.html` (computadora; se deriva de V2 con `render/mkdesktop.py <alto>`)
- Imágenes: `/_blob/<id>`. El mapa `BLOB` en `export/gen2.py` traduce cada id a un archivo de `img/`.

## Regenerar y publicar
1. Traer `V2.dc.html` y `Desktop.dc.html` actuales del artifact a `canvas/project/`.
2. Si aparece un `/_blob/<id>` nuevo: descargar ese asset del artifact a `img/<nombre>.jpg`
   y agregarlo a `BLOB` en `export/gen2.py` (nombre nuevo para no chocar con la caché de 1 semana).
3. `cd render && npm install` (fuentes @fontsource).
4. `cd export && python3 gen2.py` → genera `export/site/`.
5. Probar: `python3 serve.py site &` y `node t2.js` (360–1440 px: sin scroll horizontal, sin errores, interacciones OK).
6. En un clon de `main`: `git rm -rq .`, copiar `export/site/.` , commit, push. Vercel despliega solo.
7. Verificar: `gh api repos/ndelacruz-create/qr-empresa/commits/<sha>/status` → success.

## Reglas
- Español neutro en los textos. noindex se mantiene. No usar dominio acpuntacana.
- Los wa.link se conservan. Cabeceras de seguridad en `export/vercel.json` (CSP sin inline scripts).
- Los eventos con fecha se ocultan solos al día siguiente (data-until); no hace falta redesplegar por eso.

## Versiones por temporada
- `VERSION` (variable de entorno) elige qué archivos usar: sin valor → `V2.dc.html`/`Desktop.dc.html` (Thanksgiving, 23–26 nov);
  `VERSION=navidad` → `V2-navidad.dc.html`/`Desktop-navidad.dc.html` (Nochebuena destacada, desde el 27 nov).
- Ejemplo: `cd export && VERSION=navidad python3 gen2.py`. Para el escritorio: `cd render && VERSION=navidad python3 mkdesktop.py <alto>`.
- gen2.py se niega a generar si quedan datos entre corchetes sin completar ([Qué incluye], [Precio], [fecha]).
