import socket
import cv2
import pickle
import struct
import imutils
import time
import threading

HEADER=64
FORMAT='utf-8'
def buffer_clear():
	global frame
	cap=cv2.VideoCapture(0)
	while True:
		ret,fr=cap.read()
		if ret:
		    frame=fr
                        
def handle_client(conn,addr):
	while(True):
		print (f" [NEW CONNECTION]{addr} connected.")
		connected=True
		while connected:
			msg_length=conn.recv(HEADER).decode(FORMAT)
			if msg_length:
				msg=conn.recv(1024).decode(FORMAT)
			if (msg=="DISCONNECT"):
				connected=False
			print(f"[{addr}]{msg}")
	conn.close()
	
def video(client_socket,addr):
	global frame
	while True:

		print('GOT CONNECTION FROM:', addr)
		if client_socket:
			while(1):
				frame = imutils.resize(frame, width=320)
				a = pickle.dumps(frame)
				message = struct.pack("Q", len(a))+a
				client_socket.sendall(message)
				cv2.imshow('TRANSMITTING VIDEO', frame)
				key = cv2.waitKey(1) & 0xFF
				if key == ord('q'):
					client_socket.close()

def start():
	# Socket Create
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 8000
	socket_address = ("", port)
	frame=None

	# Socket Bind
	server_socket.bind(socket_address)
	SERVER=socket.gethostbyname(socket.gethostname())
	print(SERVER)



	server_socket.listen(5)
	print("LISTENING AT:", socket_address)
	
	thread3=threading.Thread(target=buffer_clear)
	
	thread3.start()
	time.sleep(5)
	print("ggs")
	client_socket,addr=server_socket.accept()
	thread1=threading.Thread(target=video,args=(client_socket,addr))
	thread2=threading.Thread(target=handle_client,args=(client_socket,addr))
	
	
	thread1.start()
	thread2.start()    

start()
