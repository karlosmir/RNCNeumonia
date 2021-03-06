"""
RED NEURONAL CONVOLUCIONAL, 
Dataset con fotos de neumonia
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator # Preprocesa las images y rescala
import warnings
import cv2
import os
warnings.filterwarnings('ignore')

# Visualizacion
labels = ['PNEUMONIA', 'NORMAL']
img_size = 150

def get_data(data_dir):
    data = [] 
    for label in labels: 
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

train = get_data('C:/Users/USUARIO/Desktop/NeumoniaImagenes/chest_xray/train')
test = get_data('C:/Users/USUARIO/Desktop/NeumoniaImagenes/chest_xray/test')

### PNEUMONIA PLACA TORAAX
plt.figure(figsize = (5,5))
plt.imshow(train[0][0], cmap='gray')
plt.title(labels[train[0][1]]) # 0 imagen pneumonia

### NORMAL PLACA TORAAX
plt.figure(figsize = (5,5))
plt.imshow(train[-1][0], cmap='gray')
plt.title(labels[train[-1][1]]) # -1 imagen normal


# Preprocesado
# Rescala las imagenes del Train
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
# Rescala las imagenes del test
test_datagen = ImageDataGenerator(rescale = 1./255)

# Creando el DF Training SET
training_set = train_datagen.flow_from_directory('C:/Users/USUARIO/Desktop/NeumoniaImagenes/chest_xray/train',
                                                 target_size = (64, 64),
                                                 class_mode = 'binary')

# Creando el DF Test SET
test_set = test_datagen.flow_from_directory('C:/Users/USUARIO/Desktop/NeumoniaImagenes/chest_xray/test',
                                            target_size = (64, 64),
                                            class_mode = 'binary')

# Creamos la red RNC, Convolucion --> Pooling --> Flattenin --> Full Connect
RNC = tf.keras.models.Sequential()
# 1?? Capa Convolucion2D, entrada de datos
RNC.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu", input_shape=[64, 64, 3]))
# 2?? Capa - Pooling, Simplifica los problemas y reduce las operaciones
RNC.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='valid'))
# 3?? Capa de Convolucion y Pooling
RNC.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"))
RNC.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='valid'))
# 4?? Capa - Flattening, adapta la estructura de forma vertical en una columna
RNC.add(tf.keras.layers.Flatten())
# Full Connection, a??adimos la red neuronal totalmentne conectada
RNC.add(tf.keras.layers.Dense(units=128, activation='relu'))
# Capa de Salida
RNC.add(tf.keras.layers.Dense(units=1, activation='sigmoid')) # Funcion sigmoide

# Compilamos el modelos con el optimizador Adam y entropia cruzada binaria
RNC.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Entrenamos el modelo
RNC.fit_generator(training_set,
                  steps_per_epoch = 20,
                  epochs = 25,
                  validation_data = test_set
                  ) 

RNC.save('C:/Users/USUARIO/Desktop/NeumoniaImagenes/chest_xray/NeumoniaModelRNC.h5')