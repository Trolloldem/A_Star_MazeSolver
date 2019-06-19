import math
from sys import argv
from MazeGenerator import mazeGen
from NodeClass import Node


class A_StarResult:
    def __init__(self,path,image):
        self.path=path
        self.image=image

def euclideanDistance(point1,point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

def getPath(destination,image):
    count=0
    path=[]
    while(destination!=None):
        count=count+1
        image.putpixel(destination.getXY(),(255,0,0))
        path.append(destination.getXY())
        destination=destination.getParent()
    print("Costo del cammino:"+str(count))
    path.reverse()
    return path

def moveNotWall(point,image,direction): #utilizzata per spostare end e start non su un muro
    canStart = False
    while (not (canStart)):
        if (image.getpixel(point) == (0, 0, 0)):
            point = (point[0] + direction, point[1])
        else:
            canStart = True
    if(direction==-1):
        print(point)
    return point

def A_StarPathfind(image,start,endCoord,dim):
    actual=start
    image.putpixel(actual.getXY(), (255, 0, 0))
    openNodes = []
    openNodes.append(start)
    closedNodes = []
    neighbors = []
    actualCoord=actual.getXY()

    while len(openNodes)!=0:
        neighbors = []
        actual=openNodes[0]
        if(actual.getXY()==endCoord):
            result= A_StarResult(getPath(actual,image),image)
            return result

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
    result=A_StarResult([],image)
    return result


def main(dim):
    image=mazeGen(dim) #generazione labirinto
    startCoord = (0,0)
    startCoord = moveNotWall(startCoord,image,+1)
    start = Node(startCoord[0],startCoord[1],None,euclideanDistance((0,0),(dim-1,dim-1)),0)
    endCoord = (dim-1,dim-1)
    endCoord = moveNotWall(endCoord,image,-1)
    print(endCoord)
    result=A_StarPathfind(image,start,endCoord,dim)
    print(result.path)
    result.image.save("SolvedMaze_" + str(dim) + "x" + str(dim) + ".png", "PNG")

if __name__ == "__main__":
    script, dimension = argv
    main(int(dimension))







