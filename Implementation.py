import math
from sys import argv
from sys import exit
from MazeGenerator import mazeGen
from NodeClass import Node
import datetime
from _datetime import datetime, timedelta
from PIL import Image
import argparse


class A_StarResult:
    def __init__(self,path,image,visitedNodes,timeUsed,pathCost):
        self.path=path
        self.image=image
        self.visitedNodes=visitedNodes
        self.timeUsed=timeUsed
        self.pathCost=pathCost

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

def A_StarPathfind(image,start,endCoord,dim,hFun,run):
    image.putpixel(start.getXY(), (255, 0, 0))
    openNodes = []
    openNodes.append(start)
    closedNodes = []
    startTime = datetime.now()
    while len(openNodes)!=0:
        neighbors = []
        actual=openNodes[0]
        if(actual.getXY()==endCoord):
            endTime = datetime.now()
            if run==1:
                print("Tempo utilizzato:")
                print(endTime-startTime)
                print("Nodi in frontiera: " + str(len(openNodes)))
                print("Nodi esplorati: " + str(len(closedNodes)+1))
                print("Costo del cammino: " + str(actual.getGValue()))
            result = A_StarResult(getPath(actual, image), image,len(closedNodes)+1,endTime-startTime,actual.getGValue())
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
                neighbors.append(Node(actualCoord[0] - 1, actualCoord[1]-1, actual, hFun((actualCoord[0] -1, actualCoord[1]-1), endCoord),actual.getGValue() + euclideanDistance(actualCoord,(actualCoord[0] - 1, actualCoord[1]-1))))
        if (actualCoord[0] + 1 < dim and actualCoord[1] +1 <dim and image.getpixel((actualCoord[0] + 1, actualCoord[1]+1)) != (0, 0, 0) and image.getpixel((actualCoord[0] + 1, actualCoord[1]+1)) != (0, 255, 0)):
            if (not(image.getpixel((actualCoord[0] + 1, actualCoord[1])) == (0, 0, 0) and image.getpixel((actualCoord[0],actualCoord[1] + 1)) == (0, 0, 0))):
                neighbors.append(Node(actualCoord[0] + 1, actualCoord[1]+ 1, actual, hFun((actualCoord[0] + 1, actualCoord[1]+1), endCoord),actual.getGValue() + euclideanDistance(actualCoord,(actualCoord[0] + 1, actualCoord[1]+1))))
        if (actualCoord[0] - 1 >= 0 and actualCoord[1] +1< dim and image.getpixel((actualCoord[0] - 1, actualCoord[1]+1)) != (0, 0, 0) and image.getpixel((actualCoord[0] - 1, actualCoord[1]+1)) != (0, 255, 0)):
            if (not(image.getpixel((actualCoord[0] - 1, actualCoord[1])) == (0, 0, 0) and image.getpixel((actualCoord[0],actualCoord[1] + 1)) == (0, 0, 0))):
                neighbors.append(Node(actualCoord[0] - 1, actualCoord[1]+1, actual, hFun((actualCoord[0] - 1, actualCoord[1]+1), endCoord),actual.getGValue() + euclideanDistance(actualCoord,(actualCoord[0] - 1, actualCoord[1]+1))))
        if (actualCoord[0] + 1 <dim and actualCoord[1] -1>=0 and image.getpixel((actualCoord[0] + 1, actualCoord[1]-1)) != (0, 0, 0) and image.getpixel((actualCoord[0] + 1, actualCoord[1]-1)) != (0, 255, 0)):
            if (not(image.getpixel((actualCoord[0] + 1, actualCoord[1])) == (0, 0, 0) and image.getpixel((actualCoord[0],actualCoord[1] - 1)) == (0, 0, 0))):
                neighbors.append(Node(actualCoord[0] + 1, actualCoord[1]-1, actual, hFun((actualCoord[0] + 1, actualCoord[1]-1), endCoord),actual.getGValue() + euclideanDistance(actualCoord,(actualCoord[0] + 1, actualCoord[1]-1))))

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







