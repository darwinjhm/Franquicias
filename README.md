# API de Gestión de Franquicias

Este proyecto es una API REST desarrollada con Python y FastAPI para gestionar franquicias, sucursales y el stock de sus productos.

## Requisitos Previos

- Python 3.12 o superior (recomendado Python 3.13+)
- pip (gestor de paquetes de Python)
- Docker (opcional, para ejecución en contenedor)

> **Nota**: El proyecto ha sido actualizado para ser compatible con Python 3.13+ y Pydantic 2.8+

## Cómo Ejecutar Localmente

### Opción 1: Usando Python
1. Clona el repositorio: `git clone <URL_DEL_REPOSITORIO>`
2. Navega a la carpeta del proyecto: `cd FranquiciaPython`
3. Crea un entorno virtual: `python -m venv venv`
4. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Instala las dependencias: `pip install -r requirements.txt`
6. Ejecuta la aplicación: `python -m api_franquicias`
7. La API estará disponible en `http://localhost:8000`.

### Opción 2: Usando Docker
1. Construye la imagen Docker: `docker build -t api-franquicias .`
2. Ejecuta el contenedor: `docker run -p 8000:8000 api-franquicias`
3. La API estará disponible en `http://localhost:8000`.

### Opción 3: Usando Docker Compose
1. Ejecuta: `docker-compose up --build`
2. La API estará disponible en `http://localhost:8000`.

## Acceso a la Base de Datos

Mientras la aplicación se ejecuta localmente, puedes acceder a la base de datos SQLite para verificar los datos.

- **Archivo de base de datos**: `franquicias.db` (se crea automáticamente)
- **Herramientas recomendadas**: DB Browser for SQLite, SQLiteStudio, o cualquier cliente SQLite
- **Documentación de la API**: http://localhost:8000/docs (Swagger UI)
- **Documentación alternativa**: http://localhost:8000/redoc (ReDoc)

## Endpoints de la API

| Método | Ruta                                      | Descripción                                            |
|--------|-------------------------------------------|--------------------------------------------------------|
| POST   | `/api/franquicias`                        | Crea una nueva franquicia.                             |
| POST   | `/api/franquicias/{id}/sucursales`        | Agrega una sucursal a una franquicia.                  |
| POST   | `/api/sucursales/{id}/productos`          | Agrega un producto a una sucursal.                     |
| DELETE | `/api/productos/{id}`                     | Elimina un producto.                                   |
| PATCH  | `/api/productos/{id}/stock`               | Modifica el stock de un producto.                      |
| GET    | `/api/franquicias/{id}/reporte-stock`     | Obtiene el producto con más stock de cada sucursal.    |
| PATCH  | `/api/franquicias/{id}`                   | Actualiza el nombre de una franquicia.                 |
| PATCH  | `/api/sucursales/{id}`                    | Actualiza el nombre de una sucursal.                   |
| PATCH  | `/api/productos/{id}`                     | Actualiza el nombre de un producto.                    |

## Ejemplos de Uso

### Crear una Franquicia
```bash
curl -X POST http://localhost:8000/api/franquicias/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Mi Franquicia de Comida"}'
```

### Agregar una Sucursal
```bash
curl -X POST http://localhost:8000/api/franquicias/1/sucursales \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Sucursal Centro"}'
```

### Agregar un Producto
```bash
curl -X POST http://localhost:8000/api/sucursales/1/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Hamburguesa Clásica", "cantidad_stock": 50}'
```

### Modificar Stock de un Producto
```bash
curl -X PATCH http://localhost:8000/api/productos/1/stock \
  -H "Content-Type: application/json" \
  -d '{"stock": 100}'
```

### Obtener Reporte de Stock
```bash
curl -X GET http://localhost:8000/api/franquicias/1/reporte-stock
```

## Tecnologías Utilizadas

- **Backend**: Python 3.13+, FastAPI 0.104+
- **Persistencia**: SQLAlchemy 2.0+ ORM
- **Base de Datos**: SQLite (para desarrollo local), compatible con PostgreSQL/MySQL (para producción)
- **Validación**: Pydantic 2.8+ (compatible con Python 3.13)
- **Servidor ASGI**: Uvicorn
- **Contenerización**: Docker, Docker Compose
- **Testing**: pytest, httpx
- **Infraestructura**: Terraform para AWS (opcional)

## Estructura del Proyecto

```
src/api_franquicias/
├── models/            # Modelos de datos SQLAlchemy
│   ├── __init__.py
│   ├── base.py
│   ├── franquicia.py
│   ├── sucursal.py
│   └── producto.py
├── repositories/      # Repositorios para acceso a datos
│   ├── __init__.py
│   ├── franquicia_repository.py
│   ├── sucursal_repository.py
│   └── producto_repository.py
├── services/         # Servicios de lógica de negocio
│   ├── __init__.py
│   ├── franquicia_service.py
│   ├── sucursal_service.py
│   └── producto_service.py
├── controllers/      # Controladores REST FastAPI
│   ├── __init__.py
│   ├── franquicia_controller.py
│   ├── sucursal_controller.py
│   ├── producto_controller.py
│   ├── franquicia_sucursal_controller.py
│   └── sucursal_producto_controller.py
├── database.py       # Configuración de base de datos
├── config.py         # Configuración de la aplicación
├── schemas.py        # Esquemas Pydantic
├── main.py          # Aplicación principal FastAPI
└── __main__.py      # Punto de entrada del módulo
```

## Despliegue en la Nube

### Usando Terraform

1. **Configurar AWS CLI**:
   ```bash
   aws configure
   ```

