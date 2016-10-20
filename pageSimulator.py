import random
import sys

class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

class LinkedList(object):
    def __init__(self, head=None):
        self.head = head
		
    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
          if current.get_data() == data:
              found = True
          else:
              previous = current
              current = current.get_next()
        if current is None:
          raise ValueError("Data not in list")
        if previous is None:
          self.head = current.get_next()
        else:
          previous.set_next(current.get_next())	
		
    def deleteLast(self):
        current = self.head
        previous = None
        found = False
        while current.get_next() is not None:
           previous = current
           current = current.get_next()
        lastValue = current.get_data()
        previous.set_next(None)
        current = None
        return lastValue
	
    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
          if current.get_data() == data:
             found = True
          else:
             current = current.get_next()
        if current is None:
             raise ValueError("Data not in list")
        return current
	
def pageSimulator(string,references):
   memory = [-1,-1,-1,-1]
   frequency = {}
   sequence = []
   hit = 0
   miss = 0
   if string=="FIFO":
      fifocounter = 0
      for i in range(0,references):
        if(i < 4 or fifocounter < 4):
           r = random.randint(0,9)
           if r not in memory:
              memory[fifocounter%4] = r
      	      fifocounter+=1
              miss+=1
           else: hit+=1
        else:
           value = randomizer(memory,fifocounter%4)
    	   if value not in memory:
               print "Evicted page %d from frame %d" %(memory[fifocounter%4], fifocounter%4)
    	       memory[fifocounter%4] = value
               print "Added page %d" %(memory[fifocounter%4])
    	       fifocounter+=1
               miss+=1
           else: hit+=1
        print "After reference %d: %s" %(i+1,str(memory))
   
   elif string == "LRU":
       lru = LinkedList()
       counter = 0
       for i in range(0,references):
        if -1 in memory:
           r = random.randint(0,9)
           if r not in memory:
             memory[counter] =  r
             sequence.append(r)
             lru.insert(r)
             counter+=1
             miss+=1
           else:
             sequence.append(r)
             lru.delete(r)
             lru.insert(r)
             hit+=1			 
        else:
           value = randomizer(sequence,counter-1)
           if value not in memory:
             lastValue = lru.deleteLast()
             lastValueIndex = memory.index(lastValue)
             memory[lastValueIndex] = value
             sequence.append(value)
             lru.insert(value)
             print "Evicted page %d from frame %d" %(lastValue, lastValueIndex)
             counter+=1
             print "Added page %d" %(memory[lastValueIndex])
             miss+=1
           else:
             sequence.append(value)
             lru.delete(value)
             lru.insert(value)
             hit+=1
        print "After reference %d: %s" %(i+1,str(memory))

   elif string=="random":
      counter = 0
      for i in range(0,references):
    	randomcounter = random.randint(0,3)
        if -1 in memory:
           r = random.randint(0,9)
           if r not in memory:
              if memory[randomcounter] != -1: print "Evicted page %d from frame %d" %(memory[randomcounter], randomcounter)
              memory[randomcounter] = r
              if memory[randomcounter] != -1: print "Added page %d" %(memory[randomcounter])
              miss+=1
           else:hit+=1
           sequence.append(r)
        else:
           value = randomizer(sequence,counter-1)
           if value not in memory:
              print "Evicted page %d from frame %d" %(memory[randomcounter], randomcounter)
    	      memory[randomcounter] = value
              print "Added page %d" %(memory[randomcounter])
              sequence.append(value)
    	      counter+=1
              miss+=1
           else: hit+=1
        print "After reference %d: %s" %(i+1,str(memory))
   elif string == "LFU":
      counter = 0
      for i in range(0,references):
          if -1 in memory:
            r = random.randint(0,9)
            if r not in memory:
              if memory[counter%4] != -1: print "Evicted page %d from frame %d" %(memory[counter%4], counter)
              memory[counter%4] = r
              if memory[counter%4] != -1: print "Added page %d" %(memory[counter%4])
              miss+=1
            else: hit+=1
            if r not in frequency: frequency[r] = 1
            else: frequency[r]+=1
            sequence.append(r)
            counter+=1   
          else:
            value = randomizer(sequence,counter-1)
            if value not in memory:
               newfrequency = {memory[0]:frequency[memory[0]],memory[1]:frequency[memory[1]],memory[2]:frequency[memory[2]],memory[3]:frequency[memory[3]]}
               number = min(newfrequency,key=newfrequency.get)
               slot = memory.index(number)
               print "Evicted page %d from frame %d" %(memory[slot], slot)
               memory[slot] = value
               miss+=1
               print "Added page %d" %(memory[slot])
            else: hit+=1
            if value not in frequency: frequency[value] = 1
            else: frequency[value]+=1
            sequence.append(value)
            counter+=1
          print "After reference %d: %s" %(i+1,str(memory))

   elif string == "MFU":
      counter = 0
      for i in range(0,references):
          if -1 in memory:
            r = random.randint(0,9)
            if r not in memory:
              if memory[counter%4] != -1: print "Evicted page %d from frame %d" %(memory[counter%4], counter)
              memory[counter%4] = r
              if memory[counter%4] != -1: print "Added page %d" %(memory[counter%4])
              miss+=1
            else: hit+=1
            if r not in frequency: frequency[r] = 1
            else: frequency[r]+=1
            sequence.append(r)
            counter+=1   
          else:
            value = randomizer(sequence,counter-1)
            if value not in memory:
               newfrequency = {memory[0]:frequency[memory[0]],memory[1]:frequency[memory[1]],memory[2]:frequency[memory[2]],memory[3]:frequency[memory[3]]}
               number = max(newfrequency,key=newfrequency.get)
               slot = memory.index(number)
               print "Evicted page %d from frame %d" %(memory[slot], slot)
               memory[slot] = value
               miss+=1
               print "Added page %d" %(memory[slot])
            else: hit+=1
            if value not in frequency: frequency[value] = 1
            else: frequency[value]+=1
            sequence.append(value)
            counter+=1
          print "After reference %d: %s" %(i+1,str(memory))
   print "Hit : %d" %hit
   print "Miss: %d" %miss
   print "Ratio:" ,(float(hit)/miss)*100
def randomizer(memory,counter):
   r = random.random
   pages = [0,1,2,3,4,5,6,7,8,9]
   if(r < 0.7):
      return pages[memory[counter]]
   elif(0.7 < r and r <= 0.8):
	  return pages[memory[(counter-1)]]
   else:
      pages.remove(memory[counter])
      if memory[counter-1] in pages: pages.remove(memory[(counter-1)])
      return pages[random.randint(0,7)]

def pageSimulatorWriter(string):
   for i in range(0,5):
        pageSimulator(string,100)
		
orig_stdout = sys.stdout
f = file('results.txt', 'w')
sys.stdout = f
print 'FIFO'
pageSimulatorWriter('FIFO')
print 'LRU'
pageSimulatorWriter('LRU')
print 'random'
pageSimulatorWriter('random')
print 'LFU'
pageSimulatorWriter('LFU')
print 'MFU'
pageSimulatorWriter('MFU')
sys.stdout = orig_stdout
f.close()