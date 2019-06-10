# SomeBrownianMotionThing

A little cellular automata thing done with Python 3 and Pyglet that seems to simulate something akin to Brownian motion

You have a grid of cells that can have values of:

* 0 (Empty space)
* 1-8 (Gas-filled)
* -1 (Frozen/Solid)

## At each step:

* "Filled" cells higher than a certain value will "Diffuse" into Adjacent cells (Orthogonal directions) so long as they are not solid

        ....            .1..
        .5..    --->    111.
        ....            .1..
    
* "Filled" cells have a chance to "Move" into an adjacent non-solid cell
    
    
        ....            ....
        .5..    --->    ..5.
        ....            ....
        
* cells will freeze if adjacent to a "frozen" cell (represented by cells having a value of -2)
    
    
        ....            ....
        .5X.    --->    .XX.
        ....            ....
        
## Controls:
    
* **E** to Clear out the entire board
* **P** to Pause the simulation
* **R** to Randomize the board
* **Left Mouse** to set the value of a cell to 8
* **Right Mouse** to toggle the value of a cell to -1 or 0
