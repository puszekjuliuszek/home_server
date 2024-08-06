import os
import sys
import numpy as np
# import matplotlib.pyplot as plt
import cv2
import matplotlib.image



if __name__ =="__main__":
    directory = 'D:\\Prywatne\\jul\\python_projekty\\home_server\\photo\\framing'
    files_list = os.listdir(directory)
    for file in files_list:
        size = 3200
        img = cv2.imread(os.path.join(directory, file), cv2.COLOR_RGB2BGR)
        back = np.ones((size, size, 3), dtype=np.uint8) * 255
        back[(size-img.shape[0])//2:(size+img.shape[0])//2, (size-img.shape[1])//2:(size+img.shape[1])//2] = img
        # back = np.full((3200,3200),255)
        # back[] = img
#         plt.gray()
#         plt.imshow(back)
#         print(file, img.shape)
        matplotlib.image.imsave(f"{file.split('.')[0]}.png", back)