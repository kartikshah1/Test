"""
This file stores the functions used by generic playlist
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
        if (sa[i][0] != sb[i][0]) or (sa[i][1] != sb[i][2]):
            return False
    for i in range(N):
        for j in range(N):
            if(a[i][0] == b[j][0]) and a[i][1] == b[j][2]:
                c.append(b[j])
                break
    return c


def to_array(mylist):
    a = json.loads(mylist)
    return a


def append(obj, mylist, contenttype):
    a = json.loads(mylist)
    N = len(a)
    count = 0
    for i in range(N):
        if(a[i][2] == contenttype):
            count += 1
    a.append([obj, count, contenttype])
    mylist = json.dumps(a)
    return mylist


def delete(mylist, pk, contenttype):
    a = json.loads(mylist)
    N = len(a)
    for i in range(N):
        if (int(a[i][0]) == int(pk)) and (int(a[i][2]) == int(contenttype)):
            myindex = i
            rank = a[myindex][1]
            for j in range(N):
                if (a[j][2] == int(contenttype)) and (a[j][1] > rank):
                    a[j][1] -= 1
            del a[myindex]
            mylist = json.dumps(a)
            return mylist
    return False
