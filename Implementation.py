import math
from sys import argv
from MazeGenerator import mazeGen
from NodeClass import Node
from datetime import datetime
from PIL import Image
import argparse


class A_StarResult:
    def __init__(self,path,image):
        self.path=path
        self.image=image

def euclideanDistance(point1,point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))
def  ManhattanDistance(point1,point2):
    return abs(point1[0] - point2[0])+abs(point1[1] - point2[1])
def costantDistanceZero(point1,point2):
    return 0

def getPath(destination,image):
    count=0
    path=[]
    while(destination!=None):
        count=count+1
        image.putpixel(destination.getXY(),(255,0,0))
        path.append(destination.getXY())
        destination=destination.getParent()
    print("Costo del cammino:"+str(count-1))
    path.reverse()
    return path

def moveNotWall(point,image,direction): #utilizzata per spostare end e start non su un muro
    canStart = False
    while (not (canStart)):
        if (image.getpixel(point) == (0, 0, 0)):
            point = (point[0] + direction, point[1])
        else:
            canStart = True
    return point

def A_StarPathfind(image,start,endCoord,dim,hFun):
    image.putpixel(start.getXY(), (255, 0, 0))
    openNodes = []
    openNodes.append(start)
    closedNodes = []
    startTime = datetime.now()
    while len(openNodes)!=0:
        neighbors = []
        actual=openNodes[0]
        if(actual.getXY()==endCoord):
            print(len(openNodes))
            print("GVALUE DEL NODO FINALE: "+str(actual.getGValue()))
            result= A_StarResult(getPath(actual,image),image)
            endTime = datetime.now()
            print("Tempo utilizzato:")
            print(endTime-startTime)
            return result

        actualCoord = actual.getXY()
        closedNodes.append(actual)
        openNodes.remove(actual)
        image.putpixel(actual.getXY(),(0,255,0))
        #un vicino è valido se: interno all'immagine, non è un muro, non è già stato chiuso
        if(actualCoord[0]  - 1 >=  0 and image.getpixel((actualCoord[0] - 1, actualCoord[1]))!=(0,0,0) and image.getpixel((actualCoord[0] - 1, actualCoord[1]))!=(0,255,0)):
            neighbors.append(Node(actualCoord[0] - 1, actualCoord[1], actual, hFun((actualCoord[0] - 1, actualCoord[1]), endCoord), actual.getGValue() + 1))
        if(actualCoord[0]  + 1 < dim and image.getpixel((actualCoord[0] + 1, actualCoord[1]))!=(0,0,0) and image.getpixel((actualCoord[0] + 1, actualCoord[1]))!=(0,255,0)):
            neighbors.append(Node(actualCoord[0] + 1, actualCoord[1], actual, hFun((actualCoord[0] + 1, actualCoord[1]), endCoord), actual.getGValue() + 1))
        if(actualCoord[1]  - 1 >= 0 and image.getpixel((actualCoord[0], actualCoord[1] - 1))!=(0,0,0) and image.getpixel((actualCoord[0], actualCoord[1] - 1))!=(0,255,0)):
            neighbors.append(Node(actualCoord[0], actualCoord[1] - 1, actual, hFun((actualCoord[0], actualCoord[1] - 1), endCoord), actual.getGValue() + 1))
        if (actualCoord[1] + 1 < dim and image.getpixel((actualCoord[0], actualCoord[1] + 1))!=(0,0,0) and image.getpixel((actualCoord[0], actualCoord[1] + 1))!=(0,255,0)):
            neighbors.append(Node(actualCoord[0], actualCoord[1] + 1, actual, hFun((actualCoord[0], actualCoord[1] + 1), endCoord), actual.getGValue() + 1))

        #DIREZIONI DI TEST OBLIQUE
        if (actualCoord[0] - 1 >= 0 and actualCoord[1] -1 >=0 and image.getpixel((actualCoord[0] - 1, actualCoord[1]-1)) != (0, 0, 0) and image.getpixel((actualCoord[0] - 1, actualCoord[1]-1)) != (0, 255, 0)):
            if(not(image.getpixel((actualCoord[0] - 1, actualCoord[1]))==(0,0,0) and image.getpixel((actualCoord[0] , actualCoord[1]-1))==(0,0,0))):
                neighbors.append(Node(actualCoord[0] - 1, actualCoord[1]-1, actual, hFun((actualCoord[0] -1, actualCoord[1]-1), endCoord),actual.getGValue() + 1))
        if (actualCoord[0] + 1 < dim and actualCoord[1] +1 <dim and image.getpixel((actualCoord[0] + 1, actualCoord[1]+1)) != (0, 0, 0) and image.getpixel((actualCoord[0] + 1, actualCoord[1]+1)) != (0, 255, 0)):
            if (not(image.getpixel((actualCoord[0] + 1, actualCoord[1])) == (0, 0, 0) and image.getpixel((actualCoord[0],actualCoord[1] + 1)) == (0, 0, 0))):
                neighbors.append(Node(actualCoord[0] + 1, actualCoord[1]+ 1, actual, hFun((actualCoord[0] + 1, actualCoord[1]+1), endCoord),actual.getGValue() + 1))
        if (actualCoord[0] - 1 >= 0 and actualCoord[1] +1< dim and image.getpixel((actualCoord[0] - 1, actualCoord[1]+1)) != (0, 0, 0) and image.getpixel((actualCoord[0] - 1, actualCoord[1]+1)) != (0, 255, 0)):
            if (not(image.getpixel((actualCoord[0] - 1, actualCoord[1])) == (0, 0, 0) and image.getpixel((actualCoord[0],actualCoord[1] + 1)) == (0, 0, 0))):
                neighbors.append(Node(actualCoord[0] - 1, actualCoord[1]+1, actual, hFun((actualCoord[0] - 1, actualCoord[1]+1), endCoord),actual.getGValue() + 1))
        if (actualCoord[0] + 1 <dim and actualCoord[1] -1>=0 and image.getpixel((actualCoord[0] + 1, actualCoord[1]-1)) != (0, 0, 0) and image.getpixel((actualCoord[0] + 1, actualCoord[1]-1)) != (0, 255, 0)):
            if (not(image.getpixel((actualCoord[0] + 1, actualCoord[1])) == (0, 0, 0) and image.getpixel((actualCoord[0],actualCoord[1] - 1)) == (0, 0, 0))):
                neighbors.append(Node(actualCoord[0] + 1, actualCoord[1]-1, actual, hFun((actualCoord[0] + 1, actualCoord[1]-1), endCoord),actual.getGValue() + 1))

        #FINE DIREZIONI DI TEST
        for neighbor in neighbors:
            if (image.getpixel(neighbor.getXY()) == (0, 0, 255)): #il nodo è già in frontiera => controllo il suo costo attuale
                for node in openNodes:
                    if(neighbor.getGValue()<node.getGValue() and neighbor.getXY()==node.getXY()): #se il vicino è già in frontiera, ma con costo di cammino maggiore
                        openNodes.remove(node)
                        openNodes.append(neighbor)
            else:
                openNodes.append(neighbor)
                image.putpixel(neighbor.getXY(), (0, 0, 255))
        openNodes.sort(key=lambda x: x.getFValue(), reverse=False) #ordino frontiera in base ai costi f=g+h
    result=A_StarResult([],image)
    return result







