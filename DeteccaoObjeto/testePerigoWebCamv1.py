import cv2

# Carregando as classes do COCO dataset
class_names = []
with open('DeteccaoObjeto/coco.names', 'r') as f:
    class_names = [cname.strip() for cname in f.readlines()]

# Índice da classe 'knife' no COCO dataset = 43
KNIFE_CLASS_ID = 0

# Capturando vídeo da webcam do notebook
cap = cv2.VideoCapture(0)  # 0 é o índice da webcam integrada do notebook

# Carregando a rede YOLOv4-tiny e habilitando o uso de CUDA, se disponível
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
model.setInputParams(size=(320, 320), scale=1 / 255)  # Reduzindo o tamanho da entrada para melhorar a velocidade



# Função para detectar facas em um frame
def detect_knifes(frame, countKnifes):
    
    # Detectando objetos no frame
    classes, scores, boxes = model.detect(frame, confThreshold=0.4, nmsThreshold=0.4)

    # Iterando sobre as detecções e desenhando as caixas
    for (classid, score, box) in zip(classes, scores, boxes):
        if int(classid) == KNIFE_CLASS_ID:  # Apenas detecta facas
            label = f'{class_names[int(classid)]}: {score:.2f}'
            
            # Desenhando a caixa e mostrando o label
            cv2.rectangle(frame, box, (255, 0, 0), 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            countKnifes += 1
            
        else:
            continue

    if countKnifes > 5:
        flag = 1
        countKnifes = 0
        return frame, flag, countKnifes
    else:
        flag = 0
        return frame, flag, countKnifes

def main():
    
    flag, countKnifes = 0
    images = []
    
    frame_skip = 5
    frame_count = 0
    
    while True:
        # Capturando frame da webcam
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1

        # Se o número de frames capturados for múltiplo de frame_skip; isso melhora a eficiência da CPU, visto que somente alguns frames serão analisados pela YOLOv4-tiny
        if (frame_count % frame_skip) == 0:
            print("aqui")
            # Detectando facas no frame capturado
            frame, flag, countKnifes = detect_knifes(frame, countKnifes)
        else:
            continue

        if flag == 1:
            print('Faca detectada!')
            images.append(frame)
        else:
            continue
        
        if len(images) > 5:
            # Mostrar todas as imagens salvas na variável images
            for i in range(len(images)):
                cv2.imshow('Knife Detection - Webcam', images[i])
                            
            images = []
            print("Detecção de três facas realizada com sucesso!")
            
        # DEBUGGGG
        
        # Exibindo as imagens vindas do drone
        cv2.imshow('Detection - Webcam', frame)

        # Encerrando o loop ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberando a captura de vídeo e fechando as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
