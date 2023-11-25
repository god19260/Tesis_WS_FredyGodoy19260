"""Supervisor_Mundo controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor, Receiver, Emitter
import numpy as np



# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = 3

# Configuración de receptor
receiver = robot.getDevice("receiver")
receiver.enable(timestep)

# Configuración de emisor
emitter = robot.getDevice("emitter")
emitter.setChannel(0)



Walls = []
translation_field = []
orientation_field = []

Obs = []
Obs_Translation_Field = []
Obs_Orientation_Field = []

Checkpoints = []
Checkpoints_Translation_Field = []
Checkpoints_Orientation_Field = []
Checkpoints_appearance = []


cant_paredes = 10
cant_cajas = 3
cant_checkpoints = 1

modo = 1 # 0 Obtener datos, 1 colocar paredes, 2 pruebas
mapa = 5 # 0 no cambia mapa, 1 pruebas de algoritmos, 2 validación
# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'- Obtener objetos del mundo -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-
# Paredes
for dsnumber in range(cant_paredes):
    Walls.append(robot.getFromDef('wall(' + str(dsnumber)+')'))
    translation_field.append(Walls[-1].getField('translation'))
    orientation_field.append(Walls[-1].getField('rotation'))

# Obstaculos: Cajas
for box_number in range(cant_cajas):
    Obs.append(robot.getFromDef('BOX_'+str(box_number)))
    Obs_Translation_Field.append(Obs[box_number].getField('translation'))
    Obs_Orientation_Field.append(Obs[box_number].getField('rotation'))

# Checkpoint
for checkpoint_number in range(cant_checkpoints):
    Checkpoints.append(robot.getFromDef('CP_'+str(checkpoint_number)))
    Checkpoints_Translation_Field.append(Checkpoints[checkpoint_number].getField('translation'))
    Checkpoints_Orientation_Field.append(Checkpoints[checkpoint_number].getField('rotation'))
    

#Checkpoint_Shape = robot.getFromDef('CP_0_Shape')
#Checkpoints_appearance.append(Checkpoint_Shape.getField("appearance").getSFNode())

#new_color = [1.0, 0.0, 0.0, 1.0]  # Red color
#Checkpoints_appearance[0].setSFColor("baseColor",new_color)

#-*-

print(" Prueba para obtener los nodos de cambio de color.")
"""
Nodo = robot.getFromDef('PLACA_1.PLACA_1_Shape')
appearance = Nodo.getField('PBRAppearance')
color = appearance.getSFColor()
print(color)


for i in range(child_node.getCount()):
    nodos=child_node.getMFNode(i)
    if nodos.getTypeName() == 'Shape':
        print('si entro: i> ',i)
        color_field= nodos.getField('diffuseColor')
        #color_field.setSFColor([0.0, 1.0, 0.0])
    print( nodos.getTypeName() )
