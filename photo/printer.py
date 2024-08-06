import os
import sys
sys.path.append('D:\\Prywatne\\jul\\flaskProject\\Lib\\site-packages')
import face_recognition
import matplotlib.pyplot as plt
import numpy as np
import json

def decide(face_distances, matches, how_many):
    for _ in range(min(how_many, len(matches))):
        best_match_index = np.argmin(face_distances)
        if not matches[best_match_index]:
            return False
        face_distances[best_match_index] = 1
    return True


if __name__ =="__main__":
    directory = 'D:\\Prywatne\\jul\\python_projekty\\home_server\\photo\\ex'
    with open('ex/convert_test.json', 'r') as convert_file:
        faces_dict = json.load(convert_file)
    for name in faces_dict.keys():
        if name == "Unknown1":
            face_list = faces_dict[name]
            for face in face_list:
                enc, loc, file = face
                img = face_recognition.load_image_file(os.path.join(directory + '\\' + file))
                tmp = img[loc[0]:loc[2], loc[3]:loc[1]]
                plt.imshow(tmp)
                plt.title(f'{name} {file}')
                plt.show()


