'''
import cv2
import numpy as np
import detecta_indice

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret,frame = cap.read()
    if ret==False: break

    frame = cv2.flip(frame,1)
    
    
    # Call detectar_indice function to get index finger position
    x, y = detecta_indice.detecta_indice(frame)

    print(x)
    print(y)

cap.release()
cv2.destroyAllWindows()
'''

import cv2
import numpy as np
import detecta_indice

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

celesteBajo = np.array([75, 185, 88], np.uint8)
celesteAlto = np.array([112, 255, 255], np.uint8)

# Colores para pintar
colorCeleste = (255,113,82)
colorAmarillo = (89,222,255)
colorRosa = (128,0,255)
colorVerde = (0,255,36)
colorLimpiarPantalla = (29,112,246) # Solo se usará para el cuadro superior de 'Limpiar Pantalla'

# Grosor de línea recuadros superior izquierda (color a dibujar)
grosorCeleste = 6
grosorAmarillo = 2
grosorRosa = 2
grosorVerde = 2

# Grosor de línea recuadros superior derecha (grosor del marcador para dibujar)
grosorPeque = 6
grosorMedio = 1
grosorGrande = 1

#--------------------- Variables para el marcador / lápiz virtual -------------------------
color = colorCeleste  # Color de entrada, y variable que asignará el color del marcador
grosor = 3 # Grosor que tendrá el marcador
#------------------------------------------------------------------------------------------

x1 = None
y1 = None
imAux = None

while True:

    ret,frame = cap.read()
    if ret==False: break

    frame = cv2.flip(frame,1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if imAux is None: imAux = np.zeros(frame.shape,dtype=np.uint8)

    #------------------------ Sección Superior ------------------------------------------
    # Cuadrados dibujados en la parte superior izquierda (representan el color a dibujar)
    cv2.rectangle(frame,(0,0),(50,50),colorAmarillo,grosorAmarillo)
    cv2.rectangle(frame,(50,0),(100,50),colorRosa,grosorRosa)
    cv2.rectangle(frame,(100,0),(150,50),colorVerde,grosorVerde)
    cv2.rectangle(frame,(150,0),(200,50),colorCeleste,grosorCeleste)

    # Rectángulo superior central, que nos ayudará a limpiar la pantalla
    cv2.rectangle(frame,(300,0),(400,50),colorLimpiarPantalla,1)
    cv2.putText(frame,'Limpiar',(320,20),6,0.6,colorLimpiarPantalla,1,cv2.LINE_AA)
    cv2.putText(frame,'pantalla',(320,40),6,0.6,colorLimpiarPantalla,1,cv2.LINE_AA)

    # Cuadrados dibujados en la parte superior derecha (grosor del marcador para dibujar)
    cv2.rectangle(frame,(490,0),(540,50),(0,0,0),grosorPeque)
    cv2.circle(frame,(515,25),3,(0,0,0),-1)
    cv2.rectangle(frame,(540,0),(590,50),(0,0,0),grosorMedio)
    cv2.circle(frame,(565,25),7,(0,0,0),-1)
    cv2.rectangle(frame,(590,0),(640,50),(0,0,0),grosorGrande)
    cv2.circle(frame,(615,25),11,(0,0,0),-1)
    #-----------------------------------------------------------------------------------
    
    # Detección del color celeste
# Llama a la función detecta_indice para obtener la posición del dedo índice
    x, y = detecta_indice.detecta_indice(frame)

    if x is not None and y is not None:
        # Dibuja un círculo en la posición del dedo índice
        cv2.circle(frame, (x, y), 10, color, -1)

        # Realiza acciones basadas en la posición del dedo índice
        if x1 is not None and y1 is not None:
            if 0 < x < 50 and 0 < y < 50:
                color = (0, 255, 255)  # Amarillo
                grosor = 6
            elif 50 < x < 100 and 0 < y < 50:
                color = (128, 0, 255)  # Rosa
                grosor = 6
            elif 100 < x < 150 and 0 < y < 50:
                color = (0, 255, 36)  # Verde
                grosor = 6
            elif 150 < x < 200 and 0 < y < 50:
                color = (255, 113, 82)  # Celeste
                grosor = 6
            elif 300 < x < 400 and 0 < y < 50:
                # Limpiar pantalla
                imAux = np.zeros(frame.shape, dtype=np.uint8)
            else:
                # Dibuja línea entre puntos (x1, y1) y (x, y)
                if imAux is not None:
                    imAux = cv2.line(imAux, (x1, y1), (x, y), color, grosor)

        # Actualiza los puntos previos (x1, y1)
        x1, y1 = x, y

    # Procesamiento adicional de la imagen auxiliar (imAux)
    if imAux is not None:
        imAuxGray = cv2.cvtColor(imAux, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(imAuxGray, 10, 255, cv2.THRESH_BINARY)
        thInv = cv2.bitwise_not(th)
        frame = cv2.bitwise_and(frame, frame, mask=thInv)
        frame = cv2.add(frame, imAux)

    # Muestra la imagen con las acciones realizadas
    cv2.imshow('Frame', frame)

    # Presiona 'Esc' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