"""
#appearance = child_node.getField('diffuseColor')

#appearance = child_node.getField('baseColor')
#baseColor = appearance.getField('baseColor')

#appearance.setSFColor([1,0,0])
#-*-    
    
# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-


# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'- Modos -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-
if modo == 0:
    # Obtener datos de las paredes:
    # Obtener las posiciones de las paredes 
    print(" \nPosiciones de las paredes")
    for i in range(len(Walls)):
        print('wall(',i,'): ',Walls[i].getPosition())
        
    # Obtener la orientación de las paredes 
    print(' \nOrientación de las paredes')
    for i in range(len(Walls)):
        print('wall(',i,'): ',orientation_field[i].getSFVec3f())

    # Obtener datos de las cajas
    # Obtener las posiciones de las cajas
    print(" \nPosiciones de las cajas")
    for i in range(len(Obs)):
        print('Obstaculo Caja ',i,': ', Obs[i].getPosition())

    # Obtener la orientación de las cajas
    print(' \nOrientación de las cajas')
    for i in range(len(Obs)):
        print('Obstaculo Caja ',i,': ', Obs_Orientation_Field[i].getSFVec3f())

elif modo == 1:
    if mapa == 1:
        # Mapa: Validación de algoritmos independientes
        Walls_Positions =[[0.58, -1.09, 0.0],
                [-2.13, -0.49999, 0.0],
                [-1.09, 1.46, 0.0],
                [-0.03, -2.32, 0.0],
                [-0.130006, 0.49001, 0.0],
                [0.33, -0.48, 0.0],
                [0.300002, 1.50001, 0.0],
                [0.76, 0.46, 0.0],
                [-0.91, 2.46, 0.0],
                [0.65999, 1.5, 0.0]]

        Walls_Orientations = [[0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0, 1.5708]]

        for i in range(len(Walls)):
            new_translation = Walls_Positions[i]
            translation_field[i].setSFVec3f(new_translation)

            new_orientation = Walls_Orientations[i]
            orientation_field[i].setSFRotation(new_orientation)

        # Obstaculos: Cajas
        Obs_Positions =[[-0.632595, -1.325, 0.15],
                        [1.38219, -0.0347126, 0.15],
                        [1.76719, -1.75155, 0.15]]

        Obs_Orientations = [[0.0, 0.0, 1.0, 0.523599],
                            [0.0, 0.0, 1.0, 0.523599],
                            [0.0, 0.0, -1.0, 4.692820414042842e-06]]

        for i in range(len(Obs)):
            new_translation = Obs_Positions[i]
            Obs_Translation_Field[i].setSFVec3f(new_translation)

            new_orientation = Obs_Orientations[i]
            Obs_Orientation_Field[i].setSFRotation(new_orientation)
    if mapa == 2:
            # Mapa: Validación de algoritmos independientes
        Walls_Positions =  [[0.57, 0.8, 0.0],
                            [-1.16122, 1.144, 0.0],
                            [0.09, -0.82, 0.0],
                            [-0.98, -1.04, 0.0],
                            [2.42999, 1.43001, 0.0],
                            [0.57, -1.14, 0.0],
                            [0.1, -0.16999, 0.0],
                            [-1.42, -1.0, 0.0],
                            [1.03001, -0.169991, 0.0],
                            [1.86764, -1.83187, 0.0]]

        Walls_Orientations =   [[0.0, 0.0, 1.0, -3.1415853071795863],
                                [0.0, 0.0, -1.0, -0.7854053071795866],
                                [0.0, 0.0, 1.0, -1.5707953071795862],
                                [0.0, 0.0, 1.0, -1.5707953071795862],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, 1.01503e-06],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, -1.0, -0.7854053071795866]]

        for i in range(len(Walls)):
            new_translation = Walls_Positions[i]
            translation_field[i].setSFVec3f(new_translation)

            new_orientation = Walls_Orientations[i]
            orientation_field[i].setSFRotation(new_orientation)

        # Obstaculos: Cajas
        Obs_Positions =[[-0.812602, -0.965, 0.15],
                        [-1.64782, -2.06471, 0.15],
                        [1.50719, -0.56155, 0.15]]

        Obs_Orientations = [[0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, -1.0, 4.692820414042842e-06]]

        for i in range(len(Obs)):
            new_translation = Obs_Positions[i]
            Obs_Translation_Field[i].setSFVec3f(new_translation)

            new_orientation = Obs_Orientations[i]
            Obs_Orientation_Field[i].setSFRotation(new_orientation)
    
    if mapa == 3:
            # Mapa: Validación de algoritmos independientes
        Walls_Positions =  [[-1.64271, -2.10786, 0.0],
                            [-2.03654, 0.618589, 0.0],
                            [1.26, -0.72, 0.0],
                            [-1.18,0.46,0],
                            [2.40999, -1.51999, 0.0],
                            [-0.4, -1.75, 0.0],
                            [0.630468, 0.500919, 0.0],
                            [1.01958, 1.49148, 0.0],
                            [0.433445, -0.524993, 0.0],
                            [2.04999, 1.6898, 0.0]]

        Walls_Orientations =   [[0.0, 0.0, -1.0, -0.7854053071795866],
                                [0.0, 0.0, -1.0, -1.3090053071795866],
                                [0.0, 0.0, 1.0, -1.5707953071795862],
                                [0.0, 0.0, -1.0, 1.0472],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, -1.5707953071795862],
                                [0.0, 0.0, 1.0, 2.8798],
                                [0.0, 0.0, 1.0, 2.618],
                                [0.0, 0.0, 1.0, 2.0944],
                                [0.0, 0.0, 1.0, 2.0944]]

        for i in range(len(Walls)):
            new_translation = Walls_Positions[i]
            translation_field[i].setSFVec3f(new_translation)

            new_orientation = Walls_Orientations[i]
            orientation_field[i].setSFRotation(new_orientation)

        # Obstaculos: Cajas
        Obs_Positions =[[0.7374, -1.945, 0.15],
                        [-0.227261, 1.6526, 0.15],
                        [-1.24281, -0.731549, 0.15]]

        Obs_Orientations = [[0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, -1.0, -1.0472053071795866],
                            [0.0, 0.0, 1.0, 1.30899]]

        for i in range(len(Obs)):
            new_translation = Obs_Positions[i]
            Obs_Translation_Field[i].setSFVec3f(new_translation)

            new_orientation = Obs_Orientations[i]
            Obs_Orientation_Field[i].setSFRotation(new_orientation)
    
    if mapa == 4:
            # Mapa: Validación de algoritmos independientes
        Walls_Positions =  [[0.204959, -1.9413, 0.0],
                            [1.13482, -1.11559, 0.0],
                            [1.1902, 0.082823, 0.0],
                            [1.08, -0.59, 0.0],
                            [-0.22342, -0.96411, 0.0],
                            [2.09, -1.64, 0.0],
                            [-0.3, -0.02999, 0.0],
                            [1.6, -2.08, 0.0],
                            [2.42001, 0.840009, 0.0],
                            [-2.44001, 1.43, 0.0]]

        Walls_Orientations =   [[0.0, 0.0, 1.0, 2.618],
                                [0.0, 0.0, 1.0, 2.3562],
                                [0.0, 0.0, 1.0, -2.094395307179586],
                                [0.0, 0.0, 1.0, -1.5707953071795862],
                                [0.0, 0.0, -1.0, 2.87979],
                                [0.0, 0.0, 1.0, 1.01503e-06],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, 1.5708]]

        for i in range(len(Walls)):
            new_translation = Walls_Positions[i]
            translation_field[i].setSFVec3f(new_translation)

            new_orientation = Walls_Orientations[i]
            orientation_field[i].setSFRotation(new_orientation)

        # Obstaculos: Cajas
        Obs_Positions =[[-1.72259, -0.395, 0.15],
                        [-1.50782, 1.60529, 0.15],
                        [0.822977, 0.99345, 0.15]]

        Obs_Orientations = [[0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, -1.0472053071795866]]

        for i in range(len(Obs)):
            new_translation = Obs_Positions[i]
            Obs_Translation_Field[i].setSFVec3f(new_translation)

            new_orientation = Obs_Orientations[i]
            Obs_Orientation_Field[i].setSFRotation(new_orientation)
    
    if mapa == 5:
            # Mapa: Validación de algoritmos independientes
        Walls_Positions =  [[-0.39377, -0.330622, 0.0],
                            [2.45, 0.440027, 0.0],
                            [-0.308399, -0.698404, 0.0],
                            [0.182071, -0.896094, 0.0],
                            [1.93999, -0.10999, 0.0],
                            [1.59, 1.93, 0.0],
                            [1.72351, 1.08352, 0.0],
                            [-1.17785, -1.18105, 0.0],
                            [-0.618382, -0.842897, 0.0],
                            [1.03999, 1.43, 0.0]]

        Walls_Orientations =   [[0.0, 0.0, 1.0, -2.3561953071795863],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, -1.0, 0.785397],
                                [0.0, 0.0, 1.0, -2.3561953071795863],
                                [0.0, 0.0, 1.0, 1.5708],
                                [0.0, 0.0, 1.0, -1.5707953071795862],
                                [0.0, 0.0, 1.0, -2.3561953071795863],
                                [0.0, 0.0, 1.0, 2.3562],
                                [0.0, 0.0, 1.0, 2.3562],
                                [0.0, 0.0, 1.0, 1.5708]]

        for i in range(len(Walls)):
            new_translation = Walls_Positions[i]
            translation_field[i].setSFVec3f(new_translation)

            new_orientation = Walls_Orientations[i]
            orientation_field[i].setSFRotation(new_orientation)

        # Obstaculos: Cajas
        Obs_Positions =[[1.2774, -2.165, 0.15],
                        [0.21218, 1.42529, 0.15],
                        [-1.28281, 1.16845, 0.15]]

        Obs_Orientations = [[0.0, 0.0, 1.0, 1.5708],
                            [0.0, 0.0, 1.0, 1.8326],
                            [0.0, 0.0, -1.0, 4.692820414042842e-06]]

        for i in range(len(Obs)):
            new_translation = Obs_Positions[i]
            Obs_Translation_Field[i].setSFVec3f(new_translation)

            new_orientation = Obs_Orientations[i]
            Obs_Orientation_Field[i].setSFRotation(new_orientation)

    # -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-

    # -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-


while robot.step(timestep) != -1:

    if receiver.getQueueLength() > 0:
        data = receiver.getString()
        print(data)
        receiver.nextPacket()
        #------ Enviar datos a robot ----
        data = str(Checkpoints[0].getPosition())
        emitter.send(data.encode())
   

