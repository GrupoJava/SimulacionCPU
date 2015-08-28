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
import math

# definiendo Proceso y recibe como parámetros:
#   env: el ambiente creado | noProceso: el número del proceso | cpu: procesador |
#   cantMem: memoria solicitada por el proceso | ram: la memoria ram del ambiente
#   cantInstrucciones: el total de instrucciones que realizará el proceso
def proceso(env, noProceso, cpu, llegadaP, cantMem,ram,cantInstrucciones):
    global tiempoTotal
    global tiempos
    
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

            # i es la cantidad de insturcciones a ejecutar por el procesador
            i = 3.0 # si se quiere cambiar la velocidad de procesador basta con cambiar el valor --> debe estar en flotante
            if (cantInstrucciones-realizadas)>i: # Si el proceso requiere más de i (3) instrucciones
                realizar = i # Solo puede realizar i (3) instrucciones
                # Muestra las instrucciones procesadas i (3)
                print('%s | procesando %d instrucciones [running]' % (noProceso, realizar))
                yield env.timeout(realizar/i) # Si son menos de i (3) instruccinoes, lo realiza en menos de 1 unidad de tiempo
                
            else: # Si el proceso requiere i (3) instrucciones o menos o le fantan instrucciones
                realizar = cantInstrucciones-realizadas
                # Muestra las instrucciones procesadas
                print('%s | procesando %d instrucciones [running]' % (noProceso, realizar))
                yield env.timeout(realizar/i) # Si son i (3) instrucciones, lo realiza en 1 unidad de tiempo
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
    tiempos.append(tiempoCorrida) #Aquí se van agregando los valores a una matriz para calcular la desviación Estándar

    #print ("Total: %f" % (tiempoTotal))        
            ## yield ram.get(45)
            

# Se crea ambiente de simulacion
env = simpy.Environment()  

#En esta linea se definen las Colas. Se define para tenerlas en el mismo ambiente que creamos 
#Hay 3 tipos de colas --> simpy.Resource es un tipo, Container otro tipo.

cpu = simpy.Resource(env, capacity=1) # cpu
ram = simpy.Container(env, init=100, capacity= 100)# memoria ram 
wait = simpy.Resource(env, capacity = 1) # cola de wait para las fuciones I/O

# Variables utlizadas
tiempoTotal = 0.0
RANDOM_SEED = 200
random.seed(RANDOM_SEED)
interval = 10   #Para la simulación del tiempo de creacion del proceso
tiempos =[] # lista para guardar los valores de los tiempos de Corrida
# crear los nuevos procesos que llegarán
n = 100
for i in range(n):
    #la mejor forma de simular llegadas es la distrubucion exponencial
    tCreacion = random.expovariate(1.0 / interval) #simulando las llegadas
    cantMem = random.randint(1,10)  # Simulando la cantidad de memora que utilizará el proceso
    cantInstrucciones = random.randint(1,10) # Simulando la cantidad de Instrucciones que realiza
    
    #env.process hace que algo tenga vida en nuestro ambiente
    env.process(proceso(env, 'Proceso %d' % i, cpu, tCreacion, cantMem, ram, cantInstrucciones))

    
# correr la simulacion
env.run()

#Imprime el promedio
promedio = tiempoTotal/n
print('Promedio por proceso: %f' %(promedio))

#Calcula la desviación estándar
sumatoria = [] #Un arreglo para luego hacer los cálculos (Xi - Xprom)^2
op1 = 0.0
op2 = 0.0
for i in range(n):
    op1 = (tiempos[i] - promedio)**2 # op1 es (Xi - Xprom)^2 donde Xi es tiempoCorrida y Xprom es promedio
    sumatoria.append(op1) # Guarda los valores ya operados
    op2 = op2 + sumatoria[i] # Esta variable corresponde a "Sumatoria i a n de (Xi - Xprom)^2" en la formula de desv Estandar

op3 = (op2/(n-1)) # (Sumatoria de valores) / n-1
desvEst = math.sqrt(op3) # El valor que quda es la varianza al cuadrado, la desviación es la raíz de este valor

#print(tiempos)     # si se quiere ver la lista de tiempos de corrda --> Tiempo corrida = Xi
#print (sumatoria)  # si se quiere ver la lista de (Xi - Xprom)^2
#print (op2)        # si se quiere ver la sumatoria de los valores (Xi - Xprom)^2
#print (op3)        # Este valor es la varianza al cuadrado

#imprime la desviación Estándar
print ('La desviación estándar es: %f' %(desvEst))
