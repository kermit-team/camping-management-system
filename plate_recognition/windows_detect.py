import re
import cv2
import tensorflow as tf
import numpy as np
import requests
import easyocr

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

def load_labels(path='labels.txt'):
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = np.expand_dims((image-255)/255, axis=0)

def get_output_tensor(interpreter, index):
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  boxes = get_output_tensor(interpreter, 1)
  classes = get_output_tensor(interpreter, 3)
  scores = get_output_tensor(interpreter, 0)
  count = int(get_output_tensor(interpreter, 2))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results

def save_text_to_file(text, file_path):
    with open(file_path, 'a') as file:
        file.write(str(text[0]))

def fetch_data_from_api(arg):
    try:
        url = 'http://127.0.0.1:8000/api/cars/able-to-enter-camping/'
        params = {'registration_plate': '{arg}'}
        
        response = requests.post(url, json=params)
        response.raise_for_status()
        data = response.json()
        
        print("Samochod " + str(arg))
        if(data['car_exists']):
            print('jest w systemie')
        else:
            print('nie istnieje w systemie')

        if(data['car_able_to_enter_camping']):
            print('moze wjechac na teren campingu')
        else:
            print('nie moze wjechac na teren campingu')

    except requests.exceptions.RequestException as e:
        print("Wystapil blad podczas pobierania danych:", e)

def main():
    labels = load_labels()
    interpreter = tf.lite.Interpreter('detect.tflite')
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
    print(interpreter.get_input_details())

    cap = cv2.VideoCapture(1)
    while cap.isOpened():
        ret, frame = cap.read()
        img = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (320,320))
        res = detect_objects(interpreter, img, 0.5)

        for result in res:
            ymin, xmin, ymax, xmax = result['bounding_box']
            xmin = int(max(1,xmin * CAMERA_WIDTH))
            xmax = int(min(CAMERA_WIDTH, xmax * CAMERA_WIDTH))
            ymin = int(max(1, ymin * CAMERA_HEIGHT))
            ymax = int(min(CAMERA_HEIGHT, ymax * CAMERA_HEIGHT))

            cv2.rectangle(frame,(xmin, ymin),(xmax, ymax),(0,255,0),3)
            cv2.putText(frame,labels[int(result['class_id'])],(xmin, min(ymax, CAMERA_HEIGHT-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA)
            roi = frame[ymin:ymax, xmin:xmax]

            reader = easyocr.Reader(['en'])
            read_text = reader.readtext(roi)
            if not read_text:
              pass
            elif len(read_text[0]) > 1 != "":
              final_text = read_text[0][1].replace(" ","")
              fetch_data_from_api(final_text)
              #save_text_to_file(final_text, 'recognized_text.txt')
            
        cv2.imshow('Pi Feed', frame)

        if cv2.waitKey(10) & 0xFF ==ord('q'):
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
