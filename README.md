# 📚 Taller de Lenguajes de Programación - Python

Este repositorio contiene el desarrollo completo del taller de TDD y APIs con Python.

## 📁 Estructura del Proyecto

```
taller_tlp_python/
├── README.md                    # Este archivo (documentación general)
├── requirements.txt             # Dependencias de Python
├── .gitignore                  # Archivos a ignorar en Git
└── primer_punto/               # 🎯 PUNTO 1: Sistema de Gestión de Libros
    ├── manage.py               # Comando principal de Django
    ├── config/                 # Configuración del proyecto Django
    ├── books/                  # App principal con modelos, vistas, etc.
    └── venv/                   # Entorno virtual de Python
```

---

# 📚 Primer Punto: Sistema de Gestión de Libros - API REST con Django

Este primer punto implementa una aplicación completa de gestión de libros siguiendo los principios de **TDD (Test-Driven Development)** y **API REST** utilizando Django y Django REST Framework.

## 🎯 Funcionalidades Implementadas

### 📖 Casos de Uso Principales

1. **Gestión de Libros (CRUD)**
   - ✅ Listado de libros con filtros avanzados
   - ✅ Creación de nuevos libros con validaciones
   - ✅ Actualización de información de libros
   - ✅ Eliminación de libros (soft delete)

2. **Gestión de Categorías**
   - ✅ Listado de categorías de libros
   - ✅ Creación de nuevas categorías
   - ✅ Eliminación de categorías (soft delete)

3. **Sistema de Descuentos y Transformaciones**
   - ✅ Aplicar descuentos a libros específicos
   - ✅ Modificar precios y ofertas especiales
   - ✅ Actualizar stock de libros
   - ✅ Gestionar disponibilidad de productos

### 🛠️ Características Técnicas

- **TDD**: 21 pruebas unitarias cubren todos los casos de uso
- **API REST**: Endpoints completamente documentados con Swagger
- **Validaciones**: Validaciones robustas en modelos y serializers
- **Filtros**: Búsqueda avanzada por múltiples criterios
- **Interfaz Web**: Dashboard moderno con Tailwind CSS
- **Documentación**: API autodocumentada con OpenAPI/Swagger

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Git
- pip (gestor de paquetes de Python)

### 📥 Instalación Paso a Paso

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/taller_tlp_python.git
cd taller_tlp_python
```

2. **Entrar al directorio del primer punto**
```bash
cd primer_punto
```

3. **Crear y activar entorno virtual**
```bash
# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

4. **Instalar dependencias**
```bash
# Volver a la raíz para acceder a requirements.txt
cd ..
pip install -r requirements.txt

# Regresar al primer punto
cd primer_punto
```

5. **Configurar base de datos**
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

6. **Crear datos de ejemplo**
```bash
# Generar datos de muestra (recomendado)
python manage.py create_sample_data

# O si quieres limpiar datos existentes y crear nuevos:
python manage.py create_sample_data --clear
```

7. **Crear superusuario** (opcional)
```bash
python manage.py createsuperuser
```

8. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

9. **¡Listo! Visita la aplicación**
   - 🌐 **Interfaz principal**: http://localhost:8000/
   - 📚 **Gestión de libros**: http://localhost:8000/books/
   - 📂 **Gestión de categorías**: http://localhost:8000/categories/
   - 🔧 **Panel admin**: http://localhost:8000/admin/
   - 📖 **API docs**: http://localhost:8000/api/docs/

## 🛠️ Comandos Útiles

> **📁 Nota**: Todos los comandos de Django deben ejecutarse desde la carpeta `primer_punto/`

### 📊 Gestión de Datos

```bash
# Asegúrate de estar en primer_punto/
cd primer_punto

# Crear datos de ejemplo (recomendado para nuevas instalaciones)
python manage.py create_sample_data

# Limpiar base de datos y crear datos frescos
python manage.py create_sample_data --clear

# Ver ayuda del comando
python manage.py create_sample_data --help
```

### 🧪 Pruebas

```bash
# Asegúrate de estar en primer_punto/
cd primer_punto

# Ejecutar todas las pruebas
python manage.py test

# Ejecutar solo pruebas de la app books
python manage.py test books

# Ejecutar con más detalle
python manage.py test --verbosity=2
```

### 🔧 Desarrollo

```bash
# Asegúrate de estar en primer_punto/
cd primer_punto

# Crear nuevas migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate

# Crear superusuario para panel admin
python manage.py createsuperuser

# Abrir shell interactivo de Django
python manage.py shell

# Verificar configuración del proyecto
python manage.py check
```

