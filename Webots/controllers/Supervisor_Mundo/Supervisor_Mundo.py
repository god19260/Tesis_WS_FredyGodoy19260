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

modo = 0 # 0 Obtener datos, 1 colocar paredes, 2 pruebas

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

Nodo = robot.getFromDef('PLACA_1.PLACA_1_Shape')
appearance = Nodo.getField('PBRAppearance')
color = appearance.getSFColor()
print(color)

"""
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
# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-


while robot.step(timestep) != -1:

    if receiver.getQueueLength() > 0:
        data = receiver.getString()
        print(data)
        receiver.nextPacket()
        #------ Enviar datos a robot ----
        data = str(Checkpoints[0].getPosition())
        emitter.send(data.encode())
   