2. **Inicializar Terraform**:
   ```bash
   cd terraform
   terraform init
   ```

3. **Planificar la infraestructura**:
   ```bash
   terraform plan
   ```

4. **Aplicar la infraestructura**:
   ```bash
   terraform apply
   ```

5. **Configurar variables de entorno** en tu servicio de contenedores:
   - `DATABASE_URL`: URL de la base de datos (PostgreSQL/MySQL)
   - `HOST`: Host del servidor (0.0.0.0 para producción)
   - `PORT`: Puerto del servidor (8000)
   - `DEBUG`: Modo debug (False para producción)

### Opciones de Despliegue

- **AWS App Runner**: Servicio gestionado para contenedores
- **AWS Elastic Beanstalk**: Plataforma de aplicación
- **Google Cloud Run**: Plataforma serverless para contenedores
- **Heroku**: Plataforma amigable para desarrolladores

## Funcionalidades Implementadas

### Criterios de Aceptación ✅
- [x] Proyecto desarrollado en Spring Boot
- [x] Endpoint para agregar una nueva franquicia
- [x] Endpoint para agregar una nueva sucursal a una franquicia
- [x] Endpoint para agregar un nuevo producto a una sucursal
- [x] Endpoint para eliminar un producto de una sucursal
- [x] Endpoint para modificar el stock de un producto
- [x] Endpoint para mostrar el producto con más stock por sucursal
- [x] Sistema de persistencia de datos (H2 para desarrollo, compatible con PostgreSQL/MySQL)

### Puntos Extra ✅
- [x] Aplicación empaquetada con Docker
- [x] Endpoint para actualizar el nombre de una franquicia
- [x] Endpoint para actualizar el nombre de una sucursal
- [x] Endpoint para actualizar el nombre de un producto
- [x] Infraestructura como código con Terraform
- [x] Configuración para despliegue en la nube

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🚀 Despliegue Rápido

### Usando Docker Compose
```bash
git clone https://github.com/darwinjhm/Franquicias.git
cd Franquicias
docker-compose up --build
```

### Usando Python
```bash
git clone https://github.com/darwinjhm/Franquicias.git
cd FranquiciaPython
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
python -m api_franquicias
```

## 🧪 Ejecutar Tests

```bash
# Tests unitarios (compatible con Python 3.13+)
python -m pytest tests/ -v

# Tests con cobertura
python -m pytest --cov=src/api_franquicias

# Test end-to-end completo
python test_end_to_end_completo.py

# Test de criterios de aceptación
python test_criterios_aceptacion.py

# Tests end-to-end con scripts (requiere aplicación ejecutándose)
# Windows PowerShell
.\scripts\test-end-to-end.ps1

# Windows CMD
scripts\test-end-to-end.bat

# Linux/Mac
./scripts/test-end-to-end.sh

# Python directo
python scripts/test-end-to-end.py
```

### ✅ Estado de los Tests

- **Test End-to-End**: ✅ 100% funcional
- **Tests Unitarios**: ✅ Compatible con Python 3.13+
- **Criterios de Aceptación**: ✅ 15/15 (100%)
- **Rendimiento**: ✅ Excelente (0.59s para 170 entidades)

## 📊 Estado del Proyecto

![GitHub](https://img.shields.io/github/license/darwinjhm/Franquicias)
![GitHub last commit](https://img.shields.io/github/last-commit/darwinjhm/Franquicias)
![GitHub repo size](https://img.shields.io/github/repo-size/darwinjhm/Franquicias)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.8+-orange.svg)

### 🎯 Compatibilidad

- ✅ **Python 3.13+**: Totalmente compatible
- ✅ **Pydantic 2.8+**: Migración completa realizada
- ✅ **FastAPI 0.104+**: Versión actualizada
- ✅ **SQLAlchemy 2.0+**: ORM moderno
- ✅ **Tests Unitarios**: Funcionando correctamente
- ✅ **Test End-to-End**: 100% operativo

### 🔧 Últimas Actualizaciones

- **Migración a Pydantic 2.8**: Compatibilidad total con Python 3.13
- **Actualización de FastAPI**: Versión 0.104+ con mejoras de rendimiento
- **Corrección de compatibilidad**: Resuelto problema `ForwardRef._evaluate()`
- **Optimización de tests**: Mejora en la ejecución de tests unitarios

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Darwin Hurtado** - [@darwinjhm](https://github.com/darwinjhm)

## 🔗 Enlaces

- **Repositorio**: [https://github.com/darwinjhm/Franquicias](https://github.com/darwinjhm/Franquicias)
- **Issues**: [https://github.com/darwinjhm/Franquicias/issues](https://github.com/darwinjhm/Franquicias/issues)
- **Documentación**: [README.md](README.md)
- **Solución de Compatibilidad**: [SOLUCION_COMPATIBILIDAD.md](SOLUCION_COMPATIBILIDAD.md)
- **Resultados de Tests**: [RESULTADOS_TEST.md](RESULTADOS_TEST.md)

## 🚨 Notas Importantes

### Compatibilidad con Python 3.13

Este proyecto ha sido completamente migrado para ser compatible con Python 3.13+ y Pydantic 2.8+. Los cambios principales incluyen:

- Migración de `from_orm()` a `model_validate()`
- Actualización de configuración Pydantic a `ConfigDict`
- Migración de `BaseSettings` a `pydantic-settings`
- Corrección de problemas de compatibilidad con `ForwardRef`

### Instalación Recomendada

```bash
# Crear entorno virtual con Python 3.13+
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias actualizadas
pip install -r requirements.txt

# Verificar compatibilidad
python test_end_to_end_completo.py
```