### 📦 Despliegue

```bash
# Asegúrate de estar en primer_punto/
cd primer_punto

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic

# Verificar configuración para producción
python manage.py check --deploy
```

## 📝 Dependencias del Proyecto

```txt
Django==5.2.4
djangorestframework==3.16.0
django-filter==25.1
drf-spectacular==0.28.0
```

> **Nota**: El archivo `requirements.txt` contiene todas las dependencias con sus versiones exactas.

## 🌐 Endpoints de la API

### 📚 Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/books/` | Listar todos los libros |
| `POST` | `/api/books/` | Crear nuevo libro |
| `GET` | `/api/books/{id}/` | Obtener detalle de libro |
| `PUT` | `/api/books/{id}/` | Actualizar libro completo |
| `PATCH` | `/api/books/{id}/` | Actualizar libro parcial |
| `DELETE` | `/api/books/{id}/` | Eliminar libro (soft delete) |

### 🎯 Acciones Especiales de Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/books/{id}/apply_discount/` | Aplicar descuento |
| `POST` | `/api/books/{id}/update_stock/` | Actualizar stock |
| `POST` | `/api/books/{id}/remove_discount/` | Remover descuento |
| `GET` | `/api/books/discounted_books/` | Listar libros con descuento |
| `GET` | `/api/books/low_stock/` | Listar libros con stock bajo |
| `GET` | `/api/books/by_category/` | Agrupar libros por categoría |
| `GET` | `/api/books/search_advanced/` | Búsqueda avanzada |

### 📂 Categorías

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/categories/` | Listar categorías |
| `POST` | `/api/categories/` | Crear nueva categoría |
| `GET` | `/api/categories/{id}/` | Obtener detalle de categoría |
| `PUT` | `/api/categories/{id}/` | Actualizar categoría |
| `DELETE` | `/api/categories/{id}/` | Eliminar categoría (soft delete) |
| `GET` | `/api/categories/{id}/books/` | Libros de una categoría |

## 🎨 Interfaz Web

### Acceso a la Interfaz
- **Lista de Libros**: `http://localhost:8000/books/`
- **Lista de Categorías**: `http://localhost:8000/categories/`
- **Página Principal**: `http://localhost:8000/` *(redirige a libros)*

### Características de la Interfaz
- 📱 **Diseño responsive** con Tailwind CSS
- 🔍 **Filtros de búsqueda** en tiempo real
- 📊 **Dashboard con estadísticas** (total, descuentos, stock bajo)
- 💰 **Gestión visual de descuentos** con modales
- 📦 **Control de stock** integrado
- ✨ **Notificaciones toast** para feedback de acciones
- ➕ **CRUD completo** con modales para crear/editar
- 🗑️ **Eliminación segura** con confirmación
- 📝 **Formularios validados** con mensajes de error
- 🎨 **Iconos intuitivos** para acciones rápidas

### 🛠️ Funcionalidades CRUD en la Interfaz Web

#### 📖 Gestión de Libros
- **➕ Crear Libro**: Modal con formulario completo
  - Validación de ISBN único
  - Selección de categoría
  - Campos obligatorios marcados
  - Previsualización de descuentos
  
- **✏️ Editar Libro**: Modal precargado con datos existentes
  - Todos los campos editables
  - Validaciones en tiempo real
  - Actualización inmediata en la lista

- **🗑️ Eliminar Libro**: Confirmación con modal
  - Soft delete (marca como no disponible)
  - Confirmación antes de eliminar
  - Actualización automática de estadísticas

- **🔧 Acciones Rápidas**:
  - 📖 Ver detalles (abre API endpoint)
  - 💰 Aplicar descuento personalizado
  - 📦 Actualizar stock (positivo/negativo)

#### 📂 Gestión de Categorías
- **➕ Crear Categoría**: Modal simple y eficiente
  - Nombre único requerido
  - Descripción opcional
  - Estado activo/inactivo

- **✏️ Editar Categoría**: Modificar información existente
  - Cambiar nombre y descripción
  - Activar/desactivar categoría

- **❌ Desactivar Categoría**: Soft delete seguro
  - Modal de confirmación
  - Reversible (se puede reactivar)
  - No afecta libros existentes

- **✅ Reactivar Categoría**: Restaurar categorías inactivas

## 📚 Documentación de la API