def main(dim,type):
    if(type=="random"):
        image=mazeGen(dim) #generazione labirinto
    if(type=="critica"):
        image=Image.open("critica.png")
        dim=250
    if (type == "empty"):
        image = Image.open("empty.png")
        dim=200
    if (type == "example"):
        image = Image.open("creata.png")
        dim=200

    imageEuClid=image.copy()
    imageDij=image.copy()
    startCoord = (0,0)
    startCoord = moveNotWall(startCoord,image,+1)
    start = Node(startCoord[0],startCoord[1],None,euclideanDistance((0,0),(dim-1,dim-1)),0)
    endCoord = (dim-1,dim-1)
    endCoord = moveNotWall(endCoord,image,-1)
    resultEuclid=A_StarPathfind(imageEuClid,start,endCoord,dim,euclideanDistance)

    #print("Path con h=euclidea")
    #print(resultEuclid.path)

    resultMan=A_StarPathfind(image,start,endCoord,dim,ManhattanDistance)
    '''
    print("Path Manhattan:")
    print(resultMan.path)'''
    resultDij = A_StarPathfind(imageDij, start, endCoord, dim,costantDistanceZero)
    resultDij.image.save("SolvedMaze_" + str(dim) + "x" + str(dim) + "_Dij.png", "PNG")
    resultEuclid.image.save("SolvedMaze_" + str(dim) + "x" + str(dim) + "_Euclidean.png", "PNG")
    resultMan.image.save("SolvedMaze_" + str(dim) + "x" + str(dim) + "_Manhattan.png", "PNG")

if __name__ == "__main__":
    argumentList = argv[1:]
    parser = argparse.ArgumentParser(description='Genera e trova la soluzione del labirinto generato')
    parser.add_argument('--dim',dest="dim", type=int,help='dimensione immagine')
    parser.add_argument('type', metavar='tipo', type=str,
                        help='Tipo di run: "random" per labirinto random, "empty" per immagine bianca, "critica" per immagine problematica, "example" per un\'immagine generica')
    args = parser.parse_args()
    if args.type=="random" and args.dim!=None:
        print("Genero labirinto di dimensione:"+str(args.dim))
    if args.dim==None:
        dim=0
    main(args.dim,args.type)







