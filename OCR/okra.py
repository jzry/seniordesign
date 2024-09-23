import torch
import torchvision.transforms as transforms
import numpy as np
import cv2
import matplotlib.pyplot as plt

class OkraDigitGetter:
    
    def __init__(self):
        # Load model
        self.__model = torch.load('./okra3.model', weights_only=False)
        self.__model.to('cpu')
        self.__model.eval()
        
        # Set default parameters
        self.debug_images = False
        self.column_skip = 5
    
    def __preprocess_image(self, img):
        kernel = np.ones((3,3),np.float32)/90
        img = cv2.filter2D(img,-1,kernel)
        _, img = cv2.threshold(
            img,
            13, # this value probably needs to be adjusted based on lighting conditions
            255,
            cv2.THRESH_BINARY_INV,
        )
        return img
        
    def digit_from_image(self, img):
        img = self.__preprocess_image(img)
        return self.__digit_from_image(img)
        
    def __digit_from_image(self, img):
        prep = transforms.Compose([transforms.ToTensor(), transforms.Resize((28, 28))])
        img = prep(img)
        if self.debug_images:
            plt.imshow(img.view((28, 28)).numpy())
            plt.show()
        img = img.reshape((1, 1, 28, 28))
        #img = torch.flatten(img)
        pred = self.__model(img)
        class_num = torch.argmax(pred)
        probs = torch.nn.functional.softmax(pred[0], dim=0)
        confidence = probs[class_num] * 100
        return (class_num.item(), confidence.item())
    
    def image_to_digits(self, img):
        img = self.__preprocess_image(img)
        numbers = []
        confidence = []
        # Traverse the image top-down, left-right
        x = 0
        while x < img.shape[1]:
            y = 0
            while y < img.shape[0]:
                if img[y, x] > 0:
                    seg = self.__get_character_segment(img, x, y)
                    num, conf = self.__digit_from_image(seg)
                    numbers.append(num)
                    confidence.append(conf)
                    x = self.__max_x
                    break
                y = y + 1
            x = x + self.column_skip
                    
        return (numbers, confidence)
                    
    
    def __get_character_segment(self, img, start_x, start_y):
        self.__min_x = start_x
        self.__max_x = start_x
        self.__min_y = start_y
        self.__max_y = start_y
        # Calculate the min/max values by doing a recursive 'space fill' search algorithm thing...
        self.__traverse(img, start_x, start_y)
        # Get borders
        paddingVert = 20
        paddingHoriz = 30
        left = max(self.__min_x - paddingHoriz, 0)
        right = min(self.__max_x + paddingHoriz, img.shape[1] - 1)
        top = max(self.__min_y - paddingVert, 0)
        bottom = min(self.__max_y + paddingVert, img.shape[0] - 1)
        
        return img[top:bottom, left:right]
        
    def __traverse(self, img, x, y):
        # Check if we're in bounds
        if x < 0 or x >= img.shape[1]:
            return
        if y < 0 or y >= img.shape[0]:
            return
        
        # Check if this is part of the background
        if img[y,x] == 0:
            return
        
        # Check if we've been here before
        if img[y,x] == 254:
            return
        
        # Mark this spot
        img[y,x] = 254
        
        # Set max and min values
        if x > self.__max_x:
            self.__max_x = x
        if x < self.__min_x:
            self.__min_x = x
        if y > self.__max_y:
            self.__max_y = y
        if y < self.__min_y:
            self.__min_y = y
            
        # Move to the surrounding pixels
        for move_x in range(-1, 2, 1):
            for move_y in range(-1, 2, 1):
                self.__traverse(img, x + move_x, y + move_y)
    
                
    