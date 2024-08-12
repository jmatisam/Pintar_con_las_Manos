import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Abrir la cámara (0 para la cámara predeterminada)
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        max_num_hands=1,
        min_tracking_confidence=0.5) as hands:
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            height, width, _ = frame.shape
            frame = cv2.flip(frame, 1)

            # Convertir la imagen de BGR a RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detectar manos en la imagen
            results = hands.process(rgb_frame)
            
            # Dibujar las landmarks y conexiones de la mano si están presentes
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
            
            cv2.imshow('Dibujar con la Mano', frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
