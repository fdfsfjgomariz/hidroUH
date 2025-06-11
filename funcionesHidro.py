from typing import List, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculaHU(area:float, longitud:float, desnivel:float,  duracion:int, dt:int=30, prop:bool=False):
   '''Calcula el Hidrograma Unitario Instantaneo de una cuenca a partir de:
      area en km2, longitud en km, desnivel en m, duración en horas dt en minutos.
      Si prop is True devuelve el HU en proporción '''

   pendiente = desnivel/(1000*longitud)              # adimensional
   tc = 0.06628 * longitud**0.77 / pendiente**0.385  # horas
   tp = duracion/2 + 0.35*tc                         # horas
   qp = 0.208 * area /tp                             # m3/s 
   tb = 2.67* tp                                     # horas
   q = []
   pasos = round(tb*60)
   for i in range(pasos):                            # Cálculo minuto a minuto 
       t=(i-1)/60                                    # Tiempo en horas
       if t<=tp: q.append(t*qp/tp)                   # Cálculo q en la rama ascendente del HU
       if t>tp:  q.append(qp - (t-tp)*qp/(tb-tp))    # Cálculo q en la rama descendente del HU
   q = [qq*60 for qq in q]                           # Paso del caudal de m3/seg a m3/min
   qcum = []
   for i in range(0,len(q),dt): 
      qcum.append(sum(q[i:i+dt]))
   if prop is False:
      return(qcum)
   else: 
      qprop = [q/sum(qcum) for q in qcum]                             
      return(qprop)


def calculaHUmod(area:float,tc:float, duracion:int, dt:int=30, prop:bool=False):
   '''Calcula el Hidrograma Unitario Instantaneo de una cuenca a partir de:
      area en km2, longitud en km, desnivel en m, duración en horas dt en minutos.
      Si prop is True devuelve el HU en proporción '''

   tp = duracion/2 + 0.35*tc                         # horas
   qp = 0.208 * area /tp                             # m3/s 
   tb = 2.67* tp                                     # horas
   q = []
   pasos = round(tb*60)
   for i in range(pasos):                            # Cálculo minuto a minuto 
       t=(i-1)/60                                    # Tiempo en horas
       if t<=tp: q.append(t*qp/tp)                   # Cálculo q en la rama ascendente del HU
       if t>tp:  q.append(qp - (t-tp)*qp/(tb-tp))    # Cálculo q en la rama descendente del HU
   q = [qq*60 for qq in q]                           # Paso del caudal de m3/seg a m3/min
   qcum = []
   for i in range(0,len(q),dt): 
      qcum.append(sum(q[i:i+dt]))
   if prop is False:
      return(qcum)
   else: 
      qprop = [q/sum(qcum) for q in qcum]                             
      return(qprop)


def HUconv(p, hu, area, intervalo):
   '''Convolución del yetograma a partir de HU en proporción, area en km2 intervalo en horas''' 
   area = area * 1000000         # paso el área a m2
   intervalo = intervalo * 3600  # paso el intervalo a segundos
   h = [0] * (len(p)+len(hu)-1)
   #print(len(h))
   for t in range(len(hu)): 
        conv = hu[t] * p
        h[t:(t+len(p))] = h[t:(t+len(p))] + conv
        #pripe = [50, 75, 25]nt(conv)
        #h[t:(t+len(hu))] = [c+hh for c,hh in zip(conv,h[t:(t+len(hu))])]  
        #print(t,conv,h)
   #print(h)     
   return([hh*area/(1000*intervalo) for hh in h]) #paso de l/m2 a m3/m2


def ncMod(p=[1,2,3,4,5], nc=58, figure=None):
    ''' Aplicación del Número de curva nc a un yetograma de precipitación.
        Si figure es un nombre de fichero, guarda el gráfico en él'''
    S = 25400/nc - 254
    Ia = 0.2*S
    PeTot = ((np.sum(p) - 0.2*S)**2)/(np.sum(p) + 0.8*S)
    Fa = np.sum(p)- (Ia+PeTot) 
    #print(Ia, PeTot, Fa )
    P_ac = np.cumsum(p)
    Ia_ac, Pe_ac, F_ac = [np.nan]*len(p),  [np.nan]*len(p), [np.nan]*len(p)
    for t in range(len(p)):
       Ia_ac[t] = P_ac[t] if P_ac[t]<Ia  else Ia   
       Pe_ac[t]=( (P_ac[t]-Ia_ac[t])**2) / (P_ac[t] + S -Ia_ac[t])
       F_ac[t]=P_ac[t]-(Pe_ac[t]+Ia_ac[t])
    #print(P_ac)
    #print(Ia_ac)
    #print(F_ac)
    #print(Pe_ac)
    Pe = [Pe_ac[0]];Pe.extend(np.diff(Pe_ac))
    F = [F_ac[0]]; F.extend(np.diff(F_ac))
    Ia = [Ia_ac[0]]; Ia.extend(np.diff(Ia_ac))
    if figure is not None:
       res[["Ia","F","Pe"]].plot(kind='bar', stacked=True, color=['red', 'green', 'blue'])
       plt.savefig(figure)
       plt.ylabel("mm")
       plt.xlabel("time")
       plt.close()
    return(pd.DataFrame({"P":p, "Ia":Ia, "F":F, "Pe":Pe}))


