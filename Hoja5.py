# -*- coding: cp1252 -*-

# Universidad del Valle de Guatemala
# Algoritmos y Estructura de Datos
# Hoja de Trabajo no. 5
# Rudy Alexandro Garrido Véliz - 14366
# Yosemite Noé Meléndez Ovando - 14413
# 27/08/2015

# Importando Modulos
import simpy
import random

# definiendo Proceso y recibe como parámetros:
#   env: el ambiente creado | noProceso: el número del proceso | cpu: procesador |
#   cantMem: memoria solicitada por el proceso | ram: la memoria ram del ambiente
#   cantInstrucciones: el total de instrucciones que realizará el proceso
def proceso(env, noProceso, cpu, llegadaP, cantMem,ram,cantInstrucciones):
    global tiempoTotal
    
    # Simula la creacion del proeceso
    yield env.timeout(llegadaP)
    print('%s | creado [new] en el tiempo: %f' % (noProceso, env.now))
    tiempoCreado = env.now #tiempo en que llegó / se creó

    # Hace la solicitud de memoria Ram
    yield ram.get(cantMem)
    print ('%s | solicitando memoria: %d [ready] en el tiempo: %f '% (noProceso, cantMem, env.now))

    #Muestra la cantidad de instrucciones que requiere el proceso
    print('%s | procesando %d instrucciones [running]' % (noProceso, cantInstrucciones))

    
    realizadas=0 #variable que indica la cantidad de instruccinoes realizadas de cada Proceso
    while realizadas != cantInstrucciones: # Este while se ejecuta hasta que se hayan ralizado todas las instrucciones

        # Se hace la solicitud para conectarse al cpu
        with cpu.request() as req:  
            yield req # este req espera a que se desocupe el cpu
        
            # Realizar instruciones
            # Se solicita que el CPU realice 3 instrcciones por unidad de tiempo
            if (cantInstrucciones-realizadas)>3: # Si el proceso requiere más de 3 instrucciones
                realizar = 3 # Solo puede realizar 3 instrucciones
                # Muestra las instrucciones procesadas (3)
                print('%s | procesando %d instrucciones [running]' % (noProceso, realizar))
                yield env.timeout(realizar/3.0) # Si son menos de 3 instruccinoes, lo realiza en menos de 1 unidad de tiempo
                
            else: # Si el proceso requiere 3 instrucciones o menos o le fantan instrucciones
                realizar = cantInstrucciones-realizadas
                # Muestra las instrucciones procesadas
                print('%s | procesando %d instrucciones [running]' % (noProceso, realizar))
                yield env.timeout(realizar/3.0) # Si son 3 instrucciones, lo realiza en 1 unidad de tiempo
                break
            
            # Variable contadora que indica la cantidad de instrucciones realizadas
            realizadas+=realizar 
            print ('%s | instrucciones realizadas: %d [running]' % (noProceso, realizadas))

            # Si ya se realizaron todas las instrucciones, salir del while
            if (realizadas == cantInstrucciones): 
                break

            # Se hace la solicitud para ir a la cola Wait
            with wait.request() as req:
                waitRan = random.randint(1,2)
                # Se muestra si el random para el wai es 1 0 2
                print ('%s | Solicitando cola "Wait" (1/2)... %d ' % (noProceso, waitRan))

                # Si el waiRan es 1, pasa a cola de Waiting. Se realizan operaciones de entrada/salida
                if (waitRan == 1 and realizadas < cantInstrucciones):
                    yield req #para esperar en wait y solicitar memoria
                    print ('%s | en operacinoes I/0 [waiting]' % (noProceso))

                    #Se simula que las operaciones de I/0 pueden variar en tiempo
                    op = random.randint (1,10)  # Utilizada para realizar las operaciones I/O
                                                # (No se especificaba en la hoja de instrucciones)
                    yield env.timeout(op) #Luego de realizar las operaciones I/O regresa a la cola ready
                else:
                    print ('%s | Regresando a cola [ready]' % (noProceso))

    # Regresando la memoria RAM que demanda el proceso 
    yield ram.put(cantMem)   
    print('%s | dejando el cpu [Terminated] en el tiempo: %f ' % (noProceso, env.now))

    
    tiempoCorrida = env.now - tiempoCreado    # El tiempo de Corrida de un proceso
    tiempoTotal = tiempoTotal + tiempoCorrida # tiempoTotal para calcular el promedio

    #print ("Total: %f" % (tiempoTotal))        
            ## yield ram.get(45)
            

# Se crea ambiente de simulacion
env = simpy.Environment()  

#En esta linea se definen las Colas. Se define para tenerlas en el mismo ambiente que creamos 
#Hay 3 tipos de colas --> simpy.Resource es un tipo, Container otro tipo.

cpu = simpy.Resource(env, capacity=2) # cpu
ram = simpy.Container(env, init=100, capacity= 100)# memoria ram 
wait = simpy.Resource(env, capacity = 1) # cola de wait para las fuciones I/O

# Variables utlizadas
tiempoTotal = 0.0
RANDOM_SEED = 200
random.seed(RANDOM_SEED)
interval = 10   #Para la simulación del tiempo de creacion del proceso

# crear los nuevos procesos que llegarán
n = 50
for i in range(n):
    #la mejor forma de simular llegadas es la distrubucion exponencial
    tCreacion = random.expovariate(1.0 / interval) #simulando las llegadas
    cantMem = random.randint(1,10)  # Simulando la cantidad de memora que utilizará el proceso
    cantInstrucciones = random.randint(1,10) # Simulando la cantidad de Instrucciones que realiza
    
    #env.process hace que algo tenga vida en nuestro ambiente
    env.process(proceso(env, 'Proceso %d' % i, cpu, tCreacion, cantMem, ram, cantInstrucciones))

    
    
# correr la simulacion
env.run()
print('Promedio por proceso: %f' %(tiempoTotal/n))
