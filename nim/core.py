#!/usr/bin/python
# coding=utf-8

import random
import copy

NONE = 0
SELECTED = 1
REMOVED = 2
class core:
    def caculate(self, map):
        """ 根据当前的局面计算出移动的棋子的列表，返回移动列表
        """

        nimsum = self.nim_sum(map)
        print "map", map
        print "nim sum: %d" %(nimsum)

        if nimsum != 0: # 必胜
            print "nimsum: ", nimsum
            for y in range(len(map)):
                count = 0
                remove_element = []     #   存放可移除棋子的下标
                if NONE in map[y]:      #   此堆中有石子
                    print "NONE in map[%d]" %(y)
                    for x in range(len(map[y])):
                       if map[y][x] == NONE:
                            remove_element.append(x)    # 找出此堆中的石子
                            count += 1
                    if (count & (1 << (self.bit(nimsum) - 1))) > 0: # 此句是必胜算法的核心
                        print "y: %d; count: %d" %(y, count) 
                        print "bit(nimsum): %d" %(self.bit(nimsum))
                        remove_element.reverse()
                        remove_count = count - (count^nimsum)   # 得到移除的石子的个数，这里必须要括号，-的优先级比^的要高
                        print "count: %d" %(count)
                        print "count^nimsum: %d" %(count^nimsum)
                        print "count - count^nimsum: %d" %(count - count^nimsum)
                        print "remove_count: ", remove_count
                        print "remove_element: ", remove_element
                        return_list = []
                        for i in range(remove_count):
                            print "append: (%d, %d)" %(remove_element[i], y)
                            return_list.append((remove_element[i], y))
                        print "return_list:", return_list
                        return return_list
                    

        else:   # 必败则随机选取一个有棋子的堆，移除此堆中随机个数的棋子
            removable_list = []
            for y in range(len(map)):
                if NONE in map[y]:
                    removable_list.append(y)    # 存下标
            print "removable_list: ", removable_list
            print "len(removable_list): %d" %(len(removable_list))
            index = random.randint(0, len(removable_list)-1)
            print "index: %d" %(index)
            print "removable_list[index]: ", removable_list[index]
            print "map[removable_list[index]]: ", map[removable_list[index]]
    
            removable_element = []
            for x in range(len(map[removable_list[index]])):
                if map[removable_list[index]][x] == NONE:
                    removable_element.append(x) # 存下标
            print "removable_element: ", removable_element
            print "len(removable_element): %d" %(len(removable_element))
            count = random.randint(1, len(removable_element))
            print "count: ", count
            removable_element.reverse()     # 逆序

            print "removable_element: ", removable_element
            
            return_list = []
            for x in range(count):
                return_list.append((removable_element[x], removable_list[index]))
    
            print "random return_list:", return_list
            return return_list




    def nim_sum(self, map):
        nim_sum = 0
        for y in range(len(map)):
            count = 0
            for x in range(len(map[y])):
                if map[y][x] == NONE:
                    count += 1
            nim_sum = nim_sum^count
            print "count: %d; nim_sum: %d" %(count, nim_sum)
        return nim_sum

    def bit(self, a):
        """返回数的位数如11(3)返回2, 0 返回0, 1返回1
        """
        if a == 0:
            return 0
        else:
            return len(str(bin(a))) - 2     # 0b100
        
            
    def gameover(self, map):
        over = True
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == NONE:
                    over = False
        return over
