import cv2
import numpy as np
import detecta_indice

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

# Colores para pintar
colorAzul = (0,52,255)
colorAmarillo = (204, 255, 0)
colorRojo = (255,0,0)
colorVerde = (0,255,36)
colorLimpiarPantallaBackg = (0,0,0) # Solo se usará para el bakcground del cuadro superior de 'Borrar Pantalla'
colorLimpiarPantalla = (255,255,255) # Solo se usará para el texto cuadro superior de 'Borrar Pantalla'
# Grosor de línea recuadros superior izquierda (color a dibujar)
grosorAzul = 7
grosorAmarillo = 2
grosorRojo = 2
grosorVerde = 2

# Grosor de línea recuadros superior derecha (grosor del marcador para dibujar)
grosorPeque = 7
grosorMedio = 1
grosorGrande = 1

#--------------------- Variables para el marcador / lápiz virtual -------------------------
color = colorAzul  # Color de entrada, y variable que asignará el color del marcador
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
    cv2.rectangle(frame,(50,0),(100,50),colorRojo,grosorRojo)
    cv2.rectangle(frame,(100,0),(150,50),colorVerde,grosorVerde)
    cv2.rectangle(frame,(150,0),(200,50),colorAzul,grosorAzul)

    # Rectángulo superior central, que nos ayudará a limpiar la pantalla
    cv2.rectangle(frame,(300,0),(400,50),colorLimpiarPantallaBackg ,-1)
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
        cv2.circle(frame, (x, y), 10, grosor, -1)
        

        # Realiza acciones basadas en la posición del dedo índice
        if x1 is not None and y1 is not None:
            if 0 < x < 50 and 0 < y < 50:
                color = colorAmarillo # Color del lápiz/marcador virtual
                grosorAmarillo = 6
                grosorRojo = 2
                grosorVerde = 2
                grosorAzul = 2
            if 50 < x < 100 and 0 < y < 50:
                color = colorRojo # Color del lápiz/marcador virtual
                grosorAmarillo = 2
                grosorRojo = 7
                grosorVerde = 2
                grosorAzul = 2
            if 100 < x < 150 and 0 < y < 50:
                color = colorVerde # Color del lápiz/marcador virtual
                grosorAmarillo = 2
                grosorRojo = 2
                grosorVerde = 7
                grosorAzul = 2
            if 150 < x < 200 and 0 < y < 50:
                color = colorAzul # Color del lápiz/marcador virtual
                grosorAmarillo = 2
                grosorRojo = 2
                grosorVerde = 2
                grosorAzul = 7
            if 490 < x < 540 and 0 < y < 50:
                grosor = 3 # Grosor del lápiz/marcador virtual
                grosorPeque = 7
                grosorMedio = 1
                grosorGrande = 1
            if 540 < x < 590 and 0 < y < 50:
                grosor = 7 # Grosor del lápiz/marcador virtual
                grosorPeque = 1
                grosorMedio = 7
                grosorGrande = 1
            if 590 < x < 640 and 0 < y < 50:
                grosor = 11 # Grosor del lápiz/marcador virtual
                grosorPeque = 1
                grosorMedio = 1
                grosorGrande = 7
            if 300 < x1 < 400 and 0 < y < 50:
                cv2.rectangle(frame,(300,0),(400,50),colorLimpiarPantallaBackg,-1)
                cv2.putText(frame,'Borrar',(320,20),6,0.6,colorLimpiarPantalla,1.5,cv2.LINE_AA)
                cv2.putText(frame,'pantalla',(320,40),6,0.6,colorLimpiarPantalla,1.5,cv2.LINE_AA)
                imAux = np.zeros(frame.shape,dtype=np.uint8)
            if 0 < y1 < 60 or 0 < y < 60 :
                    imAux = imAux
            else:
                imAux = cv2.line(imAux,(x,y),(x1,y1),color,grosor)   
        else:
            x1, y1 = None, None    
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



