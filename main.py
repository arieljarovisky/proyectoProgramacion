import cv2
import numpy as np
import datetime
import time

# Cargar el clasificador preentrenado para detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Inicializar la cámara
cap = cv2.VideoCapture(0)  # Usa 0 para la cámara predeterminada

# Leer el primer fotograma
ret, frame1 = cap.read()
frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)

last_capture_time = time.time()  # Última vez que se tomó una foto
delay = 2  # Segundos entre capturas

while True:
    # Capturar el siguiente fotograma
    ret, frame2 = cap.read()
    if not ret:
        break
    
    # Convertir a escala de grises y aplicar desenfoque
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.GaussianBlur(frame2_gray, (21, 21), 0)

    # Calcular la diferencia absoluta entre los dos fotogramas
    diff = cv2.absdiff(frame1_gray, frame2_gray)
    
    # Umbral para determinar cambios
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # Encontrar contornos de los cambios detectados
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Detectar rostros en la imagen actual
    faces = face_cascade.detectMultiScale(frame2_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Si hay un rostro y también movimiento significativo
    if len(faces) > 0 and any(cv2.contourArea(c) > 500 for c in contours):
        current_time = time.time()
        if current_time - last_capture_time >= delay:  # Esperar el delay antes de la próxima captura
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"captura_{timestamp}.jpg"
            cv2.imwrite(filename, frame2)
            print(f"📸 Foto tomada: {filename}")
            last_capture_time = current_time  # Actualizar el último tiempo de captura

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Rectángulo verde

    # Mostrar el video con detección de movimiento y rostro
    cv2.imshow("Camara en Vivo", frame2)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    # Actualizar el primer fotograma
    frame1_gray = frame2_gray

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
