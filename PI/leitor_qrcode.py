import cv2
from pyzbar import pyzbar
import requests
import serial
import time

URL_VERIFICACAO = "http://localhost:5000/qrcode/"  
PORTA_SERIAL = "/dev/ttyUSB0"  
BAUDRATE = 9600

try:
    arduino = serial.Serial(PORTA_SERIAL, BAUDRATE, timeout=1)
    time.sleep(2)
    print("✅ Conectado ao Arduino.")
except serial.SerialException:
    arduino = None
    print("⚠️ Não foi possível conectar ao Arduino.")

cap = cv2.VideoCapture(0)

print("📷 Lendo QR Codes. Pressione 'q' para sair.")

lidos = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    qrcodes = pyzbar.decode(frame)

    for qr in qrcodes:
        conteudo = qr.data.decode('utf-8')
        if conteudo in lidos:
            continue
        lidos.add(conteudo)
        print(f"🔍 Lido: {conteudo}")

        try:
            usuario_id = conteudo.split("/")[-1]
            resposta = requests.get(f"{URL_VERIFICACAO}{usuario_id}")
            if resposta.status_code == 200:
                print("✅ QR Code válido. Abrindo cancela...")
                if arduino:
                    arduino.write(b"ABRIR\n")
                else:
                    print("⚠️ Arduino não conectado.")
            else:
                print("❌ QR Code inválido ou usuário não aprovado.")
        except Exception as e:
            print("❌ Erro na verificação:", e)

    cv2.imshow("Leitor de QR Code", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
