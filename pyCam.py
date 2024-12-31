import cv2
import requests
import time
from datetime import datetime

# Configuração do bot do Telegram
telegram_url = "https://api.telegram.org/ID_DO_BOT:TOKEN_API_TELEGRAM/SendMessage"
chat_id = "ID_DO_CHAT"

# Função para enviar mensagem ao Telegram
def enviar_mensagem(telegram_url, chat_id, texto):
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            print(f"Mensagem enviada: {texto}")
        else:
            print(f"Erro ao enviar mensagem: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erro ao se comunicar com o Telegram: {e}")

# Defina o URL do stream RTSP
rtsp_url = "rtsp://USUARIO:SENHA@IP:PORTA/cam/realmonitor?channel=NUMERO_CAMERA&subtype=0"

# Iniciar captura do stream RTSP
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Erro ao acessar o stream RTSP.")
    exit()

# Definir a área de interesse (ROI) onde o movimento será monitorado
roi_x, roi_y, roi_w, roi_h = 0, 300, 70, 100  # (x, y, largura, altura)
threshold_area = 500  # Tamanho mínimo para ser considerado movimento

# Inicializar o fundo para subtração de fundo
fgbg = cv2.createBackgroundSubtractorMOG2()

# Variável para controlar o intervalo de envio de mensagens
ultima_mensagem = 0
intervalo_mensagem = 1  # Enviar mensagem a cada 1 segundo

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erro ao ler frame.")
        break

    # Redimensionar o frame (opcional) para desempenho melhor
    frame_resized = cv2.resize(frame, (640, 480))

    # Convertendo a imagem para escala de cinza
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Aplicar subtração de fundo para detectar movimento
    fgmask = fgbg.apply(gray)

    # Detectar contornos na máscara do movimento
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    movement_detected = False  # Flag para verificar se o movimento foi detectado

    for contour in contours:
        if cv2.contourArea(contour) < threshold_area:
            continue  # Ignorar pequenos movimentos

        # Obter as coordenadas do retângulo delimitador
        (x, y, w, h) = cv2.boundingRect(contour)

        # Verificar se o movimento está dentro da área de interesse (ROI)
        if roi_x <= x <= roi_x + roi_w and roi_y <= y <= roi_y + roi_h:
            # Flag de movimento detectado
            movement_detected = True

    # Se movimento for detectado e o intervalo for respeitado, envie mensagem
    if movement_detected and (time.time() - ultima_mensagem >= intervalo_mensagem):
        momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto = f"Movimento detectado na área de interesse em: {momento}"
        enviar_mensagem(telegram_url, chat_id, texto)
        ultima_mensagem = time.time()

    # Desenhar o retângulo de área de interesse (ROI) no frame
    cv2.rectangle(frame_resized, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)

    # Exibir o frame com os resultados
    cv2.imshow("Detecção de Movimento", frame_resized)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finalize recursos
cap.release()
cv2.destroyAllWindows()
