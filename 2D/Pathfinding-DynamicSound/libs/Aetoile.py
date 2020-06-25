from math import sqrt

#lsClose.append(lsOpen.pop(pts))

class navMesh:
    def __init__(self, dictPts, dictConns):
        self.dictPts = dictPts
        self.dictConns = dictConns
		
    def Aetoile(self, start, stop):
        lsOpen = []
        lsClose = [start]
        selectedPts = start
        Xgoal, Ygoal = self.dictPts.get(stop)
        dictCoutStart = {}
        dictCoutStart[start] = 0
        findAway = False
        while not findAway:
            newPoints = self.dictConns.get(selectedPts)
            for pts in newPoints:
                nom, cout = pts
                try:
                    lsClose.index(nom)
                except ValueError:
                    lsOpen.append(nom)
                    cout += dictCoutStart.get(selectedPts) #on ajoute le cout de son antécédent
                    dictCoutStart[nom] = cout
            lsOpen = epuration(lsOpen)
            if len(lsOpen) == 0:
                break
            refValue = 4096 #un grand nombre pour être certain de trouver plus petit
            selectedPts = lsOpen[0]
            for pts in lsOpen:
                Xpts, Ypts = self.dictPts.get(pts)
                X, Y = abs(Xgoal - Xpts), abs(Ygoal - Ypts)
                heuristic = int(sqrt(X**2 + Y**2))
                cout = dictCoutStart.get(pts)
                value = cout + heuristic
                if value < refValue:
                    selectedPts = pts
                    refValue = value
            index = lsOpen.index(selectedPts)
            lsClose.append(lsOpen.pop(index))
            if selectedPts == stop:
                findAway = True
                
        if not findAway:
            return []
        else:
            lsClose = self.cleanWay(lsClose)
            return lsClose

    def cleanWay(self, lsPts):
        #y'a un truc à améliorer là
        #il faut que je recule
        '''while not fini:
            for i in range(len(lsPts)-1):
                fils = self.getFils(lsPts[i])
                try:
                    fils.index[lsPts[i+1]]
                except:'''
        cleanList = []
        lsPts.reverse()
        cleanList.append(lsPts.pop(0))
        while len(lsPts) != 0:
            if self.isFils(cleanList[-1], lsPts[0]):
                cleanList.append(lsPts.pop(0))
            else:
                lsPts.pop(0)
        return cleanList              
            
    def isFils(self, startNode, dadNode):
        fils = self.getFils(dadNode)
        try:
            fils.index(startNode)
            return True
        except ValueError:
            return False

    def getFils(self, noeud):
        lsConns = self.dictConns.get(noeud)
        lsFils = []
        for pts in lsConns:
            nom, cout = pts
            lsFils.append(nom)
        return lsFils

    def extendNav(self, dictPts, dictConns):
        for pts in dictPts.keys():
            self.dictPts[pts] = dictPts.get(pts)
        for conns in dictConns.keys():
            self.dictConns[conns] = dictConns.get(conns)

    def connect(self, ptStart, ptStop, cout):
        lsConns = self.dictConns.get(ptStart)
        conns = (ptStop, cout)
        for i in range(len(lsConns)):
            nom, cout = lsConns[i]
            if nom == ptStop:
                lsConns[i] = conns
                self.dictConns[ptStart] = lsConns
                return
        lsConns.append(conns)
        self.dictConns[ptStart] = lsConns

    def addPts(self, nmPts, pos):
        self.dictPts[nmPts] = pos
        self.dictConns[nmPts] = []

    def findNear(self, pos):
        Xpos, Ypos = pos
        refValue = 2048
        bestPts = None
        for pts in self.dictPts.keys():
            X, Y = self.dictPts.get(pts)
            value = abs(X - Xpos) + abs(Y - Ypos)
            if value < refValue:
                refValue = value
                bestPts = pts
        return bestPts
		
def epuration(liste):
    aryan = []
    for elem in liste:
        try:
            aryan.index(elem)
        except ValueError:
            aryan.append(elem)
    return aryan




