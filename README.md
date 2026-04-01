# PROYECTO MÓDULO V - DJANGO

## Datos del Estudiante:

- Roberto Carlos Olguin Ledezma
- Fecha: Marzo 2026

## 1. Propósito:

Demostrar los conocimientos adquiridos en la creación de un proyecto en Django.

## 2. Requerimientos:

- Cree un Proyecto en Django con al menos una Aplicación
- Su Aplicación debe tener al menos 4 Models (Modelos o Tablas)
- Sus Models deben contener al menos 2 validaciones personalizadas
- Su Administrador de Django debe tener al menos 2 Models registrados
- Utilice Django Rest Framework para crear al menos 3 ModelViewSet o GenericAPIView
- Utilice Django Rest Framework para crear al menos 1 Custom API
- Debe incluir el archivo requirements.txt en la raíz del repositorio

## 3. Implementación:

✅ **Proyecto Django:** `ecoapp` con aplicación `proyecto`  
✅ **4 Models:** `Persona`, `TipoTarea`, `Tarea`, `TareaAsignada` en app `proyecto`  
✅ **Validaciones personalizadas:** Fecha de nacimiento futura, rango de prioridad, fechas de tarea, email único  
✅ **Admin Django:** 4 models registrados con configuraciones personalizadas  
✅ **DRF ViewSets:** `PersonaViewSet`, `TipoTareaViewSet` en app `proyecto`  
✅ **Custom APIs:** `tareas_estadisticas`, `tareas_por_persona` en app `proyecto`  
✅ **requirements.txt:** Incluido con todas las dependencias necesarias

## Instalar dependencias

- Se recomienda utilizar un entorno virtual (virtualenv)

```sh
pip install -r requirements.txt
```

## Ejecutar servidor de desarrollo

```sh
python manage.py runserver
```

## Crear SuperAdministrador

```sh
python manage.py createsuperuser
```

## API Endpoints Disponibles:

### ViewSets (CRUD Operations):

- `GET/POST /proyecto/person` - Listar y crear personas
- `GET/PUT/DELETE /proyecto/person/{id}` - Detalle, actualizar y eliminar persona
- `GET/POST /proyecto/task-types` - Listar y crear tipos de tarea
- `GET/PUT/DELETE /proyecto/task-types/{id}` - Detalle, actualizar y eliminar tipo de tarea

### Custom APIs:

- `GET /proyecto/tasks-statistics` - Estadísticas generales de tareas (totales, completadas, pendientes, porcentaje)
- `GET /proyecto/person/{persona_id}/tasks` - Todas las tareas asignadas a una persona específica
  - **Parámetro opcional:** `?state=completed` o `?state=pending` para filtrar por estado
- `GET /proyecto/all-tasks` - Todas las tareas asignadas del sistema con información de personas
  - **Parámetro opcional:** `?state=completed` o `?state=pending` para filtrar por estado

### Frontend Interface:

- `GET /proyecto/tasks` - Interfaz web para gestión y visualización de tareas

### Parámetros de búsqueda y ordenamiento:

- **Personas:** `?search=nombre` `?ordering=apellido` `?ordering=nombre`
- **Tipos Tarea:** `?ordering=prioridad` `?ordering=nombre`

### Ejemplos de uso:

```bash
# Obtener todas las personas
curl http://localhost:8000/proyecto/person

# Buscar persona por nombre
curl http://localhost:8000/proyecto/person?search=Roberto

# Obtener estadísticas de tareas
curl http://localhost:8000/proyecto/tasks-statistics

# Obtener tareas de una persona específica
curl http://localhost:8000/proyecto/person/1/tasks

# Obtener tareas completadas de una persona específica
curl http://localhost:8000/proyecto/person/1/tasks?state=completed

# Obtener todas las tareas asignadas
curl http://localhost:8000/proyecto/all-tasks

# Obtener solo tareas pendientes
curl http://localhost:8000/proyecto/all-tasks?state=pending
```

### Autenticación:

- **AllowAny** (sin requerir autenticación para desarrollo)
- **Session Authentication** (para admin de Django user:admin / pass:admin)

Todos los endpoints tienen acceso público sin requerir autenticación.
http://localhost:8000/proyecto/tasks ver el Frontend de la siguiente manera
![img.png](img.png)