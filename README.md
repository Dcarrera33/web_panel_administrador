# Magia en el bosque · web de cursos (Django + MySQL + Gmail)

Web para vender cursos de magia, pensada para que la dueña o el dueño lo gestione **todo desde un panel** sin tocar código.

- **Inicio**: foto a la izquierda, texto a la derecha, y debajo los tres primeros cursos.
- **Cursos**: lista con nombre, descripción breve, nivel, duración y precio; al entrar en uno, toda su información.
- **Saber más**: carrusel de fotos, cómo funcionan los cursos (pasos) y preguntas frecuentes.
- **Contacto**: formulario que llega a tu Gmail (y se guarda en el panel) + enlace a Instagram.
- **Panel de gestión** en `/gestion/`.

## Índice
1. [Puesta en marcha rápida](#puesta-en-marcha-rápida)
2. [Instalación paso a paso (Windows)](#instalación-paso-a-paso-windows)
3. [Páginas de la web](#páginas-de-la-web)
4. [Cómo se usa el panel](#cómo-se-usa-el-panel-gestion)
5. [Cómo escribir los textos largos](#cómo-escribir-los-textos-largos-en-el-panel)
6. [Personalizar para cada cliente](#personalizar-para-cada-cliente)
7. [Qué hay en cada archivo](#qué-hay-en-cada-archivo)
8. [Variables del `.env`](#variables-del-env)
9. [Seguridad incluida](#seguridad-incluida)
10. [Pruebas automáticas](#pruebas-automáticas)
11. [Publicar en internet](#publicar-en-internet)
12. [Problemas frecuentes](#problemas-frecuentes)

---

## Puesta en marcha rápida
Si ya tienes Python, MySQL y la base de datos `magia` creada:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env          (y rellénalo)
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```
- Web: http://127.0.0.1:8000/
- Panel: http://127.0.0.1:8000/gestion/

> **¿Solo quieres probar sin MySQL?** Añade `DB_ENGINE=sqlite` al `.env` y se usará un archivo `db.sqlite3` local.
> Para la web real usa siempre MySQL.

---

## Instalación paso a paso (Windows)

### 1. Instalar lo necesario
1. **Python 3.12 o 3.13** (python.org). Marca «Add Python to PATH».
2. **MySQL 8** y **MySQL Workbench**.
3. **Visual Studio Code**.

### 2. Crear la base de datos con Workbench
Abre tu conexión y ejecuta:
```sql
CREATE DATABASE magia CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

### 3. Preparar el proyecto en VS Code
Abre la carpeta del proyecto y, en la terminal:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Si PowerShell no deja activar el entorno: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### 4. Rellenar el archivo `.env`
Copia `.env.example` como `.env` (en la misma carpeta que `manage.py`) y rellena `SECRET_KEY`, los datos de MySQL
(`DB_PASSWORD`...) y Gmail. Para generar una `SECRET_KEY`:
```
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Gmail (para que los mensajes lleguen a tu correo)
1. Activa la **verificación en dos pasos** en tu cuenta de Google.
2. Entra en https://myaccount.google.com/apppasswords y crea una «contraseña de aplicación».
3. Pega las 16 letras en `GMAIL_APP_PASSWORD` (con o sin espacios) y tu correo en `GMAIL_USER` y `NOTIFY_EMAIL`.

Sin Gmail configurado, los emails se imprimen en la terminal (sirve para probar).

### 5. Crear las tablas, tu usuario y arrancar
```
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```
- `createsuperuser` pide una contraseña de **al menos 10 caracteres**.
- `seed_demo` carga cursos, pasos, preguntas y fotos de ejemplo para ver la web llena. Luego lo sustituyes todo desde el panel.

---

## Páginas de la web

| Dirección | Página |
|---|---|
| `/` | Inicio |
| `/cursos/` | Lista de cursos |
| `/cursos/<nombre-del-curso>/` | Ficha completa de un curso |
| `/saber-mas/` | Carrusel, pasos y preguntas frecuentes |
| `/contacto/` | Formulario de contacto (admite `?curso=...` para dejar el curso ya elegido) |
| `/legal/aviso-legal/`, `/legal/privacidad/`, `/legal/cookies/` | Textos legales |
| `/gestion/` | Panel de gestión (requiere usuario) |

---

## Cómo se usa el panel (`/gestion/`)
- **Portada del panel**: mensajes sin leer, número de cursos y fotos, últimos mensajes y botones directos.
- **Textos y datos de la web**: la foto y el texto de inicio, el nombre de la cabecera, el texto de Saber más y de
  Contacto, el correo y el Instagram, los **colores** (opcional) y los **datos legales**.
- **Cursos**: nombre, descripción breve (la de la lista), descripción completa, nivel, duración, modalidad, precio y foto.
  Debajo se añaden **apartados** (Qué aprenderás, Temario, Requisitos...). Sin precio, la web muestra «Consultar».
  En la lista de cursos se cambian el precio, el orden y la visibilidad directamente; un curso oculto no se ve en la web.
- **Fotos del carrusel**: se suben, se ordenan y se pueden ocultar. Con 2 o más fotos, el carrusel se mueve solo.
- **Pasos** y **Preguntas frecuentes**: lo que aparece en «Saber más».
- **Mensajes recibidos**: todo lo que llega por el formulario queda guardado aquí (además de llegar al correo).
  Al abrir un mensaje se marca como leído.
- Las fotos se reducen y optimizan solas al subirlas (máx. 8 MB).

## Cómo escribir los textos largos en el panel
Vale para la descripción completa, los apartados de los cursos, el texto de inicio, pasos y preguntas frecuentes:
- **Línea en blanco** = párrafo nuevo.
- **Enter normal** = salto de línea dentro del mismo párrafo.
- Líneas que empiezan por **`- `** (o `* `, `• `) = lista con estrellitas (se puede mezclar con párrafos).
- No se admite HTML: lo que escribas se muestra tal cual.

Ejemplo:

    Lo que aprenderás:
    - Forzajes
    - Controles

    Y mucho más.

---

## Personalizar para cada cliente
1. **Todo lo que se ve** (textos, foto, colores, Instagram, datos legales): desde el panel. Qué cursos salen en Inicio
   se decide con el «Orden» de los cursos (salen los tres primeros).
2. **Nombre de la cabecera**: panel → Textos y datos de la web → «Nombre de la web».
3. **Tipografías**: `magia/views.py` (diccionario `FONTS`). Las incluidas (en `magia/static/magia/fonts/`, con sus
   licencias) son Cormorant Garamond (títulos), Pinyon Script (frases a mano) y DM Sans (texto). Se sirven desde la
   propia web, sin Google Fonts.
4. **Diseño más profundo** (formas, luciérnagas, etc.): `magia/static/magia/css/style.css`. Las luciérnagas se quitan
   borrando la línea `<div class="fireflies">` de `magia/templates/magia/base.html`.
5. **Aspecto del panel**: `magia/static/magia/css/admin.css` y `magia/templates/admin/`.

Una instalación por cliente (cada una con su `.env`, su base de datos y su dominio).

### Textos legales
`magia/legal_texts.py` contiene **borradores** adaptados a esta web. Se rellenan solos con los «Datos legales» del panel.
**Que los revise una gestoría o un consultor RGPD antes de publicar.**

---

## Qué hay en cada archivo

| Archivo / carpeta | Para qué sirve |
|---|---|
| `manage.py` | El comando de Django: `runserver`, `migrate`, `createsuperuser`, `test`... |
| `config/settings.py` | Ajustes del proyecto (casi todo se lee del archivo `.env`) |
| `config/urls.py` | Rutas generales: el panel en `/gestion/` y las páginas de errores |
| `magia/models.py` | Las tablas: textos de la web, cursos y apartados, carrusel, pasos, preguntas, mensajes |
| `magia/views.py`, `magia/urls.py` | Las páginas (y `theme.css`, que aplica los colores y tipografías elegidos) |
| `magia/admin.py`, `magia/sites.py` | El panel de gestión y su portada |
| `magia/text.py`, `magia/templatetags/` | Convierten los textos del panel en párrafos y listas; iconos |
| `magia/emails.py` | Envío de emails con Gmail (en segundo plano) |
| `magia/legal_texts.py` | Borradores del aviso legal, la privacidad y las cookies |
| `magia/middleware.py`, `magia/ratelimit.py` | Cabeceras de seguridad y límite de envíos del formulario |
| `magia/context_processors.py` | Datos disponibles en todas las plantillas (contenido de la web, año) |
| `magia/templates/magia/` | El HTML (`base.html` tiene el doble encabezado y el pie; `_course_row.html`, la fila de cada curso) |
| `magia/templates/admin/` | Plantillas del panel (portada personalizada) |
| `magia/static/magia/` | CSS, JavaScript (`main.js`: menú móvil, carrusel y animaciones de entrada), tipografías e imágenes |
| `magia/management/commands/seed_demo.py` | Carga contenido de ejemplo (`python manage.py seed_demo`) |
| `magia/tests.py` | Pruebas automáticas |
| `media/` | Las fotos que se suben desde el panel (se crea sola, no va a Git) |
| `Procfile` | Comando de arranque para hostings tipo Heroku/Railway (`gunicorn config.wsgi`) |
| `.env` | Tus claves y contraseñas (**nunca** a Git) |

## Variables del `.env`

| Variable | Obligatoria | Para qué sirve |
|---|---|---|
| `DJANGO_DEBUG` | — | `1` en tu ordenador, `0` en producción |
| `SECRET_KEY` | Sí (en producción) | Clave secreta de Django |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Sí | Conexión a MySQL |
| `DB_ENGINE` | No | `sqlite` para probar sin MySQL |
| `GMAIL_USER`, `GMAIL_APP_PASSWORD` | No | Cuenta que envía los emails |
| `NOTIFY_EMAIL` | No | Dónde llegan los mensajes (por defecto, `GMAIL_USER`) |
| `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` | Sí (en producción) | Tus dominios |
| `TRUST_PROXY`, `FORCE_HTTPS` | En producción | HTTPS detrás de Nginx o del proxy del hosting |
| `EMAIL_ASYNC` | No | `0` para enviar los emails esperando a Gmail (por defecto `1`) |
| `RATE_LIMIT` | No | `0` desactiva el límite de envíos del formulario (por defecto `1`) |

## Seguridad incluida
- Panel en `/gestion/` (no en `/admin/`), contraseñas de 10+ caracteres y sesión de 8 horas.
- Formulario de contacto con protección CSRF, **campo trampa** contra robots y **límite de envíos por IP**
  (4 por minuto y 20 al día).
- Cabeceras de seguridad (Content-Security-Policy, anti-iframe, nosniff) y cookies seguras en producción.
- Los textos del panel se escapan: no se puede inyectar HTML ni cabeceras de email.

---

## Pruebas automáticas
```
python manage.py test
```
Django crea una base de datos temporal (`test_magia`), así que el usuario de MySQL necesita permiso para crear bases de
datos. Si no lo tiene, o para ir más rápido, ejecútalas con SQLite (PowerShell):
```
$env:DB_ENGINE="sqlite"; python manage.py test; Remove-Item Env:DB_ENGINE
```

## Publicar en internet
Necesitas un servidor con Python (VPS), MySQL, un dominio y HTTPS. En el `.env` de producción:
```
DJANGO_DEBUG=0
SECRET_KEY=<una cadena larga nueva>
ALLOWED_HOSTS=tudominio.es,www.tudominio.es
CSRF_TRUSTED_ORIGINS=https://tudominio.es,https://www.tudominio.es
TRUST_PROXY=1
FORCE_HTTPS=1
```
Después:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
gunicorn config.wsgi
```
- Arranca `gunicorn` detrás de **Nginx**. El CSS, JS y tipografías los sirve la propia app (WhiteNoise).
- Las **fotos subidas** (`media/`) las sirve Nginx: `location /media/ { alias /ruta/al/proyecto/media/; }`.
- El límite de envíos del formulario se guarda en memoria de cada proceso: con varios workers de gunicorn el límite
  real es algo más alto (suficiente para una web pequeña).
- Haz **copias de seguridad** diarias de la base de datos y de la carpeta `media/`.

## Problemas frecuentes
- **`pip install` falla en `mysqlclient`**: actualiza pip (`python -m pip install -U pip`) y usa Python 3.12 o 3.13
  de 64 bits, que tienen paquetes ya compilados para Windows.
- **«No se encuentra Django»**: no has activado el entorno (`venv\Scripts\activate`).
- **`Access denied for user` / `Unknown database 'magia'`**: revisa `DB_USER` y `DB_PASSWORD` del `.env` y que hayas
  creado la base de datos (paso 2).
- **Los emails no llegan**: comprueba que `GMAIL_APP_PASSWORD` es una contraseña de aplicación (no la normal de Gmail)
  y mira la terminal: los errores de envío aparecen ahí. Los mensajes quedan guardados en el panel igualmente.
- **Las fotos no se ven en producción**: falta la regla `location /media/` de Nginx.
- **Error 400 en producción**: tu dominio no está en `ALLOWED_HOSTS`. **Error 403 al enviar el formulario**: falta en
  `CSRF_TRUSTED_ORIGINS`.

---

## Créditos
En este proyecto se usó [Claude Code](https://claude.com/claude-code) (Anthropic) como consultor para resolver errores de sintaxis y para subir el proyecto a GitHub.
