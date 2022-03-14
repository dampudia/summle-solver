# summel-solver.py

import sys
import argparse
import copy
import itertools

class InvalidOPerationException(Exception):
    pass

class Node:
    def depth(self) -> int:
        pass
    def holes(self) -> int:
        pass
    def printNode(self) -> str:
        pass
    def isFinal(self) -> bool:
        """Return true when a number and true when an operation whose children nodes are final"""
        pass
    def solve(self) -> int:
        """Return the result"""
        pass
    
class Num(Node):
    def __init__(self, value):
        self.value = value
    def holes(self)->int:
        return 0
    def depth(self)->int:
        return 1    
    def printNode(self)->str:
        return str(self.value)
    def isFinal(self)->bool:
        return True
    def solve(self)->int:
        return self.value
    
class Op(Node):
    def __init__(self):
        self.l = None
        self.r = None
    def depth(self)->int:
        dl = 0
        dr = 0
        if self.l != None:
            dl = self.l.depth()
        if self.r != None:
            dr = self.r.depth()
        return min(dl, dr)    
    def holes(self)->int:
        i = 0
        if self.l == None:
            i+=1
        else:
            i+= self.l.holes()
        if self.r == None:
            i+=1
        else:
            i+= self.r.holes()
        return i
    def isFinal(self)->bool:
        if (self.l == None) or (self.r == None):
            return False
        return self.l.isFinal() and self.r.isFinal()   
    def grow(self, node):
        if self.isFinal():
            raise Exception("cannot grow final tree")
        if self.l == None:
            self.l = node
            return
        if self.r == None:
            self.r = node
            return
        if self.l.isFinal() and (not self.r.isFinal()):
            self.r.grow(node)
            return
        if self.r.isFinal() and (not self.l.isFinal()):
            self.l.grow(node)
            return
        if self.l.depth()>self.r.depth():
            self.r.grow(node)
            return
        self.l.grow(node)
                

class Sum(Op):
    def printNode(self)->str:
        return "(" + str(self.l.printNode()) + "+" + str(self.r.printNode()) + ")"
    def solve(self)->int:
        if (self.l == None) or (self.r == None):
            raise Exception
        return self.l.solve() + self.r.solve()
    
class Substract(Op):
    def printNode(self)->str:
        return "(" + str(self.l.printNode()) + "-" + str(self.r.printNode()) + ")"
    def solve(self)->int:
        if self.l.solve() - self.r.solve() < 0 :
            raise InvalidOPerationException("result is negative")
        return self.l.solve() - self.r.solve()
    
class Multiply(Op):
    def printNode(self)->str:
        return "(" + str(self.l.printNode()) + "*" + str(self.r.printNode()) + ")"
    def solve(self)->int:
        return self.l.solve() * self.r.solve()
    
class Divide(Op):
    def printNode(self)->str:
        return "(" + str(self.l.printNode()) + "/" + str(self.r.printNode()) + ")"
    def solve(self)->int:
        if self.r.solve() == 0 :
            raise InvalidOPerationException("cannot divide by zero")
        if self.l.solve() % self.r.solve() != 0 :
            raise InvalidOPerationException("result is not an integer")
        return self.l.solve() / self.r.solve()

class Tree:
    def __init__(self, total, node, intList):
        self.node = node
        self.total = total
        self.intList = intList
    def fillAndSolve(self) -> Node:
        try:
            if self.node.isFinal():
                if self.node.solve() == self.total:
                    return self.node
            perms = itertools.permutations(self.intList, self.node.holes())
            for p in perms:
                testNode = copy.deepcopy(self.node)
                for i in p:
                    testNode.grow(Num(i))
                if testNode.solve() == self.total:
                    return testNode
        except InvalidOPerationException as e:
            pass
        return None    

    def spawn(self):
        result = []
        if self.node.isFinal():
            return result
        if self.node.holes() == len(self.intList):
            return result
        for i in range(0, len(self.intList)-1):
            newNode = copy.deepcopy(self.node)
            newList = copy.deepcopy(self.intList)
            newNode.grow(Num(self.intList[i]))
            newList.pop(i)
            result.append(Tree(self.total, newNode, newList))
        newNode = copy.deepcopy(self.node)   
        newNode.grow(Sum())        
        result.append(Tree(self.total, newNode, self.intList))
        newNode = copy.deepcopy(self.node)   
        newNode.grow(Substract())        
        result.append(Tree(self.total, newNode, self.intList))
        newNode = copy.deepcopy(self.node)   
        newNode.grow(Multiply())        
        result.append(Tree(self.total, newNode, self.intList))
        newNode = copy.deepcopy(self.node)   
        newNode.grow(Divide())        
        result.append(Tree(self.total, newNode, self.intList))
        return result

    

parser = argparse.ArgumentParser("summel-solver")
parser.add_argument("total", help="The number to reach.", type=int)
parser.add_argument("numbers", help="The number to operate with, separated by commas.")
args = parser.parse_args()

print(args.total)
list = args.numbers.split(',')
intList = []
for i in list:
    try:
        intList.append(int(i))
    except ValueError:
        sys.exit("The list can only contain integers") 
   
print(intList)   

trees = [Tree(args.total, Sum(), intList), 
         Tree(args.total, Substract(), intList), 
         Tree(args.total, Multiply(), intList), 
         Tree(args.total, Divide(), intList)]

while len(trees) > 0: 
    print("tree count = " + str(len(trees)))
    newTrees = []
    for t in trees:
        result = t.fillAndSolve()
        if result != None:
            print("solution:" + result.printNode())
            quit()
        newTrees = newTrees + t.spawn()
    trees = newTrees    
    

sys.exit("solution  not found")    
    
    
    
    
    
    
    
    
    