from okra import OkraDigitGetter
import cv2
from termcolor import colored


dg = OkraDigitGetter()

dg.debug_images = True


img = cv2.imread(r'Test Images\neat_pencil.jpg', 0) # 0 is for monochrome

numbers, confidence = dg.image_to_digits(img)


for i in range(len(numbers)):
    if confidence[i] > 90.0:
        print(numbers[i], colored(f'({confidence[i]:>.2f}%)', 'green', attrs=['bold']))
    elif confidence[i] > 80.0:
        print(numbers[i], colored(f'({confidence[i]:>.2f}%)', 'yellow', attrs=['bold']))
    else:
        print(numbers[i], colored(f'({confidence[i]:>.2f}%)', 'red', attrs=['bold']))
