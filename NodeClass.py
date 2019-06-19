class Node:
    def __init__(self,x,y,parent,hValue,gValue):
        self.x=x
        self.y=y
        self.parent=parent
        self.hValue=hValue
        self.gValue=gValue
        self.fValue=gValue+hValue

    def getXY(self):
        return (self.x,self.y)

    def getParent(self):
        return self.parent

    def getFValue(self):
        return self.fValue

    def updateGValue(self,newValue,newParent):
        self.gValue=newValue
        self.fValue=self.hValue+newValue
        self.parent=newParent

    def getGValue(self):
        return self.gValue

    def __str__(self):
        coord=str(self.getXY())
        coordParent=str(self.getParent().getXY())
        Fval=str(self.getFValue())
        return "Il nodo ha coordinate: "+coord+"\nLe coordinate del padre sono: "+coordParent+"\nIl suo valore di f(n)= "+Fval

    def __eq__(self, other):
        if isinstance(other,Node):
            if(self.x==other.x and self.y==other.y):
                return True
        else:
            return False
