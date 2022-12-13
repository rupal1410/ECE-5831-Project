# Drowsiness Detection System
Created By : Rupal Choudhary

## Problem Statement
The National Highway Traffic Safety Administration estimates that approximately 100,000 police-reported, drowsy-driving crashes result in nearly 800 fatalities and about 50,000 injuries every day. 
These are just the cases that are reported to the police. To deal with this issue several automotive companies have produced various driver assistance systems like cruise control, lane departure warning, assisted steering, fatigue warning etc.
Continuous development is being done in the recent years for the advancement of Drowsiness Detection System in automotive industry.


### Data Acquisition 
In this project I have used the DROZY Dataset which is collected by the Laboratory for Signal and Image Exploitation (INTELSIG), which is part of the Department of Electrical Engineering and Computer Science of the University of Liège (ULg), Liège, Belgium! (http://www.drozy.ulg.ac.be/). 

### Modelling
The aim of the project is to create a CNN model that detects Open or Closed Eyes. The project also includes a python code that takes a live webcam footage and takes frames and predict if the eye is open or close. If the eye is open for 5 consecutive frames then it gives out a warning.

CNN models can not take videos as an input. The videos from the DROZY Dataset were converted into frames. Then the open and closed eye frames were manually segmented into individual folders. Then with the help of face-recognition library built by dlib the eyes were detected, cropped and saved as imaged of size 80x 80 pixels.

Once the dataset is ready, multiple CNN models were trained and the performance was evaluated. This model had the best results. The CNN Model I used here consists of 3 convolutional layers, number of filters were 32 in a 3 x 3 size. each convolutional layer was followed by a  2x2 pooling layer , then a dense layer is applied with 128 neurons. Since the expected output is binary either close eye or open eye I have used sigmoid function in the output layer.

The dataset was divided into training and validation dataset with 20% of the data being validation dataset, Training data 3384 images, Testing data 846 images 

The model was trained on the training dataset and then tested on validation dataset and I was able to achieve 98% accuracy.

![image](https://user-images.githubusercontent.com/84277254/207199306-0872d0b1-5dbf-44d7-a82a-49cb93269907.png)

Specificity: 0.9788135593220338
Sensitivity / Recall: 0.9866310160427807 
Accuracy: 0.9822695035460993 
Precision: 0.9736147757255936 


