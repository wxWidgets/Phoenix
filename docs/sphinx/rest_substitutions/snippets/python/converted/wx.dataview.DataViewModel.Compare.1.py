

    obj1 = self.ItemToObject(item1)
    obj2 = self.ItemToObject(item2)
    if obj1[column] == obj2[column]:
        return 1 if ascending == (item1.GetId() > item2.GetId()) else -1
    else:
        return 1 if ascending == (obj1[column] > obj2[column]) else -1
