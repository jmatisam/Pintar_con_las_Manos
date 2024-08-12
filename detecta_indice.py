import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

def detecta_indice(frame):
    x, y = None, None  # Valores predeterminados si no se detecta ninguna mano
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        height, width, _ = frame.shape
        
        # Convertir la imagen de BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          
        # Detectar manos en la imagen
        results = hands.process(rgb_frame)
          
        # Dibujar la línea con el dedo índice si está presente
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = int(hand_landmarks.landmark[8].x * width)
                y = int(hand_landmarks.landmark[8].y * height)
                
        return x, y
