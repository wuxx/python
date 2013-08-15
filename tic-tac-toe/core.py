
NONE = 0
AI = 1
PLAYER = -1

PLAYER_MIN = -1000
AI_MAX = 1000

class core:
    def __init__(self):
        self.step = 0

    def caculate(self, map):
        (x, y, v) = self.best(map)
        map[x][y] = AI
        self.step += 1
        return (x, y)

    def best(self, map):    # return the best step for AI
        bestx = -1
        besty = -1
        bestv = 0
        for x in range(len(map)):
            for y in range(len(map[x])):
                if map[x][y] == NONE:
                    map[x][y] = AI
                    self.step += 1
                    if self.iswin(map, x, y) == True:
                        self.step -= 1
                        map[x][y] = NONE
                        return [x, y, AI_MAX]
                    elif self.isend(map) == True:
                        map[x][y] = NONE
                        self.step -= 1
                        return [x, y, 0]
                    else:
                        rt = self.worst(map)
                        #print "(%d, %d)" %(x, y)
                        #print "wosrt is (%d, %d, %d)" %(rt[0], rt[1], rt[2])
                        map[x][y] = NONE
                        self.step -= 1
                        if bestx == -1 or rt[2] >= bestv:
                            bestx = x
                            besty = y
                            bestv = rt[2]
        #print "best: (%d, %d, %d)" %(bestx, besty, bestv)
        return [bestx, besty, bestv]
                

    def isend(self, map):
        for x in map:
            if NONE in x:
                return False
        return True

    def iswin(self, map, x, y):
        if abs(map[x][0] + map[x][1] + map[x][2]) == 3:
            return True
        elif abs(map[0][y] + map[1][y] + map[2][y]) == 3:
            return True
        elif abs(map[0][0] + map[1][1] + map[2][2]) == 3:
            return True
        elif abs(map[0][2] + map[1][1] + map[2][0]) == 3:
            return True
        else:
            return False

    def worst(self, map):   # return the best step of player
        bestx = -1
        besty = -1
        bestv = 0
        for x in range(len(map)):
            for y in range(len(map[x])):
                if map[x][y] == NONE:
                    map[x][y] = PLAYER
                    self.step += 1
                    if self.iswin(map, x, y) == True:
                        self.step -= 1
                        map[x][y] = NONE
                        #print "this place player win (%d, %d)" %(x, y)
                        return [x, y, PLAYER_MIN]
                    elif self.isend(map) == True:
                        map[x][y] = NONE
                        self.step -= 1
                        return [x, y, 0]
                    else:
                        rt = self.best(map)

                        map[x][y] = NONE
                        self.step -= 1
                        if bestx == -1 or rt[2] <= bestv:
                            bestx = x
                            besty = y
                            bestv = rt[2]
        return [bestx, besty, bestv]