### Swagger UI
Accede a la documentación interactiva en:
```
http://localhost:8000/api/docs/
```

### ReDoc
Documentación alternativa en:
```
http://localhost:8000/api/redoc/
```

### Schema OpenAPI
```
http://localhost:8000/api/schema/
```

## 🧪 Pruebas Unitarias

### Ejecutar todas las pruebas
```bash
python manage.py test books
```

### Cobertura de Pruebas
- ✅ **21 pruebas unitarias** cubren todos los casos de uso
- ✅ **Modelos**: Validaciones y métodos personalizados
- ✅ **APIs**: Todos los endpoints CRUD y acciones especiales
- ✅ **Funcionalidades**: Descuentos, stock, filtros

### Ejemplos de Pruebas Implementadas
```python
# Pruebas de modelos
def test_book_creation(self)
def test_apply_discount_valid(self)
def test_update_stock_positive(self)

# Pruebas de API
def test_create_book_api(self)
def test_apply_discount_api(self)
def test_list_books_api(self)
```

## 📊 Datos de Ejemplo

El proyecto incluye un comando personalizado para generar datos de muestra realistas:

### 📚 Contenido Incluido
- **8 Categorías**: Ficción, Tecnología, Ciencia, Historia, Filosofía, Arte, Biografías, Negocios
- **12 Libros**: Incluyendo clásicos y títulos modernos
- **6 Libros con descuento**: Para probar funcionalidades de ofertas (5% a 30% OFF)
- **3 Libros con stock bajo**: Para alertas de inventario (≤3 unidades)
- **Datos realistas**: ISBNs válidos, fechas de publicación reales, descripciones detalladas

### 🎯 Ejemplos de Libros Incluidos
- **Ficción**: "Cien años de soledad", "Don Quijote de la Mancha"
- **Tecnología**: "Clean Code", "Python Crash Course", "Django for Professionals"
- **Ciencia**: "El origen de las especies", "Una breve historia del tiempo"
- **Historia**: "Sapiens: De animales a dioses"
- **Filosofía**: "Así habló Zaratustra", "El arte de la guerra"
- **Biografías**: "Steve Jobs" por Walter Isaacson

### ⚡ Comando Rápido
```bash
# Generar todos los datos de ejemplo
python manage.py create_sample_data
```

> **💡 Tip**: Los datos se generan automáticamente con el comando `create_sample_data`, no necesitas configuración adicional.

## 🔧 Panel de Administración

Accede al panel de administración de Django en:
```
http://localhost:8000/admin/
```

### Funcionalidades del Admin
- 📚 Gestión completa de libros y categorías
- 📊 Estadísticas de inventario
- 🔍 Filtros y búsquedas avanzadas
- 📝 Campos de solo lectura calculados

## 🚀 Despliegue

### Configuraciones para Producción

1. **Variables de entorno**
```bash
export DEBUG=False
export SECRET_KEY="tu-clave-secreta-segura"
export ALLOWED_HOSTS="tudominio.com"
```

2. **Base de datos**
- SQLite para desarrollo (incluida)
- PostgreSQL recomendada para producción

3. **Archivos estáticos**
```bash
python manage.py collectstatic
```

## 📁 Estructura Detallada del Primer Punto

```
primer_punto/               # 🎯 PRIMER PUNTO: Django + TDD + API REST
├── config/                 # Configuración del proyecto Django
│   ├── settings.py         # Configuraciones principales
│   ├── urls.py            # URLs principales con api/
│   └── wsgi.py            # WSGI para despliegue
├── books/                  # App principal de libros
│   ├── models.py          # Modelos Book y Category
│   ├── serializers.py     # Serializers para API REST
│   ├── views.py           # ViewSets y vistas de templates
│   ├── urls.py            # URLs de la app con endpoints
│   ├── admin.py           # Configuración del admin
│   ├── tests.py           # 21 pruebas unitarias (TDD)
│   ├── management/        # Comandos personalizados de Django
│   │   └── commands/
│   │       └── create_sample_data.py  # Comando para datos de ejemplo
│   └── templates/         # Templates con Tailwind CSS
│       └── books/
│           ├── base.html      # Template base
│           ├── book_list.html # Lista de libros
│           └── category_list.html # Lista de categorías
├── venv/                  # Entorno virtual de Python
└── manage.py              # Comando de gestión de Django
```

## 🎯 Casos de Uso Cubiertos

### ✅ Requerimientos Cumplidos

