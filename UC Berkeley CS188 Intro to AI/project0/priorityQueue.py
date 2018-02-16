# author: Georgios Kamaras - 1115 2014 00058

import heapq    # python library for the various heap functions

class PriorityQueue:

    def __init__(self):
        self.heap = []     # list that implements our heap
        self.count = 0     # how many elements in queue

    def push(self, item, priority=0):
        """ Add a new item with a certain priority """
        entry = [priority, item]            # "create" the heap's entry
        heapq.heappush(self.heap, entry)    # push the entry to heap
        self.count += 1                     # we have one more element in our queue

    def isEmpty(self):
        """ Check if pq is empty """
        if self.count == 0:         # if there are no elements, our queue is empty
            return True
        return False

    def pop(self):
        """ Pop item with the lowest priority """
        if self.isEmpty():          # if queue is empty, there is nothing to be popped
            print "ERROR. Priority Queue is empty!"
            return None
        entry = heapq.heappop(self.heap)    # pop the element with the highest priority (smallest priority number)
        self.count -= 1                     # we have one less element in our queue
        return entry[1]                     # return (just) the item

    def update(self, item, priority=0):
        isIn = False                # flag to note if the given item is already in the priority queue
        for entry in self.heap:
            if entry[1] == item:    # if the given item is already in queue
                isIn = True         # note it
                if entry[0] <= priority:
                    print "%s is already in queue, with priority %d" %(entry[1], entry[0])
                else:               # we need to update our item's current priority to a better one
                    entry[0] = priority     # update item's priority

                heapq.heapify(self.heap)	# to make sure that all the items are in the correct order, based on their priority
                break	# we want to update the priority just for the first item that we encounter

        if isIn == False:   # if the given item is not already in the priority queue
            self.push(item, priority)   # just push it in the queue like any other new item

def PQSort(integerList):
    pq = PriorityQueue()    # create a priority queue
    for i in integerList:   # push each given integer inside our priority queue
        pq.push(i,i)        # the number serves both as an item's "label" and as an item's priority
    return [pq.pop() for i in range(len(integerList))]   # parameters' integerList has the same length with the returned ordered list

# my main function, not necessary, everything runs ok even without it (you can comment everything if you want)
if __name__ == "__main__":
    q = PriorityQueue() # creating my priority queue "q"
    # the commands that are used as an example in our assignment
    q.push("task1", 1)
    q.push("task1", 2)
    q.push("task0", 0)
    t = q.pop()
    print t
    t=q.pop()
    print t
    q.push("task3", 3)
    q.push("task3", 4)
    q.push("task2", 0)
    t=q.pop()
    print t
    print PQSort([2,5,3,6,1,4,7,9,0,8]) # testing my PQSort() function