def muskingum(I:List, dt:float ,K: float ,X:float , o0:float=0, addTime:int=0):
    '''Enrutamiento de avenida con Muskingum. I es el hidrograma de entrada, 
       K y X los parámetros del modelo, o0 la estimación del caudal inicial de salida,
       por defecto 0, y addTime el número de intervalos que hay auq añadir al número de
       intervalos de I''' 
    I.extend([0]*addTime)  
    #print(I)
    deno = K*(1-X) + dt/2
    C1 = (dt/2 + K*X) / deno
    C2 = (dt/2 - K*X) / deno
    C3 = (K*(1-X) - dt/2) / deno
    #print(deno,C1,C2,C3)
    O = [o0]
    for t in range(1,len(I)):
        O2 = C1*I[t-1] + C2*I[t] + C3*O[t-1]
        O.append(O2)
    return(O)


def muskingummod(I, dt:float ,K:float ,X:float, o0:float=0):
    '''Enrutamiento de avenida con Muskingum. I es el hidrograma de entrada, 
       K y X los parámetros del modelo, o0 la estimación del caudal inicial de salida,
       por defecto 0, y addTime el número de intervalos que hay auq añadir al número de
       intervalos de I'''
    
    I = np.asarray(I)
    n = len(I)
    O = np.zeros(n)

    # Establecer la condición inicial de salida
    O[0] = o0
        
    # Validar parámetros según criterios de HEC-HMS
    if X < 0 or X > 0.5:
        raise ValueError("x debe estar entre 0 y 0.5.")
    #if dt > 2 * K * X:
    #    raise ValueError(f"dt debe ser ≤ {2*K*X} para evitar coeficientes negativos (HEC-HMS).")
    
    # Calcular coeficientes
    D = 2 * K * (1 - X) + dt
    C0 = (dt - 2 * K * X) / D
    C1 = (dt + 2 * K * X) / D
    C2 = (2 * K * (1 - X) - dt) / D

    # Validar estabilidad (HEC-HMS requiere C0 ≥ 0 y C2 ≥ 0)
    if C0 < 0 or C1 < 0 or C2 < 0:
        raise ValueError("Coeficientes negativos. Ajusta K, X, o dt.")
    
    # Iteración para calcular la salida
    for t in range(1, n):
        O[t] = C0 * I[t] + C1 * I[t-1] + C2 * O[t-1]
    
    return O



def modelo(series, parametros, topologia, dt, addTime=0):
   '''Modelización con NC, HU y Muskingum. series contiene las series e precipitación de cada cuenca.
      parametros los parámetros para cada cuenca, topologia describe la topología de la red.
      addTime y dt son los parámetros addTime y dt para Muskingum.
      Devuelve diccionarios con las series de precipitación efectiva, caudal generado por HU, caudal generado
      tras aplicar Muskingum a los caudales de entrada y caudal total para cada una de las cuencas'''
   precEf, HU, Q1, musk, Q2 = {}, {}, {}, {}, {}
   lenmaxHU = 0 
   for i in topologia["id"]:
       ncRes = ncMod(series["prec"][i], nc=parametros["nc"][i])
       precEf["Q_"+str(i)] = ncRes.Pe
       HU["Q_"+str(i)] = calculaHU(parametros["area"][i], parametros["longitud"][i],
                                   parametros["desnivel"][i], parametros["duracion"][i], 
                                   dt=60, prop=True)  # Hay que unificar duraciones
       if len(HU["Q_"+str(i)]) > lenmaxHU: lenmaxHU = len(HU["Q_"+str(i)]) 
       #print("longitud de ", i, len(HU["Q_"+str(i)]), lenmaxHU)
   for i in topologia["id"]:
       addZeros = lenmaxHU - len(HU["Q_"+str(i)])
       if addZeros>0:
           HU["Q_"+str(i)] = HU["Q_"+str(i)] + [0]*addZeros
       Q1["Q_"+str(i)] = HUconv(ncRes.Pe, HU["Q_"+str(i)], parametros["area"][i], 
                                parametros["duracion"][i])
       #print("longitud de ", i, len(HU["Q_"+str(i)]), lenmaxHU)
   secuencia = []
   for i in range(len(topologia["orden"])):
       if i == 0:
          for j in topologia["orden"][i]:
             #print(i,j)
             Q2["Q_"+str(j)] = Q1["Q_"+str(j)].copy() 
             Q2["Q_"+str(j)].extend([0]*addTime)
       else:
          for j in topologia["orden"][i]:
             #print(i,j)
             tp0 = topologia["prev"][j][0]
             tp1 = topologia["prev"][j][1] 
             previos = [q1+q2 for q1,q2 in zip(Q2["Q_"+str(tp0)], Q2["Q_"+str(tp1)])]
             musk["Q_"+str(j)] = muskingum(previos, dt, parametros["K"][j], 
                                           parametros["X"][j], parametros["o0"][j],
                                           addTime=addTime)
             qq = Q1["Q_"+str(j)].copy()
             qq.extend([0]*addTime)
             Q2["Q_"+str(j)] = [q+m for q,m in zip(qq, musk["Q_"+str(j)])]
   return(precEf, Q1, musk, Q2)     



#FUNCIONES PACOGOM###################################################
def nse(predictions, targets):
    return 1 - (np.sum((targets - predictions) ** 2) / np.sum((targets - np.mean(targets)) ** 2))
    
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())
    
def pbias(predictions, targets):
    return (np.sum(targets - predictions) / np.sum(predictions)) * 100