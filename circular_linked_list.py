class PrayerSlot(object):
    def __init__(self, name, athan, iqama):
        self.name = name
        self.athan = athan
        self.iqama = iqama


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def get_total_minutes(self, t):
        head, sep, tail = t.partition(' ')
        tt = head.split(':')
        return int(tt[0]) * 60 + int(tt[1]) * 1

    def is_current(self, current, start, end):
        t = self.get_total_minutes(current)
        s = self.get_total_minutes(start)
        e = self.get_total_minutes(end)
        r = False

        if e > s:
            if t >= s and t < e:
                r = True
        else:
            r = not self.is_current(current, end, start)

        return r


class CircularLinkedList:
    def __init__(self):
        self.last = None

    def add_to_empty(self, data):

        if self.last != None:
            return self.last

        new_node = Node(data)
        self.last = new_node

        self.last.next = self.last
        return self.last

    def add(self, data):
        # check if the node is empty
        if self.last == None:
            return self.add_to_empty(data)
        new_node = Node(data)
        new_node.next = self.last.next
        self.last.next = new_node
        self.last = new_node

        return self.last

    def traverse_updated(self, current_time):
        current_node = self.last
        while not current_node.is_current(current_time, current_node.data.iqama.strftime("%H:%M"), current_node.next.data.iqama.strftime("%H:%M")):
            current_node = current_node.next
        return current_node
