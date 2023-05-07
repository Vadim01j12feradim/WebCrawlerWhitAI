import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers

import os

from keras.preprocessing.image import ImageDataGenerator
import pickle

if tf.test.gpu_device_name(): 

    print('Default GPU Device:{}'.format(tf.test.gpu_device_name()))

else:

   print("Please install GPU version of TF")
def trainModel():

    training_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2
        )
    test_datagen = ImageDataGenerator(
            rescale=1./255
        )

    train_ds=training_datagen.flow_from_directory(
        #first we get the folder where the images are stored in an organized way 
        "Images",
        #we provide the list of classes to have a consistent ordering of classes between train and test set apple->0 banana->1 etc
        classes=["yes","no"],
        #how we want to load images, we want them as rgb images so with 3 channels
        color_mode="rgb",
        #size of batches to group images
        batch_size=16,
        #resize images to match this fixed dimension
        target_size=(64,64),
        #have classes one hot encoded 
        class_mode="categorical",
        #get the training subset 
        subset="training"
    )
    valid_ds=training_datagen.flow_from_directory(
        "Images",
        classes=["yes","no"],
        color_mode="rgb",
        batch_size=16,
        target_size=(64,64),
        class_mode="categorical",
        subset="validation"
    )

    model = tf.keras.models.Sequential([    
        #Convolutional part
        layers.Conv2D(64, 2,  activation='gelu',input_shape=(64,64,3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 2,  activation='gelu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),
        layers.Flatten(),
        
        #Dense portion, with high dropout rate for a high regualization
        layers.Dense(64, activation='gelu'),
        layers.Dropout(0.8),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                loss='categorical_crossentropy',
                metrics=['accuracy',"binary_accuracy"])
    model.summary()
    history=model.fit(train_ds,epochs=30,verbose=1)
    model.save('Model.h5')