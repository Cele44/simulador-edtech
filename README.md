# Simulador_Lab - Plataforma Educativa Virtual (EdTech) 🧪

Proyecto académico desarrollado bajo la línea de producto **EdTech (Educational Technology)**, enfocado en la simulación interactiva de un laboratorio virtual utilizando arquitectura modular cliente-servidor.

---

# Tecnologías utilizadas

## Backend
- Python
- FastAPI
- MySQL
- SQLAlchemy

## Frontend
- Python
- Pygame

---

# Arquitectura del proyecto 🧫

```plaintext
SIMULADOR_LAB/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── frontend/
│   ├── escenas.py
│   ├── escenas_ui.py
│   ├── sesion_usuario.py
│   ├── reloj_simulacion.py
│   ├── objeto_lab.py
│   └── main.py
│
├── anexos/
└── README.md
```

---

# Características principales

- Simulación interactiva de laboratorio virtual
- Arquitectura modular frontend/backend
- Gestión de sesiones de usuario
- Sistema de escenas reutilizable
- Reloj de simulación
- Persistencia de datos con MySQL
- Separación de responsabilidades mediante servicios y repositorios

---

# Componentes reutilizables

## Backend
- Servicios (`services`)
- Repositorios (`repositories`)
- Modelos (`models`)
- Esquemas (`schemas`)

## Frontend
- Sistema de escenas
- Gestión de usuario
- Reloj de simulación

---

# Técnicas de refactorización aplicadas

- Extract Method
- Replace Magic Number
- Separación de responsabilidades
- Modularización cliente-servidor

---

# Instalación

## 1. Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

## 3. Activar entorno virtual

### Windows

```bash
.\venv\Scripts\Activate.ps1
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Base de datos

El sistema utiliza MySQL como gestor de base de datos.

Configurar las credenciales dentro del archivo:

```plaintext
backend/.env
```

# Autor

Maria Celeste 🫧