1. **3+ Casos de uso implementados**:
   - Gestión de libros (CRUD)
   - Gestión de categorías
   - Sistema de descuentos y stock

2. **Funcionalidades obligatorias**:
   - ✅ Listado de entidades (libros y categorías)
   - ✅ Inserción/creación de entidades
   - ✅ Eliminación de recursos (soft delete)
   - ✅ Transformación de recursos (descuentos, stock)

3. **TDD implementado**:
   - ✅ Requisitos definidos antes del desarrollo
   - ✅ Casos y pruebas unitarias creadas primero
   - ✅ Implementación siguiendo las pruebas

4. **API REST completa**:
   - ✅ Framework Django REST Framework
   - ✅ Documentación con Swagger
   - ✅ Endpoints RESTful bien diseñados

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ve el archivo [LICENSE](LICENSE) para más detalles.

## 📦 Preparar para GitHub

### 🔧 Archivos incluidos para GitHub
- ✅ `.gitignore` configurado para Django
- ✅ `requirements.txt` actualizado
- ✅ `README.md` completo con instrucciones
- ✅ Comando `create_sample_data` para datos de ejemplo
- ✅ 21 pruebas unitarias funcionando

### 🚀 Pasos para subir a GitHub

1. **Inicializar repositorio Git**
```bash
git init
git add .
git commit -m "Initial commit: Django Books Management System with TDD"
```

2. **Crear repositorio en GitHub** y conectarlo
```bash
git remote add origin https://github.com/tu-usuario/taller_tlp_python.git
git branch -M main
git push -u origin main
```

3. **Instrucciones para colaboradores**
```bash
# Clonar el proyecto
git clone https://github.com/tu-usuario/taller_tlp_python.git
cd taller_tlp_python

# Entrar al primer punto
cd primer_punto

# Instalar y configurar
python -m venv venv
source venv/bin/activate  # Linux/Mac
cd .. && pip install -r requirements.txt && cd primer_punto
python manage.py migrate
python manage.py create_sample_data

# Ejecutar
python manage.py runserver
```

### 🎯 URLs de Demostración (una vez desplegado)
- 🏠 **Aplicación**: `http://localhost:8000/`
- 📚 **Gestión de Libros**: `http://localhost:8000/books/`
- 📂 **Categorías**: `http://localhost:8000/categories/`
- 📖 **API Docs**: `http://localhost:8000/api/docs/`

### 🏷️ Features para destacar en GitHub
- ✨ **TDD completo** con 21 pruebas unitarias
- 🎨 **Interfaz moderna** con Tailwind CSS
- 📱 **Responsive design** y UX intuitiva
- 🔧 **CRUD completo** en interfaz web
- 📊 **Dashboard con estadísticas** en tiempo real
- 🚀 **API REST documentada** con Swagger
- 🎯 **Casos de uso reales** del mundo empresarial

## 👨‍💻 Desarrollado por

Proyecto de **TDD y APIs** para el curso de Taller de Lenguajes de Programación.

**Tecnologías utilizadas:**
- Django 5.2.4
- Django REST Framework 3.16.0
- Tailwind CSS (CDN)
- Swagger/OpenAPI
- SQLite

**Arquitectura:**
- Patrón MVC/MVT
- API REST con ViewSets
- Soft delete para integridad de datos
- Validaciones robustas
- Tests unitarios (TDD)

---

¡Gracias por revisar este proyecto! 🚀

### 📊 Estadísticas del Primer Punto
- **Líneas de código**: ~2,000+
- **Archivos Python**: 15+
- **Templates HTML**: 3
- **Pruebas unitarias**: 21
- **Endpoints API**: 15+
- **Tiempo de desarrollo**: Implementado siguiendo TDD

---

## 🚧 Desarrollo del Taller

### ✅ Primer Punto: Sistema de Gestión de Libros (Completado)
- **📂 Ubicación**: `primer_punto/`
- **🛠️ Tecnología**: Django + Django REST Framework
- **🧪 Metodología**: TDD (Test-Driven Development)
- **🎨 Frontend**: Templates con Tailwind CSS
- **📊 Funcionalidades**: CRUD completo de libros y categorías

### 🔄 Segundo Punto: (Próximamente)
- **📂 Ubicación**: `segundo_punto/` *(será creado)*
- **🛠️ Tecnología**: Por definir
- **📋 Estado**: Pendiente de desarrollo

> **💡 Nota**: Este repositorio contiene el taller completo. Cada punto del taller se desarrolla en su propia carpeta para mantener una organización clara y modular. 