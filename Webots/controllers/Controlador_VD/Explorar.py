import Rot_Control
import Odometria

def Explorar(agente):
    coef_velocidad = 0.01
    vel_max = 8
    ds0_min_val = 30
    dMin = 15.5
    cont = 0
    agente.FrenoEmergencia = True

    while (agente.ds0_value >= agente.ds2_value) and (agente.ds0_value >= agente.ds4_value) or agente.ds0_value>ds0_min_val:
        #agente.DatosSensores()
        
        Odometria.Avance_Lineal(agente,0) # Inicio de avance lineal

        agente.left_motor.setVelocity(vel_max*coef_velocidad)
        agente.right_motor.setVelocity(vel_max*coef_velocidad)

        if coef_velocidad < 1:
            coef_velocidad += 0.05

        agente.DatosSensores()
        Odometria.Avance_Lineal(agente,1) # Fin de avance lineal
        Odometria.Odometria(agente)
        

        if agente.ds2_value < 100 and agente.ds4_value < 100:
            ds0_min_val = 30
        else:
            ds0_min_val = 100

        if cont == 9:
            #Rot_Control.Rot_Control(agente.angulo,agente)
            cont = 0
        cont +=1        
        
        # Condiciones especiales para cambiar la rotación
        if agente.ds0_value <= dMin or agente.ds1_value <= dMin or agente.ds5_value <= dMin:
            print("---- Freno de emergencia ----")
            agente.FrenoEmergencia = False
            
            Odometria.Avance_Lineal(agente,0) # Inicio de avance lineal
            while coef_velocidad > 0.1:
                
                agente.left_motor.setVelocity(vel_max*coef_velocidad)
                agente.right_motor.setVelocity(vel_max*coef_velocidad)
                #Odometria.Odometria(agente)

                coef_velocidad -= 0.5
            
            agente.left_motor.setVelocity(0)
            agente.right_motor.setVelocity(0)
            #Odometria.Odometria(agente)
            agente.DatosSensores()
            Odometria.Avance_Lineal(agente,1) # Fin de avance lineal
            Odometria.Odometria(agente)
            break                   
        
        if agente.step(agente.timestep) == -1:
            break

    Odometria.Avance_Lineal(agente,0) # Inicio de avance lineal
    while coef_velocidad > 0:
        agente.left_motor.setVelocity(vel_max*coef_velocidad)
        agente.right_motor.setVelocity(vel_max*coef_velocidad)
        #Odometria.Odometria(agente)
        
        coef_velocidad -= 0.05
        if agente.step(agente.timestep) == -1:
            break
    agente.DatosSensores()
    Odometria.Avance_Lineal(agente,1) # Fin de avance lineal
    Odometria.Odometria(agente)
    
    agente.left_motor.setVelocity(0)
    agente.right_motor.setVelocity(0)
    #Odometria.Odometria(agente)