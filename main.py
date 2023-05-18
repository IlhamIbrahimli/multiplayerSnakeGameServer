import socket
import sys
import select
import pygame
playerCount = int(input("How many people are playing?"))
ip = input("What is your ip?")
SOCK = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SOCK.bind((ip,12345))
print("Starting server")
ClientList = []
data = []
for y in range(playerCount):
    data.append("")
print("Initilization Complete")
SOCK.listen()
pygame.init()
text = ""
screen = pygame.display.set_mode((408, 30*playerCount))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)

def update_message():
    for k in ClientList:
        k.sendall(str(data).encode())


for i in range(playerCount):
    print("Waiting for connection")
    connection, ADDRESS = SOCK.accept()
    ClientList.append(connection)
    print(ClientList)
for j in ClientList:
    j.sendall("1".encode())
while True:
    pygame.event.get()
    read_sockets, _, exception_sockets = select.select(ClientList, [], ClientList, 1)
    for notified_socket in exception_sockets:
        ClientList.remove(notified_socket)
    for notified_socket in read_sockets:
        message = notified_socket.recv(16)
        if message.decode() == "end":
            ClientList.remove(notified_socket)
            notified_socket.close()
        else:
            x = ClientList.index(notified_socket)
            data[x] = message.decode()

    data = sorted(s, key=lambda x: int(x[-1]))
    update_message()
    screen.fill((255,255,255))
    for l in data:

        text = l[:3] + " " + l[-3:] + "\n"
        t = font.render(text, True, (0,0,0),(255,255,255))
        screen.blit(t,(0,data.index(l)*30))
    
    
    
    pygame.display.update()
    clock.tick(60)



