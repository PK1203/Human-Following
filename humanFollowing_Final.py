import cv2
print(cv2.__version__)
import numpy as np

import socket
import cv2
import pickle
import struct

width=1279
height=720
class mpPose:
    import mediapipe as mp
    def __init__(self,still=False,upperBody=False,smoothData=True):
        self.myPose=self.mp.solutions.pose.Pose(still,upperBody,smoothData)
    def Marks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myPose.process(frameRGB)
        poseLandmarks=[]
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                poseLandmarks.append((int(lm.x*width),int(lm.y*height)))
        return poseLandmarks

def findDistances(poseData):
    bodySize=((poseData[12][0]-poseData[23][0])**2+(poseData[12][1]-poseData[23][1])**2)**(1./2.)
    return bodySize

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.43.47'  # paste your server ip address here
port = 8000
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q")


while len(data) < payload_size:
	packet = client_socket.recv(2*1024)  # 4K
	if not packet:
		break
	data += packet

packed_msg_size = data[:payload_size]
data = data[payload_size:]
msg_size = struct.unpack("Q", packed_msg_size)[0]

while len(data) < msg_size:
	data += client_socket.recv(2*1024)

frame_data = data[:msg_size]
data = data[msg_size:]
frame1 = pickle.loads(frame_data)
#cv2.imshow("RECEIVING VIDEO", frame1)

cam=frame1
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG')) 

findPose=mpPose()
while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    frame[250:470,639:641]=(0,0,255)
    frame[359:361,530:750]=(0,0,255)
    poseData=findPose.Marks(frame)
    if len(poseData)!=0:
        for pose in poseData:
            bodySize=findDistances(poseData)
            for ind in range(0,31):
                cv2.circle(frame,poseData[ind],5,(0,255,0),3)

            if poseData[12][0]>700 and poseData[23][0]>700 :
                print('Left')
            elif poseData[12][0]<550 and poseData[23][0]<550 :
                print('Right')
            else :
                if bodySize>500 :
                    print('Backward')
                elif bodySize<400 :
                    print('Forward')
                else :
                    print('Stop')
    else :
        print('Stop')
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()

	


   

