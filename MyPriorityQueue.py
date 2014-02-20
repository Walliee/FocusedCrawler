from Queue import PriorityQueue

# Queue implementation for Priority Queue that keeps track of insertion and 
# checks queue before new insertion to avoid duplicate insertions

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.all_items = set()
        self.counter = 0

    def put(self, item, priority):
        if item not in self.all_items:
            PriorityQueue.put(self, (priority, self.counter, item))
            self.all_items.add(item)
            self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item
    
a = MyPriorityQueue()
a.put(unicode("http://cse.poly.edu/~tehila/"), 1)
a.put(unicode("http://cse.poly.edu/~tehila/"), 1)
a.put(unicode("http://cse.poly.edu/~tehila/"), 1)
a.put(unicode("http://cse.poly.edu/~tehila/"), 2)


for item in list(a.queue):
    print item