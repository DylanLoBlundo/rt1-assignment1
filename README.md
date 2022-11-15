# rt1-assignment1
**Institution:** *Università di Genova*<br>
**Course:** *MSc in Robotics Engineering*<br>
**Subject:** *Research Track 1*<br>
**Author:** *Dylan Lo Blundo*<br>

**Assignment 1**<br>

**Introduction**
============================
This is the first assignment of the "Research Track 1" course, in the Robotics Engineering degree.
In the simulator there is a robot in an arena, with it there are gold and silver boxes.
The robot must take silver box and put it near to the gold box.

**Running the program**
============================
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

To start the program just need to launch the file "start"

**Description**
============================
There are some ways to solve this exercise.
For example one way is go to a silver box, grab it, turn around 180 deg, go to gold box (I know that forward to me there is the nearest gold box), release, turn around 180 deg, go to silver box and repeat the loop.
I chose another way, I wanted to create a general template because I imagined that in a real situation there could be problems.
For example the boxes location, it's differnt from the one proposed in the exercise, or changes due to external interventions.
To avoid this problem the robot scans the map (turning of 360 deg) to know the position of every box in the arena.
He does this scan every time he grabs and release a box, and of course at the start of the program.
So if something or someone moves one or more boxes, it's not a problem because the robot knows the new positions.
After the scan he finds the nearest box.
When he grabs or releases a box near to the gold box, he adds them to a list of complete boxes and when he searches the nearest box, he searches them from a list without boxes that are done, so when there are not boxes to go implies that he terminated his work.

**Pseudocode**
============================
``` 
create a list empty of doneBox in the arena
while simulation is running
  allBox = scanMap()
  if allBox is empty
    exit
  find nearest silver box
  allign to it
  go to it
  grab it
  insert it in the doneBox list
  allBox = scanMap()
  find the nearest gold box
  allign to it
  go to it
  release the silver box near the gold box
  insert the gold box in the donebox list
  ```
