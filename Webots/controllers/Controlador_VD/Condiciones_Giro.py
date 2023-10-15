import random

def DecisionGiro(agente):
    dMin = 15.5#agente.distanceCenter*100
    if agente.FrenoEmergencia == True:
        agente.FrenoEmergencia = False
        if agente.ds1_value <= dMin:
            agente.angulo +=45

        if agente.ds5_value <= dMin:
            agente.angulo -=45
        return
    
    
    dis = 100
    #if agente.ds0_value < dis:                  
    if agente.ds1_value >= agente.ds5_value:#agente.ds2_value >= agente.ds0_value and agente.ds2_value >= agente.ds4_value and agente.ds1_value >= agente.ds5_value:
        agente.angulo = agente.angulo -45
        #print("giro 1")
        
    elif agente.ds5_value >= agente.ds1_value:#agente.ds4_value >= agente.ds0_value and agente.ds4_value >= agente.ds2_value and agente.ds5_value >= agente.ds1_value:
        agente.angulo = agente.angulo +45
        #print("giro 2")

    elif agente.ds0_value < 70 and agente.ds3_value > agente.ds0_value and agente.ds3_value > agente.ds1_value and agente.ds3_value > agente.ds5_value:
        agente.angulo += 180 
        print("giro 3, 180°") 
            
    else:
        
        numero_aleatorio = random.randint(0, 1)
        if numero_aleatorio == 1:
            agente.angulo += 45
            print("giro 4, +45°")
        else:
            agente.angulo -= 45
            print("giro 4, -45°")
        #agente.angulo += 90

        """
        while agente.step(agente.timestep) != -1:
            if agente.step(agente.timestep) == -1:
                break
          """