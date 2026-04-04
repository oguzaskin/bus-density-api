import cv2
from ultralytics import YOLO
import requests
import time

# YOLO modeli yükle
model = YOLO("yolov8m.pt")  # Model dosyasının yolu doğru olmalı

# Kamera aç
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı, farklı index deneyin.")
    exit()

bus_id = "42"  # Render API’de tek ID örnek
server_url = f"https://bus-density-api.onrender.com/update/{bus_id}"

last_sent = 0  # Son gönderim zamanı

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Geçici kaydet
    cv2.imwrite("temp.jpg", frame)

    # YOLO ile tahmin
    results = model("temp.jpg")
    people_count = 0
    for r in results:
        for obj in r.boxes.data.tolist():  # her kutu için
            cls_id = int(obj[5])
            if cls_id == 0:  # person
                people_count += 1

    print(f"Otobüs {bus_id} Yolcu Sayısı: {people_count}")

    # API’ye sadece 3 saniyede 1 gönder
    if time.time() - last_sent > 3:
        try:
            response = requests.post(
                server_url,
                json={"count": people_count},
                timeout=2
            )
            print("API'ye gönderildi:", people_count)
        except Exception as e:
            print("Gönderim hatası:", e)
        last_sent = time.time()

    # 2 saniye bekle
    time.sleep(2)

cap.release()
cv2.destroyAllWindows()