from __future__ import print_function

import time

import numpy as np

from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()


def scanMap(doneBox):
    """
    Function to scan the environment to find all box on the map.
    Scan has computed every 30 degrees
    Then, this function remove (from the allBox list) duplicates and done box.

    Args: doneBox (array list each with two integers elements)

    Return: a list of allBox without duplicates and done box 
    """
    allBox = list()
    temp = R.see()
    for i in range(len(temp)):
        allBox.append(temp[i])

    # Does a 360 degrees and scans every 30 degrees
    for i in range(15):
        turn(10, 0.75)
        #time.sleep(0.25)
        temp = R.see()
        for j in range(len(temp)):
            allBox.append(temp[j])
    
    # Removes duplicates and done box from the list
    duplicateCode = list()
    for i in range(len(allBox)):
        if (not(i in duplicateCode)):
            for j in range(len(allBox)):
                if (i != j):
                    if ((allBox[i].info.code == allBox[j].info.code) and (allBox[i].info.marker_type == allBox[j].info.marker_type)):
                        duplicateCode.append(j)

    newAllBox = list()
    for i in range(len(allBox)):
        if (not(i in duplicateCode)):
            newAllBox.append(allBox[i])

    # Removes done box from newAllBox
    if len(doneBox) != 0:
        notDoneAllBox = list()
        
        for i in range(len(newAllBox)):
            type = 0
            if (newAllBox[i].info.marker_type == MARKER_TOKEN_SILVER):
                type = 0
            elif (newAllBox[i].info.marker_type == MARKER_TOKEN_GOLD):
                type = 1

            temp = [newAllBox[i].info.code, type]
            count = 0

            for j in range(len(doneBox)):
                if (False == (np.array_equal(temp, doneBox[j]))):
                    count += 1

            if (count == len(doneBox)):
                notDoneAllBox.append(newAllBox[i])
        return notDoneAllBox
    return newAllBox
    

def findNearestBox(allBox, markerType):
    """"
    Function to find the nearest box (silver or gold) from a list
    that contains all boxes.

    Args: allBox (list), markerType (int)

    Return: dist (float), rot_y (float) and code (int) of the nearest box
    """
    if (markerType == 0):
        distances = []
        for i in range(len(allBox)):
            if (allBox[i].info.marker_type == MARKER_TOKEN_SILVER):
                distances.append([allBox[i].dist, allBox[i].rot_y, allBox[i].info.code])
        distAndRot = min(distances)
        dist = distAndRot[0]
        rot_y = distAndRot[1]
        code = distAndRot[2]

    elif (markerType == 1):
        distances = []
        for i in range(len(allBox)):
            if (allBox[i].info.marker_type == MARKER_TOKEN_GOLD):
                distances.append([allBox[i].dist, allBox[i].rot_y, allBox[i].info.code])
        distAndRot = min(distances)
        dist = distAndRot[0]
        rot_y = distAndRot[1]
        code = distAndRot[2]

    return dist, rot_y, code

    
def updateDist(dist, rot_y, code, markerType):
    """
    Function to update the distance (dist and rot_y) between robot and box
    while the robot moves on it

    Args: dist (float), rot_y (float), code (int), markerType (int)

    Return: dist (float), rot_y (float)
    """
    box = R.see()
    if (markerType == 0):
        count = 0
        for i in range(len(box)):
            if (box[i].info.code == code and box[i].info.marker_type == MARKER_TOKEN_SILVER):
                count += 1
                dist = box[i].dist
                rot_y = box[i].rot_y
        if count == 0:
            allign(code, markerType)
    elif (markerType == 1):
        count = 0
        for i in range(len(box)):
            if (box[i].info.code == code and box[i].info.marker_type == MARKER_TOKEN_GOLD):
                count += 1
                dist = box[i].dist
                rot_y = box[i].rot_y
        if count == 0:
            allign(code, markerType)    
    return dist, rot_y 


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	    seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	    seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def goTo(dist, rot_y, code, markerType):
    """
    Function to go to the chosen box

    Args: dist (float), rot_y (float), code (int) and markerType (int)
    """
    if dist == -1:
        print("dist == -1")
        return
    elif (((markerType == 0) and (dist < d_th)) or ((markerType == 1) and (dist < 0.5))):
        return
    elif -a_th<= rot_y <= a_th:
        drive(10, 0.5)
    elif rot_y < -a_th:
        turn(-2, 0.5)
    elif rot_y > a_th:
        turn(+2, 0.5)
    dist, rot_y = updateDist(dist, rot_y, code, markerType)
    goTo(dist, rot_y, code, markerType)


def allign(code, markerType):
    """
    Function to allign to the box

    Args: code (int), markerType (int)
    """
    if (markerType == 0):
        box = R.see()
        for i in range(len(box)):
            if ((box[i].info.code == code) and (box[i].info.marker_type == MARKER_TOKEN_SILVER)):
                return goTo(dist, rot_y, code, 0)
    elif (markerType == 1):
        box = R.see()
        for i in range(len(box)):
            if ((box[i].info.code == code) and (box[i].info.marker_type == MARKER_TOKEN_GOLD)):
                return

    # Turn 30 degrees
    turn(10, 0.75)
    allign(code, markerType)


doneBox = list()
print()
while 1:
    allBox = scanMap(doneBox)

    # Remember that allBox contains all boxes are not done,
    # so if it's empty it means that He has completed his work
    if (not (allBox)):
        print("I have completed my work!")
        exit()
    
    # Find the nearest box in allBox
    dist, rot_y, code = findNearestBox(allBox, 0)

    # Once he completes his 360, he must allign to the nearest box
    print("I'm going to", code, "silver")
    allign(code, 0)

    # Once he did allign to the nearest box he must go to it
    goTo(dist, rot_y, code, 0)

    R.grab()
    print("Grab")
    print()

    # When he grabs it, he adds the box in a list
    # that contains all boxes that are done
    doneBox.append([code, 0])

    # Repeate the steps but for golden box
    allBox = scanMap(doneBox)
    dist, rot_y, code = findNearestBox(allBox, 1)
    print("I'm going to", code, "gold")
    allign(code, 1)
    goTo(dist, rot_y, code, 1)
    R.release()
    print("Release")
    print()
    doneBox.append([code, 1])