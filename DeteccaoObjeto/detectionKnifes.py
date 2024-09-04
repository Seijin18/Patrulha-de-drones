import time
import cv2

def detect_knife(img_frame):

    # Definindo cores e classes
    RECTANGLE_COLOR = (255, 0, 0)

    class_names = []
    with open('coco.names', 'r') as f:
        class_names = [cname.strip() for cname in f.readlines()]

    # Índice da classe 'knife' no COCO dataset
    KNIFE_CLASS_ID = 0

    # Carregando a rede YOLOv4-tiny
    net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')

    # Setando os parâmetros da rede neural
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255)

    # Lendo os frames e identificando objetos
    while True:
        
        start = time.time()
        
        # Detectando objetos no frame
        classes, scores, boxes = model.detect(img_frame, 0.3, 0.4)
        
        end = time.time()
        
        for (classid, score, box) in zip(classes, scores, boxes):
            # Verificando se a classe detectada é uma faca
            if int(classid) == KNIFE_CLASS_ID:
                label = f'{class_names[int(classid)]}: {score:.2f}'
                
                # Desenhando a caixa e mostrando o label
                cv2.rectangle(img_frame, box, RECTANGLE_COLOR, 2)
                cv2.putText(img_frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RECTANGLE_COLOR, 2)
        
        # Calculando e exibindo o FPS
        fps_label = f"FPS: {round(1.0 / (end - start), 2)}"
        cv2.putText(img_frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)
        cv2.putText(img_frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        
        # Mostrando a imagem com as detecções
        cv2.imshow('Knife Detection', img_frame)
        
        # Encerrando o loop ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Liberando a captura e fechando todas as janelas
    img_frame.release()
    cv2.destroyAllWindows()
