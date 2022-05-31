"""
-------------------------------------
Autor: Carlos Mir Martínez  
Fecha: 31/05/2022
Red Neuronal Convolucional Analizador de Neumonías
------------------------------------
"""
# LIBRERIAS
from PIL import Image 
import numpy as np
import tensorflow as tf
import keras
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog 
import tkinter
import warnings
warnings.filterwarnings('ignore')

# Recrea exactamente el mismo modelo solo desde el archivo
NeumoniaRNC = keras.models.load_model('C:/Users/USUARIO/Desktop/NeumoniaImagenes/chest_xray/NeumoniaModelRNC.h5')
 

def browseFiles(): 
    
    display_text.set("")
    
    def Analizar_Imagen():
      
        img = tf.keras.utils.load_img(filename, target_size=[64, 64])
        x = tf.keras.utils.img_to_array(img)
        x = np.array(x) /255
        data = x.reshape(1, 64, 64, 3)
        prediction = NeumoniaRNC.predict(data)
        prediction1 = prediction > 0.9
        prediction = prediction * 100
        if prediction1:
            var = "TIENE NEUMONIA CON 90% PRECISION,\n Precision: " + str(prediction)
        else:
            var = "NO TIENE NEUMONIA,\n Precision: " + str(prediction)
            
        display_text.set(var)
        
        
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.jpeg*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    
    label_file_explorer.configure(text="Imagen Abierta: " +  filename) 

    imagen01 = Image.open(filename)
    imagen02 = imagen01.resize((700,400), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(imagen02)
    label1 = tkinter.Label(image = test)
    label1.image = test   
    label1.place(x=0, y = 250)
    
    button_analize = Button(window, text = 'Analizar', command=Analizar_Imagen )  
    button_analize.grid(column=0, row = 3)
                                                                                                   
window = Tk() 
  
display_text = tk.StringVar()
 
window.title('Analizador de imagenes') 
   
window.geometry("700x700") 

window.config(background = "white") 
   


label_file_explorer = Label(window,  
                            text = "Explorador de Archivos", 
                            width = 100, height = 4,  
                            fg = "blue") 

label_prediction = Label(window, textvariable = display_text, width = 100, height = 4,  fg = "green" )

button_explore = Button(window,  
                        text = "Explorar Imagenes de TAC", 
                        command = browseFiles)  

 

button_exit = Button(window, text = "Salir", command = window.destroy)  
   
label_file_explorer.grid(column = 0, row = 1) 
   
button_explore.grid(column = 0, row = 2) 

button_exit.grid(column = 0,row = 4) 

label_prediction.grid(column = 0, row = 5)

window.mainloop()