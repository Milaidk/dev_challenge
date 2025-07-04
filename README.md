![👀](./core/static/images/imageapp.png)
# 🚌 Proyecto Transporte Sostenible

Este proyecto es una **plataforma de transporte sostenible** construida con Django. Permite que **conductores registren rutas** y que **pasajeros las reserven** desde un panel personalizado. El sistema incluye funcionalidades de **registro, login y control de acceso** para ambos roles, manteniendo una experiencia clara y diferenciada para cada tipo de usuario.

---

## 🚀 Funcionalidades principales

🔐 **Autenticación**:
- Registro y login para usuarios.
- Redirección de paneles según el tipo de usuario (pasajero o conductor).

🚗 **Panel de conductor**:
- Agregar nuevas rutas de transporte con origen, destino, horario y capacidad.
- Visualizar las rutas registradas.

🧍 **Panel de pasajero**:
- Explorar rutas disponibles.
- Realizar reservas.
- Visualizar las rutas reservadas.

🛠️ **Admin de Django**:
- Control interno de usuarios y rutas desde el panel de administración.

---

## 📦 Construido con

✔️ `Python` + `Django` para la lógica de backend.  
✔️ `HTML5` para la estructura de la interfaz.  
✔️ `CSS3` + `Bootstrap 5` para diseño responsivo y moderno.  
✔️ `SQLite3` como motor de base de datos local.  

---

## 🏗️ Estructura del proyecto
```
dev_challenge/
├── core/ # App principal: lógica del sistema
│ ├── static/ # Archivos estáticos como CSS
│ │ └── styles.css
│ ├── templates/ # Plantillas HTML
│ ├── templatetags/ # Filtros o tags personalizados
│ ├── admin.py # Registro de modelos en admin
│ ├── apps.py # Configuración de app
│ ├── forms.py # Formularios personalizados
│ ├── models.py # Definición de modelos: Rutas, Usuarios
│ ├── views.py # Vistas para lógica de negocio
│ └── ...
├── TinUdriv/ # Configuración principal del proyecto
│ ├── settings.py # Configuración global
│ ├── urls.py # Rutas generales del proyecto
│ └── ...
├── db.sqlite3 # Base de datos local
├── manage.py # Script de gestión Django
└── requirements.txt # Librerías necesarias
```
## Gratitud 🎁
* Gracias [👀 MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django) para el uso de los estilos y colores.
* Gracias [👀 Boodtrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/) para el resurso de logia JS.

## ⚙️ Configuración y Puesta en Marcha - Proyecto Django (Windows)

Como configurar, activar y ejecutar correctamente el proyecto Django en un entorno **Windows** y **linux**

---

## 🎯 Requisitos Previos

- Tener instalado **Python 3.10 o superior**.
- SQLite

---

## 🔧 Instalación del entorno virtual

### Ubuntu Linux / MacOS
Instalación de gestor de ambientes virtuales de Python
~~~
sudo apt install python3-venv
~~~
Creación del ambiente virtual
~~~
python3 -m venv .venv
~~~
Activación del ambiente virtual
~~~
source .venv/bin/activate
~~~
Instalación de dependencias de este proyecto
~~~
pip3 install -r requirements.txt
~~~
En caso de querer desactivar el ambiente usar
~~~
deactivate
~~~

### Windows
Instalación de gestor de ambientes virtuales de Python
~~~
pip install virtualenv
~~~
Creación del ambiente virtual
~~~
py -m venv .venv
~~~
Activación del ambiente virtual para CMD
~~~
.venv\Scripts\activate
~~~
Activación del ambiente virtual para PowerShell
~~~
.venv\Scripts\activate.ps1
~~~
Instalación de dependencias de este proyecto
~~~
pip install -r requirements.txt
~~~
En caso de querer desactivar el ambiente usar
~~~
deactivate
~~~
### Iniciar servidor
#### Linux o MacOS
~~~
python3 manage.py runserver
~~~
#### Windows
~~~
python manage.py runserver
~~~

Una vez inicializado el servidor se deberá dirigir al siguiente enlace: <http://localhost:8000>