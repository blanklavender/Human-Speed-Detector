import cv2
import numpy as np
import random
from collections import deque
import matplotlib.pyplot as plt
import os
import time
import sys

def speed_detection2(input_name, output_name, y_n,y_n2):
    cnt = 0
    if os.path.isfile(input_name)==False:
        return 0

    if(input_name.endswith('mp4') or input_name.endswith('m4v') or input_name.endswith('avi') or input_name.endswith('mkv')):
        cnt = cnt+1
    else:
        return 0

    cap = cv2.VideoCapture(input_name)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frameCount<=5 or frameCount>200:
        return 0

    fps_var = int(cap.get(cv2.CAP_PROP_FPS))
    if fps_var<5 or fps_var>10:
        return 0

    if y_n=='Y' or y_n=='y' or y_n=='N' or y_n=='n':
        if y_n2=='Y' or y_n2=='y' or y_n2=='N' or y_n2=='n':
            return 1
        else:
            return 0
    else:
        return 0
    # print(input_name)
    return 1

def make_new_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

def speed_detection(input_name, output_name, y_n):
    CONFIDENCE = 0.5
    SCORE_THRESHOLD = 0.5
    IOU_THRESHOLD = 0.5
    count = 0
    centroids_list = deque([])
    face_count = 0
    listofspeeds = []
    config_path = "yolov3.cfg"
    weights_path = "yolov3.weights"
    font_scale = 1
    thickness = 1
    labels = open("coco.names").read().strip().split("\n")
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    # read the file from the command line
    video_file = sys.argv[0]
    cap = cv2.VideoCapture(input_name)
    _, image = cap.read()
    h, w = image.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_name, fourcc, cv2.CAP_PROP_FPS, (w, h))

    while True:
        rc, image = cap.read()

        if rc!=True:
            break

        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.perf_counter()
        layer_outputs = net.forward(ln)
        time_took = time.perf_counter() - start
        print("Time took:", time_took)
        boxes, confidences, class_ids = [], [], []

        # loop over each of the layer outputs
        for output in layer_outputs:
            # loop over each of the object detections
            for detection in output:
                # extract the class id (label) and confidence (as a probability) of
                # the current object detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # discard weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > CONFIDENCE:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # perform the non maximum suppression given the scores defined before
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD)

        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]
                # current frame info
                xA = x
                xB = x + w
                yA = y
                yB = y + h
                # Enumerate over all the faces in centroids_list
                # each centroid_list element contains: [last_updated_frame, color, position,
                # lock_count, unlock_count, lockstate (unlocked by default), list_of_face_speeds_in_prev_frames, id]
                not_matched = True
                for idx, centroid_data in enumerate(centroids_list):
                    if centroid_data[0] == count:
                        continue
                    if centroids_list[idx][4] == 0:
                        centroids_list[idx][5] = "unlocked"
                        centroids_list[idx][4] = 5

                    # centroid_data[2] is previous frame ka info
                    # check proximity using manhattan distance
                    # X,Y is the distances between initial and final positions
                    X = abs(float(centroid_data[2][0] + centroid_data[2][2]) / 2 - float(xA + xB) / 2)
                    Y = abs(float(centroid_data[2][1] + centroid_data[2][3]) / 2 - float(yA + yB) / 2)
                    # if there is a rectangle in "n/2" pixel proximity of a rectangle of previous frame than i am assuming that,
                    # the face in the rectangle is same as it was in the previous frame
                    # 10 can be changed to any other value based on the movement happening in the frames, if vehicles are moving
                    # more than 10 pixels per frame suppose 20 so change the value to 20
                    alpha = 1.7 / h
                    n = 40
                    if X < n and Y < n:

                        not_matched = False  # matched means same object
                        centroids_list[idx][4] = 5
                        centroids_list[idx][2] = [xA, yA, xB, yB]
                        centroids_list[idx][6].append((np.sqrt(X ** 2 + Y ** 2) * alpha)*5)

                        if centroids_list[idx][5] == "unlocked":

                            if centroids_list[idx][0] == count - 1:
                                centroids_list[idx][3] += 1
                                # Increment lock-count

                            else:
                                centroids_list[idx][3] = 0

                        if centroids_list[idx][3] == 3:
                            centroids_list[idx][5] = "locked"
                            centroids_list[idx][3] = 0
                        if centroids_list[idx][6][-1] != 0.0:
                            cv2.rectangle(image, (xA, yA), (xB, yB), centroid_data[1], 2)
                            text = f"{str(round(centroids_list[idx][6][-1],2))}"
                            cv2.putText(image, text,
                                        (xA, yA), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                        centroids_list[idx][0] = count
                        break

                # If rectangle does not match with previous rectangles that means it is a new face so make a new rectangle
                if not_matched:
                    color = make_new_color()

                    # append new rectangle in previous faces list
                    centroids_list.appendleft([count, color, (xA, yA, xB, yB), 1, 5, "unlocked", [0], face_count])
                    face_count += 1
                    prev_color = color
                    prev_coords = [xA, yA, xB, yB]

            # plot all remaining locked rectangles
            for idx, centroid_data in enumerate(centroids_list):
                if centroid_data[5] == "locked" and centroid_data[0] != count:
                    centroids_list[idx][4] -= 1
                    if centroids_list[idx][6][-1] != 0.0:
                        cv2.rectangle(image, (centroid_data[2][0], centroid_data[2][1]), (centroid_data[2][2], centroid_data[2][3]),
                                      centroid_data[1], 2)
                        cv2.putText(image, str(round(centroids_list[idx][6][-1],2)),
                                    (centroid_data[2][0], centroid_data[2][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,
                                    cv2.LINE_AA)

                    if centroids_list[idx][4] == 0:
                        centroids_list[idx][5] = "unlocked"
                        centroids_list[idx][4] = 5
                        centroids_list[idx][3] = 0

                    # if count - centroid_data[0] == 10:
                if sum(centroid_data[6]) / len(centroid_data[6]) != 0.0:
                    listofspeeds.append((centroid_data[7], centroid_data[6], centroid_data[1]))


            centroids_list = deque([face_data for face_data in list(centroids_list) if count - face_data[0] < 10])

            if input_name == "0" or y_n == 'n':
                cv2.imshow('video2', image)
            out.write(image)

            # Wait for Esc key to stop
            if cv2.waitKey(33) == 27:
                break

            count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    encountered = []
    speed = []
    colors = []
    # counts = []
    for i in range(1,len(listofspeeds)):
        j = len(listofspeeds) - i
        if (listofspeeds[j][0] not in encountered) and (len(listofspeeds[j][1])>3):
            encountered.append(listofspeeds[j][0])
            speed.append(listofspeeds[j][1])
            colors.append(listofspeeds[j][2])
            # counts.append(listofspeeds[j][3])
    return (encountered, speed, colors)

def functionCall(input_name,output_name,y_n,y_n2):
    if speed_detection2(input_name,output_name,y_n,y_n2)==1:
        encountered, speed, colors = speed_detection(input_name, output_name, y_n)
    else:
        return 0

    if y_n2 == 'y':
        pathname = os.path.split(output_name)[0]
        file_name = os.path.basename(output_name)
        index_of_dot = file_name.index('.')
        file_name_without_extension = file_name[:index_of_dot]
        # print(file_name_without_extension)
        pathname = pathname+'\\'+file_name_without_extension
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        print(pathname)
        for i in range(0, len(speed)):
            plt.figure()
            plt.plot(speed[i], label="speed of tracker "+str(encountered[i]), color = (colors[i][0]/255, colors[i][1]/255, colors[i][2]/255))
            plt.xlabel("Frames")
            plt.ylabel("Speed (m/s)")
            plt.legend()
            plt.savefig(pathname+'\\'+str(i)+'.png')
    return 1


if __name__=='__main__':
    functionCall('untitled2.m4v', 'temp.avi', 'n', 'y')
    # untitled2.m4v

