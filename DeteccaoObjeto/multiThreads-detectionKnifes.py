# Referências: https://github.com/AlexeyAB/darknet
# YOLO: Real-Time Object Detection: https://pjreddie.com/darknet/yolo/
# https://arxiv.org/abs/2004.10934
# Convolutional Neural Networks – Andrew Ng: https://www.coursera.org/learn/convolutional-neural-networks/lecture/yNwO0/anchor-boxes

import time # Apenas utilizado para calcular o tempo de processamento; poderá ser removido sem prejuízo e poupará tempo de processamento

import cv2
import threading

# Definindo a cor para as caixas de detecção das facas
RECTANGLE_COLOR = (255, 0, 0)

class_names = []
with open('coco.names', 'r') as f:
    class_names = [cname.strip() for cname in f.readlines()]

# Índice da classe 'knife' no COCO dataset
KNIFE_CLASS_ID = 0

# Capturando vídeo da webcam para fazer testes
cap = cv2.VideoCapture(0)

# Carregando a rede YOLOv4: versão tiny
#net = cv2.dnn.readNet('yolov4-tinyVersion\yolov4-tiny.weights', 'yolov4-tinyVersion\yolov4-tiny.cfg')

# Carregando a rede YOLOv4: versão completa (bem mais pesada)
net = cv2.dnn.readNet('yolov4\yolov4.weights', 'yolov4\yolov4.cfg')

# Setando os parâmetros da rede neural
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)

# Variável para armazenar o último frame capturado
last_frame = None

# Bloqueio para garantir que apenas uma thread acesse o frame por vez
lock = threading.Lock()

# Função para capturar frames
def capture_frames():
    global last_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # A thread de captura atualiza o frame atual
        with lock:
            last_frame = frame.copy()

# Função para realizar a detecção de facas nos frames
def detection_frames():
    global last_frame
    while True:
        if last_frame is not None:
            # A thread de processamento utiliza o frame atual
            with lock:
                # Fazendo uma cópia do frame para desenhar as caixas
                frame = last_frame.copy()
            
            start = time.time()
            
            # Os parâmetros 0.3 e 0.4 são os thresholds de confiança e de supressão não máxima, respectivamente. Podem ser ajustados conforme necessário.
            classes, scores, boxes = model.detect(frame, 0.3, 0.4)
            
            end = time.time()
            
            # O tempo de processamento será exibido no frame, para que tenhamos uma ideia do FPS que o thread está processando.
            # Isso pode ser removido para melhorar o desempenho.
            
            # Iterando sobre as detecções e desenhando as caixas
            for (classid, score, box) in zip(classes, scores, boxes):
                if int(classid) == KNIFE_CLASS_ID:
                    label = f'{class_names[int(classid)]}: {score:.2f}'
                    
                    # Desenhando a caixa e mostrando o label
                    cv2.rectangle(frame, box, RECTANGLE_COLOR, 2)
                    cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RECTANGLE_COLOR, 2)
            
            # Calculando e exibindo o FPS; pode ser removido.
            fps_label = f"FPS: {round(1.0 / (end - start), 2)}"
            cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)
            cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
            
            # Mostrando a imagem com as detecções
            cv2.imshow('Knife Detection', frame)
            
        # Saindo do loop ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Criando e iniciando threads para captura de frames e detecção de objetos
capture_thread = threading.Thread(target=capture_frames)
detection_thread = threading.Thread(target=detection_frames)

capture_thread.start()
detection_thread.start()

capture_thread.join()
detection_thread.join()

# Liberando a captura e fechando todas as janelas
cap.release()
cv2.destroyAllWindows()