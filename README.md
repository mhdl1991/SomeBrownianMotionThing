# SomeBrownianMotionThing
A little thing done with Python 3 and Pyglet that seems to simulate something akin to Brownian motion

You have a grid of cells that can have a value from 0 to 16

## At each step:

* cells higher than a certain value will "Diffuse" into Adjacent cells (Orthogonal directions)

        ....            .1..
        .5..    --->    111.
        ....            .1..
    
* cells have a chance to "Move" into an adjacent cell
    
    
        ....            ....
        .5..    --->    ..5.
        ....            ....
        
## Controls:
    
* **E** to Clear out the entire board
* **P** to Pause the simulation
* **R** to Randomize the board
* **Left Mouse** to set the value of a cell to 16
* **Right Mouse** to set the value of a cell to 0
