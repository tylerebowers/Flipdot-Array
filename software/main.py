from interface.display_simulator import Display
#from interface.display import Display
import runners


d = Display()
#runners.self_test(d)

"""
modes:
"clock": (runners.Clock, (False,))
"game_of_life": (runners.GameOfLife, (2,))
"""

runner = None
new_mode = (runners.GameOfLife, (2,))#(runners.Clock, (False,))

while True:
    if new_mode is not None:
        runner = new_mode[0](d, *new_mode[1])
        new_mode = None
    else:
        runner.update()
    
