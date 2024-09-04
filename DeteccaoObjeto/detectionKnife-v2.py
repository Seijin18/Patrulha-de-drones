import time
import cv2
from djitellopy import Tello

# Definindo cores e classes
RECTANGLE_COLOR = (255, 0, 0)

class_names = []
with open('coco.names', 'r') as f:#ALTERAR SE NECESSARIO
    class_names = [cname.strip() for cname in f.readlines()]

KNIFE_CLASS_ID = 43 #escolhe a faca

me = Tello()
me.connect()
print(f"Battery: {me.get_battery()}%")
me.streamoff()
me.streamon()

# ALTERAR COM O CAMINHO CORRETO / OU \
net = cv2.dnn.readNet('yolov4/yolov4-tiny.weights', 'yolov4/yolov4-tiny.cfg')

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1 / 255)


def detect_knifes(frame):
    start = time.time()

    classes, scores, boxes = model.detect(frame, 0.3, 0.4)

    end = time.time()

    for (classid, score, box) in zip(classes, scores, boxes):
        # Verificando se a classe detectada é uma faca
        if int(classid) == KNIFE_CLASS_ID:
            label = f'{class_names[int(classid)]}: {score:.2f}'

            # Desenhando a caixa e mostrando o label
            cv2.rectangle(frame, box, RECTANGLE_COLOR, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RECTANGLE_COLOR, 2)

    # Calculando e retornando o FPS e o frame processado
    fps = round(1.0 / (end - start), 2)
    return frame, fps


def main():
    # ALTERAR ESSA PARTE USAR APENAS A FUNCAO COM ALGUNS ITENS ABAIXO
    while True:
        # ESSA PARTE PEGA OS FRAMES
        frame_read = me.get_frame_read()
        frame = frame_read.frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # AQUI ELE RETORNA OS FRAMES, O FPS E EXIBE O VIDEO DETECTANDO
        frame, fps = detect_knifes(frame)
        fps_label = f"FPS: {fps}"
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

        cv2.imshow('Knife Detection - Tello', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    me.streamoff()
    cv2.destroyAllWindows()

if __name__ == "_main_":
    main()