import csv
import time
import sys
from collections import deque
from collections import ChainMap

class Graph:
    def __init__(self):
        self.vertexlist = {}
        self.lenVertex = 0

    def addVertex(self, key):
        if key not in self.vertexlist:
            self.lenVertex = self.lenVertex+1
            newVertex = Vertex(key)
            self.vertexlist[key] = newVertex
            return newVertex

    def getVertex(self, findVertex):
        if findVertex in self.vertexlist:
            return self.vertexlist[findVertex]
        else:
            return None

    def addEdge(self, fromVertex,toVertex):
        if fromVertex not in self.vertexlist:
            nv = self.addVertex(fromVertex)
        if toVertex not in self.vertexlist:
            nv = self.addVertex(toVertex)
        self.vertexlist[fromVertex].addNeighbor(self.vertexlist[toVertex])
        self.vertexlist[toVertex].addNeighbor(self.vertexlist[fromVertex])

    def getId(self):
        return self.id

    def __iter__(self):
        return iter(self.vertexlist.values())

    def displayVertexItems(self,name):
        listvertex = list(self.getVertex(name).getConnections())
        return listvertex

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr):
        self.connectedTo[nbr.id] = nbr

    # def __str__(self):
    #     return str(self.id) + ' connectedTo: ' + str([x for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

def process(graph_input,payment_input,output1,output2,output3):
    g = Graph()
    count = 0
    if len(sys.argv) == 0:
        print('Specify input and output arguments')
        exit()
    else:
        readdata = set()
        with open(graph_input,'r',encoding="utf8") as f:
         for line in f:
             data = line.split(',')
             if data.__len__() > 4:
                 if data[1].__len__() < 10:
                    if (data[1], data[2]) not in readdata:
                        readdata.add((data[1], data[2]))

                        if count == 0:
                            count += 1
                            continue

                        count += 1
                        data[2] = data[2].strip()
                        g.addVertex(data[1])
                        g.addEdge(data[1],data[2])
                        if count == 10:
                            time.sleep(2)
        f.close()

        print("Graph Created")
        print(count)

        feature1 = open(output1, 'w')
        feature2 = open(output2, 'w')
        feature3 = open(output3, 'w')
        count =0
        with open(payment_input,'r', encoding="utf8") as input:
            for line in input:
                data = line.split(',')
                if data.__len__() > 4:
                #     if data[1].__len__() < 10:
                        # if (data[1], data[2]) not in readdata:
                        #     readdata.add((data[1], data[2]))
                            if count == 0:
                                count += 1
                                continue
                            count += 1
                            start_vertex = g.vertexlist.get(data[1])
                            receiver= data[2].strip()
                            if start_vertex == None:
                              feature1.write("unverified" + "\n")
                              feature2.write("unverified" + "\n")
                              feature3.write("unverified" + "\n")
                            else:
                              edge_recv = start_vertex.connectedTo.get(receiver)
                              # Feature 1
                              if edge_recv != None:
                                  feature1.write("trusted" + "\n")
                                  feature2.write("trusted" + "\n")
                                  feature3.write("trusted" + "\n")
                              else:
                                  feature1.write("unverified" + "\n")
                                  # Feature 2
                                  # Consider source and their corresponding neighbours in a Breadth First Search Graph.
                                  # So each node from Level 0 points to a dictinoary with keys as its neighbours.
                                  # Using O(1) key search we find 2nd degree friend

                                  new_rcv, graph, visited, end, chain, depth = find_second_order(g, data[1], receiver)
                                  # new_rcv = breadthFirst(g, data[1], receiver)

                                  if new_rcv != None:
                                      feature2.write("trusted" + "\n")
                                      # feature3.write("trusted" + "\n")
                                  else:
                                      feature2.write("unverified" + "\n")
                                      new_rcv, graph, visited, end, chain, depth = findnextorder(graph, visited, end, chain, depth)

                                      if new_rcv != None:
                                          feature3.write("trusted" + "\n")
                                      else:
                                          new_rcv, graph, visited, end, chain, depth = findnextorder(graph, visited, end, chain, depth)

                                          if new_rcv != None:
                                              feature3.write("trusted" + "\n")
                                          else:
                                              feature3.write("unverified" + "\n")
                            #print(count)
                            if count == 10:
                                time.sleep(2)



def find_second_order(graph, start, end, visited=[], depth=0):
    visited = set()
    if start == end:
        return None
    if not graph.vertexlist.get(start):
        return None
    found_vertex = None
    list_dict = graph.vertexlist.get(start)
    visited.add(start)
    chain = ChainMap()
    depth += 1  # 1
    for neigh_vertex in list_dict.connectedTo:
        if neigh_vertex not in visited:
            visited.add(neigh_vertex)
            temp_vertex = graph.vertexlist.get(neigh_vertex)
            newpath = temp_vertex.connectedTo.get(end)
            if newpath:
                found_vertex = newpath
                break
            else:
                chain = chain.new_child(temp_vertex.connectedTo)

    depth += 1  # 2
    return (found_vertex, graph, visited, end, chain, depth)


def findnextorder(graph, visited, end, chain, depth):
    newchain = ChainMap()
    found_vertex = None
    for neigh_vertex in dict(chain):
        if neigh_vertex not in visited:
            visited.add(neigh_vertex)
            temp_vertex = graph.vertexlist.get(neigh_vertex)
            newpath = temp_vertex.connectedTo.get(end)
            if newpath:
                found_vertex = newpath
                break
            else:
                newchain = newchain.new_child(temp_vertex.connectedTo)

    depth += 1
    return (found_vertex, graph, visited, end, chain, depth)

def breadthFirst(graph,start, end):
   visited= set()
   queue = deque()
   start_vertex = graph.vertexlist.get(start)

   count_depth = 0
   timeToDepthIncrease = 0
   queue.appendleft(start_vertex.connectedTo)
   visited.add(start)
   timeToDepthIncrease += 1

   while len(queue) > 0:
      vertex = queue.pop()
      timeToDepthIncrease -= 1
      if timeToDepthIncrease == 0:
          count_depth += 1
          pendingDepthIncrease = True

      for new in vertex:
         if new not in visited:
            visited.add(new)
            temp_vertex = graph.vertexlist.get(new)
            newpath = temp_vertex.connectedTo.get(end)
            if newpath:
                return newpath
                break

            if count_depth > 2:
                continue
            else:
                queue.appendleft(temp_vertex.connectedTo)

      if pendingDepthIncrease:
         timeToDepthIncrease = queue.__len__()
         pendingDepthIncrease = False

   return None

if __name__ == '__main__':
    # if len(sys.argv) == 0 or len(sys.argv) < 5:
    #     print('Specify input and output arguments')
    #     sys.exit()
    # else:
    #     graph_input = sys.argv[1]
    #     payment_input =sys.argv[2]
    #     output1= sys.argv[3]
    #     output2= sys.argv[4]
    #     output3 = sys.argv[5]
        graph_input = "D:/Fall 2016/Insight 2016/batch_payment.csv"
        payment_input = "D:/Fall 2016/Insight 2016/stream_payment.csv"
        output1 = "D:/Fall 2016/Insight 2016/paymo_output/output1.txt"
        output2 = "D:/Fall 2016/Insight 2016/paymo_output/output2.txt"
        output3 = "D:/Fall 2016/Insight 2016/paymo_output/output3.txt"
        process(graph_input,payment_input,output1,output2,output3)
