"""
This file stores the functions used by playlist
"""
import json


def is_valid(mylist, actuallist):
    """
    To keep the sanctity of the playlist, we would want checks of the sort of
    count same at both places and ids are correct
    """
    a = json.loads(mylist)
    sa = sorted(a)
    b = json.loads(actuallist)
    sb = sorted(b)
    N = len(a)
    M = len(b)
    if(N != M):
        return False
    c = []
    for i in range(N):
        if not(sa[i] == sb[i][0]):
            return False
    for i in range(N):
        for j in range(N):
            if(a[i] == b[j][0]):
                c.append(b[j])
                break
    return c


def to_array(mylist):
    a = json.loads(mylist)
    return a


def append(obj, mylist):
    a = json.loads(mylist)
    a.append([obj, len(a)])
    mylist = json.dumps(a)
    return mylist


def delete(mylist, pk):
    a = json.loads(mylist)
    N = len(a)
    for i in range(N):
        if int(a[i][0]) == int(pk):
            myindex = i
            rank = a[myindex][1]
            for i in range(N):
                if a[i][1] > rank:
                    a[i][1] -= 1
            del a[myindex]
            mylist = json.dumps(a)
            return mylist
    return False
