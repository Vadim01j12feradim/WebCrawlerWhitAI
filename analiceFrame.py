import cv2
import numpy as np
import tensorflow as tf
import os
import probes as HTML
# //Installs
import subprocess
import html

def analize(frame):
    model=tf.keras.models.load_model("Model.h5")

    faceCascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    #####################################

    # Add text to the image
    position = (265, 42)  # (x, y) position of the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.8
    fontClar = 3
    textColor = (240, 255, 255)  # BGR color tuple in OpenCV format
    ###################################
    imagenGrises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imagenRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    faces = faceCascade.detectMultiScale(
        imagenGrises,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(60, 60)
    )
    #por cada cara detectada pintar un cuadro
    print("Faces in image: ",len(faces))
    text = "no"
    for (x, y, w, h) in faces:
        # cv2.putText(x,y,"of course")
        rostro=cv2.resize(frame[y:y+h,x:x+w],(64,64))
        rostroRGB=cv2.resize(imagenRGB[y:y+h,x:x+w],(64,64))
        rostroRGB=rostroRGB/255.0
        rostro=rostro/255.0
        classes=["yes ","no"]
        output=model.predict(np.array([rostroRGB]))
        print(output)
        output=np.argmax(output ,axis=1)
        print(output)
        print("Output is: ",classes[output.squeeze()])

        text = classes[output.squeeze()]

        (textWidth, textHeight), _ = cv2.getTextSize(text, font, fontScale, fontClar)
        posX = x -54
        posY = y - textHeight - 10 -18
        posWidth = textWidth + 20
        posHeight = textHeight + 20
        cv2.rectangle(frame, (posX, posY), (posX + posWidth, posY + posHeight), (0, 150, 255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, text, (x-45, y-20), font, fontScale, textColor, fontClar)
    cv2.imshow("Image with Text", frame)
    print("\n\n\n\n\n\n\n\n'",text.replace(" ", ""),"'")
    if(text.replace(" ", "") == "yes"):
        print("saving image ...","\n\n\n\n\n\n\n\n")
        path = 'Person'  # Reemplazar con la ruta de la carpeta que deseas analizar
        num = 0
        # Iterar sobre los nombres de archivo en la carpeta
        for file_name in os.listdir(path):
            num += 1  # Incrementar el contador de archivos
        num += 1
        link = "Person/"+str(num)+".jpg"
        cv2.imwrite(link,frame)
        HTML.addLinkIMG(link)
        resultado = subprocess.run(["exiftool", link], capture_output=True, text=True)
        outHTML = html.escape(resultado.stdout)
        OUT = outHTML = f'<pre>{outHTML}</pre>'
        HTML.addIMGMetadata(OUT)
        return True

    cv2.waitKey(100)
                # Close all OpenCV windows
    cv2.destroyAllWindows()
    return False
    # dir = "Saved"
    # size = os.listdir(dir)
    # Fs = len(size)
    # cv2.imwrite(dir+"/"+str(Fs+1)+".jpg")
