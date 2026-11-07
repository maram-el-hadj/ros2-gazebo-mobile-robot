# Notes du projet : robot mobile ROS 2 Humble + Gazebo Fortress

## Architecture
Gazebo (simulation physique) <-> ros_gz_bridge <-> ROS 2 (noeuds de controle)

## Etape 1 : Robot (models/robot.sdf)
- model = un objet, world = le monde complet
- link = piece solide, joint = liaison entre 2 links
- visual = ce qu'on voit, collision = forme utilisee par la physique, inertial = masse
- joint revolute = rotation (roues), joint ball = rotule (roue folle)
- Plugin DiffDrive: transforme cmd_vel (Twist) en vitesses de roues et publie /odom
- wheel_separation = distance entre roues (0.24 m), wheel_radius = rayon (0.1 m)
- Friction des roues (mu=1.0) pour l'adherence, friction nulle sur la roue folle
- Lancement: ign gazebo -r worlds/mon_monde.sdf

## Etape 2 : Monde, murs, launch file
- Le world contient : physique, 3 plugins systemes (Physics, UserCommands,
  SceneBroadcaster), lumiere, sol, murs, obstacle, et include du robot
- Murs et obstacle = models <static>true</static> : ils ne bougent pas,
  pas besoin d'inertial
- Piece de 6 m x 6 m, obstacle (boite) en (1.5, 1)
- Le robot s'arrete devant un mur : la collision fonctionne
- Launch file Python : lance plusieurs processus avec une seule commande
- setup.py > data_files copie launch/worlds/models dans install/
  (ros2 launch lit depuis install/)
- Erreur rencontree : "XMLDeclaration" = fichier XML colle deux fois

## Etape 3 : Bridge ROS 2 <-> Gazebo
- Gazebo et ROS 2 ont des topics et des messages differents ; le bridge traduit
- Syntaxe : /topic@type_ros2<symbole>type_gazebo
  - [ = Gazebo vers ROS 2 (capteurs), ] = ROS 2 vers Gazebo (commandes)
  - @ = bidirectionnel
- /cmd_vel : ROS 2 -> Gazebo (geometry_msgs/Twist)
- /odom : Gazebo -> ROS 2 (nav_msgs/Odometry, position estimee)
- driver_node : publisher /cmd_vel + subscriber /odom + timer 10 Hz
  Boucle : lire capteur -> decider -> commander
  S'arrete quand x >= 2.0 m
- Test : ros2 topic list, ros2 topic echo /odom --once

## Questions d'entretien
- ROS 2 vs Gazebo : ROS 2 = middleware de communication entre programmes
  du robot (le cerveau) ; Gazebo = simulateur de physique et de capteurs
- Pourquoi un bridge : formats de messages differents entre Gazebo et ROS 2
- link vs joint : link = piece solide, joint = liaison/mouvement entre deux links
- inertial/collision : la physique a besoin de la masse et de la forme de contact
- static : l'objet est fixe, pas simule dynamiquement
- visual vs collision : visual = affichage, collision = contact physique
- Launch file : script qui demarre plusieurs noeuds/processus ensemble
- Odometrie : estimation de la position a partir de la rotation des roues

## Etape 4 : Lidar, bridge /scan, evitement d'obstacles
- Lidar 2D : mesure la distance au plus proche obstacle dans plusieurs directions
- LaserScan : ranges, angle_min/max, angle_increment, range_min/max ; un rayon
  sans retour donne inf ; angle du rayon i = angle_min + i * angle_increment
  (0 = devant, positif = gauche)
- Gazebo : <sensor type="gpu_lidar"> dans un link + plugin systeme Sensors dans le world
- IMPORTANT : gpu_lidar fonctionne avec render_engine ogre2. Avec ogre, le scan
  renvoyait des valeurs fausses (toutes a 1.0)
- Bridge : /scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan
- obstacle_avoider : machine a etats FORWARD / TURN avec hysteresis
  (tourne si devant < 0.7 m, arrete de tourner si devant > 0.95 m ;
  direction choisie une seule fois au debut du virage)
- Ne pas lancer driver_node et obstacle_avoider ensemble (deux publishers /cmd_vel)

### Problemes rencontres et solutions
- Robot qui basculait : 2 roues folles (avant/arriere), chassis plus bas et plus
  lourd, inerties explicites, accelerations limitees dans DiffDrive
- Simulation lente (RTF ~9 %) : pas de temps 4 ms, lidar 120 rayons, ombres off
- Scan faux : mauvais moteur de rendu (ogre au lieu de ogre2)
- Methode de debug : isoler la chaine (lidar, bridge, DiffDrive) avec
  ros2 topic pub, ros2 topic hz, ign topic -e

### Questions d'entretien (etape 4)
- Que contient un LaserScan ? Pourquoi inf ?
- Pourquoi le plugin Sensors et le moteur ogre2 ?
- Pourquoi l'hysteresis dans l'evitement ? Eviter l'oscillation entre TURN et FORWARD
- Comment as-tu debugge un robot qui ne bougeait pas ? Test de chaque maillon
