# Axanet — Gestor de Clientes

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-enabled-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Aplicación CLI en **Python** para gestionar archivos de clientes usando **diccionarios (tablas hash)** como índice. Incluye integración completa con **GitHub Actions** para notificaciones automáticas al equipo.

## Características Principales

**CRUD Completo**: Crear, actualizar, consultar, listar y eliminar clientes
**Índice Eficiente**: Búsquedas rápidas con tabla hash (`index.json`)
**Historial de Acciones**: Rastreo completo de cambios por cliente
**CLI Intuitiva**: Comandos fáciles de recordar y usar
**GitHub Actions**: 3 workflows automáticos para notificaciones
**Git Integration**: Commits automáticos con etiquetas especiales
**Búsqueda Avanzada**: Buscar por nombre, servicio o notas
**Estadísticas**: Métricas de uso y actividad

## Estructura del Proyecto
```
axanet-app/
├─ app.py                      # CLI principal
├─ axanet_manager.py           # Lógica de negocio
├─ team.json                   # Configuración del equipo
├─ requirements.txt            # Dependencias
├─ data/
│  ├─ index.json               # Índice (tabla hash)
│  └─ clients/                 # Archivos JSON por cliente
├─ .github/
│  └─ workflows/
│     ├─ notify-new-client.yml      # Workflow nuevo cliente
│     ├─ notify-update-client.yml   # Workflow actualización
│     └─ notify-consult-client.yml  # Workflow consulta
└─ docs/
   └─ diagrama-flujo.md        # Documentación técnica
```

## Requisitos del Sistema

- **Python**: 3.10 o superior
- **Git**: Para funcionalidad `--git` y `--push`
- **GitHub**: Repositorio con Actions habilitado

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/al05089397-spec/axanet-app.git
cd axanet-app
```

### 2. Configurar el equipo

Edita `team.json` con los handles reales de tu equipo:
```json
{
  "members": [
    { "name": "Alex Desarrollador", "github": "@alex-dev-2024" },
    { "name": "Sofia QA", "github": "@sofia-qa-lead" }
  ]
}
```

### 3. Crear estructura de datos
```bash
mkdir -p data/clients
echo '{}' > data/index.json
```

## Uso de la Aplicación

### Comandos Básicos
```bash
# Crear cliente
python app.py create --name "María García" --service "Desarrollo Web" --notes "Proyecto e-commerce"

# Actualizar cliente
python app.py update --name "María García" --service "SEO + Desarrollo" --notes "Fase 2 del proyecto"

# Consultar cliente
python app.py consult --name "María García"

# Listar todos los clientes
python app.py list

# Buscar clientes
python app.py search --query "desarrollo"

# Ver estadísticas
python app.py stats

# Eliminar cliente
python app.py delete --name "María García"
```

### Integración con Git
```bash
# Con commit automático
python app.py create --name "Cliente Nuevo" --service "Consultoría" --git

# Con commit y push
python app.py update --name "Cliente Existente" --service "Nuevo servicio" --git --push
```

## GitHub Actions - Workflows Automáticos

### Workflow 1: Nuevo Cliente
- **Trigger**: Commit con `[NEW_CLIENT] name=...`
- **Acciones**: 
  - Crea resumen en Actions
  - Notifica al equipo
  - Genera checklist de seguimiento

### Workflow 2: Actualización Cliente
- **Trigger**: Commit con `[UPDATE_CLIENT] name=...`
- **Acciones**:
  - Analiza cambios realizados
  - Muestra historial del cliente
  - Notifica cambios al equipo
  - Sugiere acciones de seguimiento

### Workflow 3: Consulta Cliente
- **Trigger**: Commit con `[CONSULT_CLIENT] name=...`
- **Acciones**:
  - Registra la consulta
  - Genera estadísticas de acceso
  - Log de auditoría

## Ejemplos de Uso

### Flujo Completo de Cliente
```bash
# 1. Crear cliente nuevo
python app.py create --name "TechCorp SA" --service "Cloud Migration" --notes "Migración a AWS Q1-2024" --git --push

# 2. Consultar información
python app.py consult --name "TechCorp SA" --git

# 3. Actualizar con nuevo servicio
python app.py update --name "TechCorp SA" --service "Cloud + DevOps" --notes "Agregado CI/CD pipeline" --git --push

# 4. Ver historial completo
python app.py consult --name "TechCorp SA"
```

### Gestión de Múltiples Clientes
```bash
# Ver todos los clientes
python app.py list

# Buscar por servicio específico
python app.py search --query "cloud"

# Ver estadísticas generales
python app.py stats
```

## Características Técnicas

### Algoritmos y Estructuras de Datos
- **Tabla Hash**: Índice principal para O(1) lookups
- **JSON Storage**: Archivos individuales por cliente
- **Historial Secuencial**: Array de acciones ordenado por timestamp

### Validaciones y Seguridad
- Validación de nombres de archivo seguros
- Manejo de errores robusto
- Backups automáticos del índice
- Verificación de integridad de datos

### Performance
- Búsquedas instantáneas por nombre de cliente
- Carga lazy de archivos de datos
- Índice en memoria para operaciones rápidas

## GitHub Actions en Detalle

### Configuración de Notificaciones

En `team.json` puedes configurar:
```json
{
  "notifications": {
    "new_client": {
      "enabled": true,
      "mention_team": true
    },
    "update_client": {
      "enabled": true,
      "mention_team": true
    },
    "consult_client": {
      "enabled": true,
      "mention_team": false
    }
  }
}
```

## Desarrollo y Contribuciones

### Estructura del Código

- `axanet_manager.py`: Lógica de negocio principal
- `app.py`: Interfaz CLI y comandos
- `.github/workflows/`: Definiciones de GitHub Actions

### Testing Local
```bash
# Crear cliente de prueba
python app.py create --name "Cliente Test" --service "Prueba" --notes "Testing"

# Verificar estructura de datos
cat data/index.json
ls -la data/clients/
```

## Métricas y Estadísticas

La aplicación rastrea:
- Total de clientes activos
- Consultas realizadas por cliente
- Historial de cambios completo
- Estadísticas de uso diario/semanal

## Seguridad y Respaldos

- Archivos JSON individuales evitan pérdida masiva de datos
- Índice se regenera automáticamente si se corrompe
- Historial inmutable de todas las operaciones
- Git como sistema de respaldo automático

## Soporte y Documentación

- **Documentación**: Ver carpeta `docs/` para detalles técnicos
- **Workflows**: Los Actions incluyen documentación integrada

## Beneficios del Sistema

### Para Desarrolladores
- Código limpio y bien documentado
- Arquitectura escalable y modular
- Testing y CI/CD integrado

### Para el Equipo
- Notificaciones automáticas en tiempo real
- Seguimiento transparente de cambios
- Métricas de rendimiento continuo

### Para el Negocio
- Gestión centralizada de clientes
- Historial completo de interacciones
- Reportes automáticos de actividad

---

## Licencia

MIT License - ver archivo `LICENSE` para detalles.

## 👥 Equipo

Desarrollado para **TecMilenio** como proyecto académico de Desarrollo de Software.

---