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
