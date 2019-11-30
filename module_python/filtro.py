from scipy.stats import norm
from prettytable import PrettyTable
import numpy as np
import time
import math

class Filtro():
    def __init__(self,dt=1,x=3,y=5,Pk1=0.2,Pk2=0.1): #Pk2 = Covarianza
        #Variables extras
        self.a = 10**-3 #Determina la dispersion
        self.k = 0  #Pranetro de escala
        self.L = 5 #Variables del sistema, longitud del vector x, cantidad de sigmas
        self.λ = (self.a**2 * (self.L + self.k)) - self.L #Factor de escala
        
        #(L + λ) = 1
        self.dt = dt
        self.n = 5

        self.peso_W = 0.0 #Pesos

        self.Xk_0 = np.array([[x],[y]]) #Punto medio
        self.Xk= None  #Puntos sigmas
        self.Xˆk = np.array([[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]]) #Puntos sigmas primas

        self.Zk = np.array([[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]]) #Yk Observacion real
        self.Zˆk = np.array([[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]])  # Observacion de la prediccion

        self.matriz_Q = np.array([[Pk1**2,0],[0,Pk2**2]]) #None   matriz de covarianza de la medida
        self.matriz_R = np.array([[Pk1**2,0],[0,Pk2**2]]) #None   matriz de covarianza del estado

        self.Pk =  np.array([[Pk1,0],[0,Pk2]]) #Covarianza
        self.Pzkzk=None
        self.Pxkzk = None

        self.Kk = None

        self.iniciar_proceso()
        

    def iniciar_proceso(self):
        self.puntos_sigma()
        self.prediccion()
        self.actualizacion()
        #self.imprimir_resultados()

    def puntos_sigma(self):
        self.Xk = np.concatenate(( self.Xk_0 , (self.Xk_0 + ((self.L+self.λ) * self.Pk )**1/2 ) , (self.Xk_0 - (self.L+self.λ) * self.Pk )**1/2  ),axis=1)
        self.peso_W =  self.λ / (self.L + self.λ) #1/self.n
    
    def prediccion(self): 
        for j in range(0,self.n):
            self.Xˆk[0][j] = self.peso_W  *  self.Xk[0][j] #y x
            self.Xˆk[1][j] = self.peso_W  *  self.Xk[1][j] 
        self.Pk = self.peso_W * np.matmul((self.Xk - self.Xˆk) , np.transpose((self.Xk - self.Xˆk))) + self.matriz_Q
    
    def actualizacion(self):
        for j in range(0,self.n):
            self.Zk[0][j] = math.atan2( self.Xk[1][j] , self.Xk[0][j] )
            self.Zk[1][j] = math.sqrt( (self.Xk[0][j] **2) + (self.Xk[1][j] **2) )
            self.Zˆk[0][j] =  self.peso_W * self.Zk[0][j]  #y x
            self.Zˆk[1][j] = self.peso_W *  self.Zk[1][j]
        self.Pzkzk = (self.peso_W * np.matmul( (self.Zk - self.Zˆk) , np.transpose(self.Zk - self.Zˆk) ) ) + self.matriz_R
        self.Pxkzk = (self.peso_W * np.matmul( (self.Xk - self.Xˆk) , np.transpose(self.Zk - self.Zˆk) ) ) 
        self.Kk = self.Pxkzk - (self.Pzkzk**-1)
        self.Xˆk = self.Xˆk + np.matmul( self.Kk , (self.Zk - self.Zˆk) )
        self.Pk = self.Pk - np.matmul ( np.matmul(self.Kk,self.Pzkzk) , np.transpose(self.Kk) )


    def imprimir_resultados(self):
        print("Peso W:   ",self.peso_W)

        print("Puntod Medio Xk_0:   ",self.Xk_0)
        print("Puntos Sigmas Xk:   ",self.Xk)
        print("Puntos Sigmas Primas de Xˆk:   ",self.Xˆk)

        print("Observacio Real:   ",self.Zk)
        print("Observacio de la predicion:   ",self.Zˆk)

        print("Matriz Q:   ",self.matriz_Q)
        print("Matriz R:   ",self.matriz_R)

        print("Covarianza Pk:   ",self.Pk)
        print("Covarianza Pzkzk:   ",self.Pzkzk)
        print("Covarianza Pxkzk:   ",self.Pxkzk)
        
        print("Ganancia Kk:   ",self.Kk)
        #print("Ganancia Kk:   ",h(self.Kk))

""" Filtro() """