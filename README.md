# Gazebo + ROS 2 Simulator

Simulador genérico para testear robots y mundos en Gazebo con ROS 2 Humble.

## Estructura

```
.
├── Dockerfile              # ROS 2 Humble + Gazebo
├── docker-compose.yaml     # Configuración Docker
└── src/
    ├── robots/             # Modelos de robots
    │   └── tugbot/
    ├── sim_launcher/       # Launch files parametrizables
    └── worlds/             # Mundos SDF
        ├── empty.sdf
        └── tugbot_warehouse.sdf
```

## Requisitos

- Docker
- Docker Compose
- X11 para GUI (opcional, se puede usar headless)

## Instalación & Uso

### Build

```bash
docker-compose build
```

### Lanzar

```bash
docker-compose up -d
```

### Ejecutar simulación

Opción A: Con GUI en X11
```bash
docker exec -it gazebo-dev bash
ros2 launch sim_launcher sim.launch.py robot:=tugbot world:=empty.sdf use_rviz:=true
```

Opción B: Headless (sin GUI)
```bash
docker exec gazebo-dev bash -lc \
  "ros2 launch sim_launcher sim.launch.py robot:=tugbot world:=tugbot_warehouse.sdf use_rviz:=false"
```

## Parámetros

### robot
- `tugbot` (default)
- Agregá más modelos en `src/robots/`

### world
- `empty.sdf` (default)
- `tugbot_warehouse.sdf`
- Agregá más mundos en `src/worlds/`

### use_rviz
- `true` (default) - Lanza RViz2
- `false` - Solo Gazebo

## Ejemplo

```bash
# Tugbot en warehouse con RViz
ros2 launch sim_launcher sim.launch.py \
  robot:=tugbot \
  world:=tugbot_warehouse.sdf \
  use_rviz:=true

# Otro robot en mundo vacío sin RViz
ros2 launch sim_launcher sim.launch.py \
  robot:=otro_robot \
  world:=empty.sdf \
  use_rviz:=false
```

## Bridge ROS ↔ Gazebo

El bridge se configura automáticamente via `src/robots/<robot>/config/bridge.yaml`

Ejemplo:
```yaml
- topic_name: /cmd_vel
  ros_type_name: geometry_msgs/msg/Twist
  gz_type_name: ignition.msgs.Twist
  direction: ros_to_gz
```

## Detener

```bash
docker-compose down
```

## Desarrollo

Cambios en `src/` se aplican automáticamente (volumen montado).

Nuevo paquete:
```bash
docker exec gazebo-dev bash -lc "colcon build --symlink-install"
```

## Status

✓ Funciona en Linux con Docker  
✓ GUI completa en X11  
✓ Modular (robots + mundos parametrizables)  
✓ Bridge ROS 2 ↔ Gazebo  

---

**Nota:** Para Jetson ARM64, cambiar base Docker a `dustynv/l4t-pytorch:r36.4.0`
