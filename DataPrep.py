# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 14:07:45 2022

@author: Rupal Choudhary
"""

import os
import face_recognition
from PIL import Image
import cv2 as cv

class DataPrep:
    def __init__(self):
        pass
    
    def get_data(self,dir_path,size = 512):
        labels = ['Open', 'Close']
        count = 0
        error_count = 0
        IMG_SIZE = size
        data = []
        for label in labels:
            path = os.path.join(dir_path, label)
            class_num = labels.index(label)
            class_num +=0
            print(class_num)
            for img in os.listdir(path):
                try:
                    img_array = cv.imread(os.path.join(path, img), cv.IMREAD_COLOR)
                    resized_array = cv.resize(img_array, (IMG_SIZE, IMG_SIZE))
                    #resized_array = np.array(resized_array)
                    data.append([resized_array, class_num])
                except Exception as e:
                    print(e)
                    error_count += 1
                    print('ErrorCount = ' + str(error_count))
                    continue
                count += 1
                if count % 500 == 0:
                    print('Succesful Image Import Count = ' + str(count))
        return data
    
    def write_data(self,path,feature, y):
        labels = ['Open', 'Close']
        for label in labels:
            location = os.path.join(path, label)
            for img in range(feature.shape[0]):
                try:
                    filename = '/'+label+str(img)+'.jpg'
                    fullpath = location+filename
                    if label == labels[y[img]]:
                        print('Writing Image...',fullpath)
                        cv.imwrite(fullpath,feature[img])
                except Exception as e:
                    print(e)
                    

    def eye_cropper(self,loc):
        count = 0
      
        for folder in os.listdir(loc):
            path = os.path.join(loc, folder)
            print(folder)
            for img in os.listdir(path):
                # Using Facial Recognition Library on Image
                image = face_recognition.load_image_file(os.path.join(path, img))
                print('loading image...')
                
                face_landmarks_list = face_recognition.face_landmarks(image)

                eyes = []
                try:
                    eyes.append(face_landmarks_list[0]['left_eye'])
                    eyes.append(face_landmarks_list[0]['right_eye'])
                except:
                    continue
    
                for eye in eyes:
                    x_max = max([coordinate[0] for coordinate in eye])
                    x_min = min([coordinate[0] for coordinate in eye])
                    y_max = max([coordinate[1] for coordinate in eye])
                    y_min = min([coordinate[1] for coordinate in eye])
    
                  # establish the range of x and y coordinates    
                    x_range = x_max - x_min
                    y_range = y_max - y_min
                  

                    if x_range > y_range:
                        right = round(0.7*x_range) + x_max
                        left = x_min - round(0.7*x_range)
                        bottom = round(((right-left) - y_range))/2 + y_max
                        top = y_min - round(((right-left) - y_range))/2
                    else:
                        bottom = round(0.7*y_range) + y_max
                        top = y_min - round(0.7*y_range)
                        right = round(((bottom-top) - x_range))/2 + x_max
                        left = x_min - round(((bottom-top) - x_range))/2
 
                    im = Image.open(os.path.join(path, img))
                  
                    im = im.crop((left, top, right, bottom))
                    im = im.resize((80,80))
                    
                    save = 'path/to/save/cropped/eye/images/'+ folder
                    print('Saving File',save)
                    im.save(save+'/crop' + str(count) + '.jpg')
                    count += 1
                  
                    if count % 100 == 0:
                        print(count)
        