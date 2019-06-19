import math
from MazeGenerator import mazeGen
from NodeClass import Node


def euclideanDistance(point1,point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

def getPath(destination):
    count=0
    while(destination!=None):
        count=count+1
        image.putpixel(destination.getXY(),(255,0,0))
        destination=destination.getParent()
    print("Nodi contati:"+str(count))

dim=1000
image=mazeGen(dim) #generazione labirinto

canStart=False
startCoord=(0,0)
while(not(canStart)):
    if(image.getpixel(startCoord)==(0,0,0)):
        startCoord=(startCoord[0]+1,startCoord[1])
    else:
        canStart=True
start = Node(startCoord[0],startCoord[1],None,euclideanDistance((0,0),(dim-1,dim-1)),0)
endCoord = (dim-1,dim-1)
canStart=False
while(not(canStart)):
    if(image.getpixel(startCoord)==(0,0,0)):
        endCoord=(endCoord[0]-1,endCoord[1])
    else:
        canStart=True
actual=start
dist=euclideanDistance((0,0),endCoord) #calcolo distanza punti
image.putpixel(actual.getXY(), (255, 0, 0))
openNodes = []
openNodes.append(start)
closedNodes = []
neighbors = []
actualCoord=actual.getXY()
counter=0
while len(openNodes)!=0:
    neighbors = []
    actual=openNodes[0]
    if(actual.getXY()==endCoord):
        print("Cammino: "+str(actual.getFValue()))
        getPath(actual)
        break
    actualCoord = actual.getXY()
    closedNodes.append(actual)
    openNodes.remove(actual)
    image.putpixel(actual.getXY(),(0,255,0))
    #un vicino è valido se: interno all'immagine, non è un muro, non è già stato chiuso
    if(actualCoord[0]  - 1 >=  0 and image.getpixel((actualCoord[0] - 1, actualCoord[1]))!=(0,0,0) and image.getpixel((actualCoord[0] - 1, actualCoord[1]))!=(0,255,0)):
        neighbors.append(Node(actualCoord[0] - 1, actualCoord[1], actual, euclideanDistance(actualCoord, endCoord), actual.getGValue() + 1))
    if(actualCoord[0]  + 1 < dim and image.getpixel((actualCoord[0] + 1, actualCoord[1]))!=(0,0,0) and image.getpixel((actualCoord[0] + 1, actualCoord[1]))!=(0,255,0)):
        neighbors.append(Node(actualCoord[0] + 1, actualCoord[1], actual, euclideanDistance(actualCoord, endCoord), actual.getGValue() + 1))
    if(actualCoord[1]  - 1 >= 0 and image.getpixel((actualCoord[0], actualCoord[1] - 1))!=(0,0,0) and image.getpixel((actualCoord[0], actualCoord[1] - 1))!=(0,255,0)):
        neighbors.append(Node(actualCoord[0], actualCoord[1] - 1, actual, euclideanDistance(actualCoord, endCoord), actual.getGValue() + 1))
    if (actualCoord[1] + 1 < dim and image.getpixel((actualCoord[0], actualCoord[1] + 1))!=(0,0,0) and image.getpixel((actualCoord[0], actualCoord[1] + 1))!=(0,255,0)):
        neighbors.append(Node(actualCoord[0], actualCoord[1] + 1, actual, euclideanDistance(actualCoord, endCoord), actual.getGValue() + 1))
    for neighbor in neighbors:
        if (image.getpixel(neighbor.getXY()) == (0, 0, 255)): #il nodo è già in frontiera => controllo il suo costo attuale
            for node in openNodes:
                if(neighbor.getGValue()<node.getGValue()): #se il vicino è già in frontiera, ma con costo di cammino maggiore
                    openNodes.remove(node)
                    openNodes.append(neighbor)
        else:
            openNodes.append(neighbor)
            image.putpixel(neighbor.getXY(), (0, 0, 255))
    openNodes.sort(key=lambda x: x.getFValue(), reverse=False) #ordino frontiera in base ai costi f=g+h

print("Numero di nodi espanso: "+str(len(closedNodes)))
image.save("SolvedMaze_" + str(dim) + "x" + str(dim) + ".png", "PNG")






