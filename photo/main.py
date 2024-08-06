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
        faces_dict_2 = json.load(convert_file)
    faces_dict = {}

    i = 0
    for name in faces_dict_2.keys():
        if name[:7] == "Unknown":
            i = max(i, int(name[7:]))
        face_list = faces_dict_2[name]
        faces_dict[name] = []
        for face in face_list:
            enc, loc, file = face
            faces_dict[name].append((np.array(enc), loc, file))

    i += 1
    print(i)
    files_list = os.listdir(directory)
    print(files_list)
    for plik in files_list:
        print(f"robie {plik}")
        if plik.endswith('.jpg') or plik.endswith('.jpeg') or plik.endswith('.png') or plik.endswith('.JPG') or plik.endswith('.JPEG'):
            img = face_recognition.load_image_file(directory + '\\' + plik)
            # Wczytanie obrazu
            # img_rot = np.rot90(img, k=2)

            # Znalezienie twarzy na obrazie
            face_locations = face_recognition.face_locations(img)
            print(face_locations)
            face_encodings = face_recognition.face_encodings(img, face_locations)
            if len(face_encodings) != 0:
                for idx, face_encoding in enumerate(face_encodings):

                    # dodanie do słownika z twarzami
                    was_added = False
                    for face_name in faces_dict.keys():
                        face_list = [i[0] for i in faces_dict[face_name]]
                        matches = face_recognition.compare_faces(face_list, face_encoding)
                        face_distances = face_recognition.face_distance(face_list, face_encoding)
                        if decide(face_distances, matches, 3):
                            faces_dict[face_name].append((face_encoding, face_locations[idx], directory + "\\" + plik))
                            faces_dict_2[face_name].append((face_encoding.tolist(), face_locations[idx], directory + "\\" + plik))
                            was_added = True
                            break
                        if was_added:
                            break
                    if not was_added:
                        name = "Unknown" + str(i)
                        faces_dict[name] = [(face_encoding, face_locations[idx], plik)]
                        faces_dict_2[name] = [((face_encoding.tolist(), face_locations[idx], plik))]
                        i += 1

    # for name in faces_dict.keys():
    #     face_list = faces_dict[name]
    #     if len(face_list) > 1:
    #         figure, axis = plt.subplots(len(face_list))
    #         for idx, face in enumerate(face_list):
    #             enc, loc, file = face
    #
    #             img = face_recognition.load_image_file(os.path.join(directory, file))
    #             tmp = img[loc[0]:loc[2], loc[3]:loc[1]]
    #             # For Sine Function
    #             axis[idx].imshow(tmp)
    #
    #         plt.show()
    #     else:
    #         enc, loc, file = face_list[0]
    #         img = face_recognition.load_image_file(os.path.join(directory, file))
    #         tmp = img[loc[0]:loc[2], loc[3]:loc[1]]
    #         plt.imshow(tmp)
    #         plt.show()

    with open('ex/convert_test.json', 'w') as convert_file:
        convert_file.write(json.dumps(faces_dict_2))

