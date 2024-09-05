import cv2
import numpy as np
import datetime as dt

# Carregando as classes do COCO dataset
class_names = []
with open('DeteccaoObjeto/coco.names', 'r') as f:
    class_names = [cname.strip() for cname in f.readlines()]

# Índice da classe 'knife' no COCO dataset = 43
# Índice da classe 'person' no COCO dataset = 0
# Índice da classe 'mouse' no COCO dataset = 64

KNIFE_CLASS_ID = 64

'''
me = Tello()
me.connect()
print(f"Battery: {me.get_battery()}%")
me.streamoff()
me.streamon()
'''
cv2.cuda.getCudaEnabledDeviceCount()

# Capturando vídeo da webcam do notebook
cap = cv2.VideoCapture(0)

# Carregando a rede YOLOv4-tinyq
net = cv2.dnn.readNet('DeteccaoObjeto/yolov4-tinyVersion/yolov4-tiny.weights', 'DeteccaoObjeto/yolov4-tinyVersion/yolov4-tiny.cfg')

# Verificando se há suporte para GPU
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print('CUDA enabled devices found, using GPU for inference')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
else:
    print('CUDA enabled devices not found, using CPU for inference')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Configurando os parâmetros da rede neural
model = cv2.dnn_DetectionModel(net)

# Reduzi o tamanho da entrada para melhorar a velocidade do modelo; size=(320, 320), size=(416, 416) ou size=(608, 608)
model.setInputParams(size=(320, 320), scale=1 / 255)


# Função para detectar facas em um frame
def detect_knifes(frame):
    
    # Detectando objetos no frame
    classes, scores, boxes = model.detect(frame, confThreshold=0.4, nmsThreshold=0.4)

    detected = False
    for (classid, score, box) in zip(classes, scores, boxes):
        if int(classid) == KNIFE_CLASS_ID:  # Apenas detecta facas
            label = f'{class_names[int(classid)]}: {score:.2f}'
            
            # Desenhando a caixa e mostrando o label
            cv2.rectangle(frame, box, (255, 0, 0), 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            detected = True  # Marca que uma faca foi detectada
    
    return frame, detected

def combine_images(images, rows, cols, scale=0.5):
    
    spacing = 5 # Espaçamento entre as imagens de 10 pixels
    
    # Redimensiona e organiza as imagens em uma grade
    height, width = images[0].shape[:2]
    new_height, new_width = int(height * scale), int(width * scale)
    combined_height = rows * new_height + (rows - 1) * spacing
    combined_width = cols * new_width + (cols - 1) * spacing
    
    # Cria uma imagem preta para combinar as imagens redimensionadas em seguida
    combined_image = np.zeros((combined_height, combined_width, 3), dtype=np.uint8)

    # Itera sobre as imagens e as redimensiona na grade
    for idx, image in enumerate(images):
        resized_image = cv2.resize(image, (new_width, new_height))
        row = idx // cols
        col = idx % cols
        y_start = row * (new_height + spacing)
        x_start = col * (new_width + spacing)
        
        # Adiciona a imagem redimensionada à imagem combinada
        combined_image[y_start:y_start+new_height, x_start:x_start+new_width] = resized_image

    return combined_image

def main():
    detected_images = []
    frame_skip = 5  # Número de frames a serem ignorados entre as detecções
    frame_count = 0
    
    while True:
        # Capturando frame da webcam
        ret, frame = cap.read()
        if not ret:
            break
        
        '''
        frame_read = me.get_frame_read()
        frame = frame_read.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        '''
        
        frame_count += 1

        # Se o número de frames capturados for múltiplo de frame_skip
        if frame_count % frame_skip == 0:
            # Detectando facas no frame capturado
            frame, detected = detect_knifes(frame)

            if detected:
                detected_images.append(frame.copy())  # Armazenando o frame com detecção

            # Se cinco imagens forem detectadas, combinar e exibir
            if len(detected_images) == 6:
                combined_image = combine_images(detected_images, rows=2, cols=3)
                cv2.imshow('Knife Detection - Combined', combined_image)
                detected_images = []  # Reiniciar a lista de detecções

        # Exibindo a imagem com as detecções
        cv2.imshow('Knife Detection - Webcam', frame)

        # Encerrando o loop ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberando a captura de vídeo e fechando as janelas
    cap.release()
    # me.streamoff()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
