# -*- coding: cp1252 -*-
import simpy
import random


def proceso(env, noProceso, cpu, llegadaP, cantMem,ram,cantInstrucciones):
    global tiempoTotal
    
    # Simula la creacion del proeceso
    yield env.timeout(llegadaP)
    print('%s | creado [new] en el tiempo: %f' % (noProceso, env.now))
    tiempoCreado = env.now #tiempo en que llegó / se creó

    # Hace la solicitud de memoria Ram
    yield ram.get(cantMem)
    print ('%s | solicitando memoria: %d [ready] en el tiempo: %f '% (noProceso, cantMem, env.now))

   
    print('%s | procesando %d instrucciones [running]' % (noProceso, cantInstrucciones))
    realizadas=0
    while realizadas != cantInstrucciones:


        with cpu.request() as req:  #pedimos conectarnos a cpu 
            yield req #este req espera a que se desocupe el cpu
        
            # Realizar instruciones
            
            if (cantInstrucciones-realizadas)>=3:
                realizar = 3
                print('%s | procesando %d instrucciones [running]' % (noProceso, realizar))
                yield env.timeout(realizar/3.0) # Si son menos de 3 instruccinoes, lo realiza en menos de 1 unidad de tiempo
                
            else:
                realizar = cantInstrucciones-realizadas
                print('%s | procesando %d instrucciones [running]' % (noProceso, realizar))
                yield env.timeout(realizar/3.0) # Si son 3 instrucciones, lo realiza en 1 unidad de tiempo
                yield ram.put(cantMem)
                break
            
            
            realizadas+=realizar

            
            print ('%s | instrucciones realizadas: %d [running]' % (noProceso, realizadas))
            if (realizadas == cantInstrucciones):
                break
            
            with wait.request() as req:
                waitRan = random.randint(1,2)
                print ('%s | Solicitando cola "Wait" (1/2)... %d ' % (noProceso, waitRan))
                if (waitRan == 1 and realizadas < cantInstrucciones):
                    yield req #para esperar en wait y solicitar memoria
                    print ('%s | en operacinoes I/0 [waiting]' % (noProceso))
                    op = random.randint (1,10) #Utilizada para realizar las operaciones I/O
                    yield env.timeout(op) #Luego de realizar las operaciones I/O regresa a la cola ready
                else:
                    print ('%s | Regresando a cola [ready]' % (noProceso))
                    
        
    print('%s | dejando el cpu [Terminated] en el tiempo: %f ' % (noProceso, env.now))
    tiempoCorrida = env.now - tiempoCreado
    tiempoTotal = tiempoTotal + tiempoCorrida
            
            #with wait.request() as requ:
                
            #yield env.timeout(memRequerida)
            #print('%s leaving the cpu at %s' % (noProceso, env.now))

            ## yield ram.get(45)

            ## yield ram.set(45)


#
env = simpy.Environment()  #crear ambiente de simulacion

#En esta linea se definen las Colas. Decimos que lo queremos en el mismo ambiente que creamos 
#Hay 3 tipos de colas --> simpy.Resource es un tipo
cpu = simpy.Resource(env, capacity=1) #cpu
ram = simpy.Container(env, init=100, capacity= 200)# memoria ram 
wait = simpy.Resource(env, capacity = 1) # cola de wait para las fuciones I/O

tiempoTotal = 0.0
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
interval = 10   #Para la simulación del tiempo de creacion del proceso

# crear los nuevos procesos que llegarán
n = 100
for i in range(n):
    tCreacion = random.expovariate(1.0 / interval) #simulando las llegadas
    cantMem = random.randint(1,10)
    cantInstrucciones = random.randint(1,10)
    
    #env.process hace que algo tenga vida en nuestro ambiente
    env.process(proceso(env, 'Proceso %d' % i, cpu, tCreacion, cantMem, ram, cantInstrucciones))

    #la mejor forma de simular llegadas es la distrubucion exponencial
    
# correr la simulacion
env.run()
print('Promedio por proceso: %f' %(tiempoTotal/n))
