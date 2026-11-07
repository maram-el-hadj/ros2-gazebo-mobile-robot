# Robot mobile différentiel : ROS 2 Humble + Gazebo Fortress

Simulation d'un robot mobile à deux roues motrices, conçu entièrement à partir
de zéro (modèle SDF, monde, lidar, nœuds ROS 2) et piloté depuis ROS 2 via
`ros_gz_bridge`. Aucun robot réel n'est nécessaire.

## Fonctionnalités
- Modèle de robot différentiel (chassis, 2 roues motrices, 2 roues folles, lidar)
- Monde de simulation : pièce de 6 x 6 m avec un obstacle
- Pont ROS 2 ↔ Gazebo (`/cmd_vel`, `/odom`, `/scan`)
- Évitement d'obstacles avec lidar 2D (machine à états avec hystérésis)
- À venir : SLAM et navigation autonome (Nav2)

## Architecture
```
Gazebo Fortress (physique, robot, lidar)
      |  /scan, /odom         ^  /cmd_vel
      v                       |
        ros_gz_bridge
      |  /scan, /odom         ^  /cmd_vel
      v                       |
ROS 2 Humble : obstacle_avoider (et driver_node pour les tests)
```

| Topic | Type ROS 2 | Sens |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | ROS 2 → Gazebo |
| `/odom` | `nav_msgs/Odometry` | Gazebo → ROS 2 |
| `/scan` | `sensor_msgs/LaserScan` | Gazebo → ROS 2 |

## Structure du dépôt
```
robot_basics/
├── models/robot.sdf          # robot : chassis, roues, lidar, plugin DiffDrive
├── worlds/mon_monde.sdf      # monde : sol, murs, obstacle, plugins système
├── launch/robot.launch.py    # lance Gazebo + bridge
├── robot_basics/
│   ├── driver_node.py        # avance jusqu'à x = 2 m en lisant /odom
│   └── obstacle_avoider.py   # évitement d'obstacles avec /scan
├── docs/                     # captures d'écran
├── NOTES.md                  # notes d'apprentissage
└── setup.py / package.xml
```

## Prérequis
- Ubuntu 22.04, ROS 2 Humble, Gazebo Fortress (`ign gazebo`)
- `sudo apt install ros-humble-ros-gz`

## Installation
```bash
mkdir -p ~/maram_ws/src && cd ~/maram_ws/src
git clone https://github.com/maram-el-hadj/ros2-gazebo-mobile-robot.git robot_basics
cd ~/maram_ws
colcon build --symlink-install --packages-select robot_basics
source install/setup.bash
```

## Utilisation
Terminal 1 : simulation + bridge
```bash
ros2 launch robot_basics robot.launch.py
```
Terminal 2 : évitement d'obstacles
```bash
ros2 run robot_basics obstacle_avoider
```
Alternative de test (utilise `/odom`, s'arrête à x = 2 m) :
```bash
ros2 run robot_basics driver_node
```
Ne pas lancer les deux nœuds ensemble : ils publient tous les deux sur `/cmd_vel`.

Vérifications :
```bash
ros2 topic list
ros2 topic hz /scan
ros2 topic echo /odom --once
```

## Choix techniques
- **`ogre2`** comme moteur de rendu : nécessaire pour `gpu_lidar` (avec `ogre`, les mesures étaient fausses).
- **Stabilité** : deux roues folles, châssis bas et lourd, inerties explicites, accélérations limitées.
- **Performance** : pas de temps 4 ms, lidar 120 rayons, ombres désactivées.
- **Évitement** : 3 secteurs (devant, gauche, droite), seuils 0.7 m / 0.95 m (hystérésis), direction choisie une seule fois par virage.

## Limites connues
- Chemins absolus (`/home/maram/maram_ws/...`) dans `worlds/mon_monde.sdf` et le launch file.
- Le topic `/scan` est publié plus vite que les 10 Hz demandés (à investiguer).

## Aperçu
![Simulation](docs/gazebo_world.png)

## Roadmap
- [x] Étape 1 : robot différentiel (SDF + DiffDrive)
- [x] Étape 2 : monde, murs, obstacle, launch file
- [x] Étape 3 : bridge ROS 2 ↔ Gazebo, nœud de contrôle
- [x] Étape 4 : lidar + évitement d'obstacles
- [ ] Étape 5 : TF et odométrie
- [ ] Étape 6 : SLAM Toolbox
- [ ] Étape 7 : navigation avec Nav2
- [ ] Chemins portables

## Auteur
Maram El Hadj : [GitHub](https://github.com/maram-el-hadj)