def main(dim,type,run,show=False):

    euclideanTimes=[]
    euclideanNodes=[]
    euclideanLenPath=[]
    ManhattanTimes = []
    ManhattanNodes = []
    ManhattanLenPath = []
    DijTimes = []
    DijNodes = []
    DijLenPath = []

    for i in range(0,run):
        if(type=="random"):
            specificName="random"
            image=mazeGen(dim) #generazione labirinto
        if(type=="critica"):
            specificName = "critica"
            image=Image.open("critica.png")
            dim=250
        if (type == "empty"):
            specificName = "empty"
            image = Image.open("empty.png")
            dim=200
        if (type == "example"):
            specificName = "example"
            image = Image.open("creata.png")
            dim=200
        if (type == "bench"):
            specificName = "example"
            image = Image.open("bench.png")
            dim=820
            startCoord = (210, 10)
            endCoord = (800,805)


        imageEuClid=image.copy()
        imageDij=image.copy()

        if(type!="bench"):
            startCoord = (0,0)
            endCoord = (dim-1,dim-1)
        endCoord = moveNotWall(endCoord,image,-1)
        startCoord = moveNotWall(startCoord, image, +1)
        start = Node(startCoord[0], startCoord[1], None, euclideanDistance((0, 0), (dim - 1, dim - 1)), 0)

        resultEuclid=A_StarPathfind(imageEuClid,start,endCoord,dim,euclideanDistance,run)
        euclideanTimes.append(resultEuclid.timeUsed)
        euclideanNodes.append(resultEuclid.visitedNodes)
        euclideanLenPath.append(resultEuclid.pathCost)

        resultMan=A_StarPathfind(image,start,endCoord,dim,ManhattanDistance,run)
        ManhattanTimes.append(resultMan.timeUsed)
        ManhattanNodes.append(resultMan.visitedNodes)
        ManhattanLenPath.append(resultMan.pathCost)

        resultDij = A_StarPathfind(imageDij, start, endCoord, dim,costantDistanceZero,run)
        DijTimes.append(resultDij.timeUsed)
        DijNodes.append(resultDij.visitedNodes)
        DijLenPath.append(resultDij.pathCost)

        resultDij.image.save("SolvedMaze_"+specificName+"_"+ str(dim) + "x" + str(dim) + "_Dij.png", "PNG")
        resultEuclid.image.save("SolvedMaze_" +specificName+"_"+ str(dim) + "x" + str(dim) + "_Euclidean.png", "PNG")
        resultMan.image.save("SolvedMaze_" + specificName+"_"+str(dim) + "x" + str(dim) + "_Manhattan.png", "PNG")

        if show:
            resultDij.image.show()
            resultMan.image.show()
            resultEuclid.image.show()

    if run!=1:
        print("Misurazioni euristica euclidea:")
        print("Media dei tempi:"+str(sum(euclideanTimes, timedelta(0)) / len(euclideanTimes)))
        print("Media dei nodi esplorati:"+str(sum(euclideanNodes,0)/len(euclideanNodes)))
        print("Misurazioni euristica Manhattan:")
        print("Media dei tempi:" + str(sum(ManhattanTimes, timedelta(0)) / len(ManhattanTimes)))
        print("Media dei nodi esplorati:" + str(sum(ManhattanNodes, 0) / len(ManhattanNodes)))
        print("Misurazioni Dijkstra:")
        print("Media dei tempi:" + str(sum(DijTimes, timedelta(0)) / len(DijTimes)))
        print("Media dei nodi esplorati:" + str(sum(DijNodes, 0) / len(DijNodes)))
        alwaysOptimal=True
        for i in range(0,len(euclideanLenPath)):
            if not(euclideanLenPath[i]==DijLenPath[i] and ManhattanLenPath[i]==DijLenPath[i]):
                alwaysOptimal=False
        if alwaysOptimal:
            print("Ottimo sempre raggiunto")
        else:
            print("Non viene sempre raggiunto l'ottimo")

if __name__ == "__main__":
    argumentList = argv[1:]
    parser = argparse.ArgumentParser(description='Genera e trova la soluzione del labirinto generato')
    parser.add_argument('--dim','-d',dest="dim", type=int,help='dimensione immagine')
    parser.add_argument('type', metavar='tipo', type=str,
                        help='Tipo di run: "random" per labirinto random, "empty" per immagine bianca, "critica" per immagine problematica, "example" per un\'immagine generica, "bench" per un\'immagine di benchmark')
    parser.add_argument('--show','-s',help='Mostra le immagini a fine computazione',action="store_true")
    parser.add_argument('--run', '-r', type=int,help='Numero di run consecutive', dest="run")
    args = parser.parse_args()
    if args.type=="random" and args.dim!=None:
        print("Genero labirinto di dimensione:"+str(args.dim))
    if  args.type=="random" and args.dim==None:
        print("Dimensione necessaria per labirinti random: -d <dimensione>")
        exit()
    if args.dim==None:
        args.dim=0
    if args.run==None:
        args.run=1
    if args.show:
        print("L'immagine verrà visualizzata")
    main(args.dim,args.type,args.run,args.show)







