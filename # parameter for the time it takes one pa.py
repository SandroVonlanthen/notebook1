# parameter for the time it takes one passenger to unload their luggage
time_unloading_luggage = 1

import os
from time import sleep

from IPython.display import clear_output
import numpy as np

from copy import deepcopy

# -------- fixed parameters -------- 
no_seats_per_row_per_side = 3
no_sides = 2

# -------- variable parameters -------- 
# the number of rows in the plane
# note that in the configuration linked above, there are 28 rows; however, for initial runs we suggest to use a smaller number
no_rows = 5
# the number of iterations it takes an agent to load thier lagguage
time_loading_lagguage = 1

# -------- parameters that depend on other values -------- 
no_seats = no_rows*no_seats_per_row_per_side*no_sides



class Db_Passenger:
    def __init__ (self, seat_no):
        # id = unique number between 1 & the number of seats
        # this corresponds to their seat number (-1 --> unassigned)
        self.id = seat_no
        
        # row number (starting from 1)
        self.row_no = int(seat_no / (no_seats_per_row_per_side*no_sides)) + 1
        
        # the seat number within the row
        self.column_no = seat_no % (no_seats_per_row_per_side*no_sides)
        # if the seat is accross the aisle, add 1 to its number
        if self.column_no >= no_seats_per_row_per_side:
            self.column_no += 1
                       
        # luggage un-loading status (initially, this is how long it takes an agent to unload their luggage)
        self.remaining_unloading_luggage = time_unloading_luggage
        
        # itinerary - what they have to do to get out of the plane
        self.itinerary = []
        # 1) get to the aisle
        if self.column_no < no_seats_per_row_per_side:
            self.itinerary += [(0, 1) for i in range(no_seats_per_row_per_side - self.column_no)]
        else:
            self.itinerary += [(0, -1) for i in range(self.column_no - no_seats_per_row_per_side)]
        # 2) unload the luggage
        self.itinerary += [("unload_luggage") for i in range(time_unloading_luggage)]
        # 3) advance on the aisle, i.e. move down, i.e. add (-1, 0) to their position
        self.itinerary += [(-1, 0) for i in range(self.row_no+1)]
    
    def __eq__ (self, other):
        '''Two passengers are equal if they have the same seat'''
        if isinstance(other, Db_Passenger):
            return self.id == other.id
        else:
            return False
    
    def __hash__(self):
        '''Passengers are hashed by their id'''
        return self.id
    

class Db_Plane:
    def __init__(self, priority = 'front'):
        # passengers are labeled by their sit number
        self.passengers = [Db_Passenger(i) for i in range(no_seats)]
        # frequency vector of passengers that moved this round (in one iteration a passenger can make at most one move)
        self.moved = {self.passengers[i]:0 for i in range(no_seats)}
        
        # the type of priority at deboarding
        self.priority = priority
        
        # current plane occupation
        # a value of -1 --> that space is empty
        # there is a row 0 (one extra space in front) and two rows at the end (for aisle space - no seats)
        self.no_rows_map = no_rows + 3
        self.no_cols_map = no_seats_per_row_per_side*no_sides + 1
        # start with the empty configuration
        self.map = [[-1 for c in range(self.no_cols_map)] for r in range(self.no_rows_map)]
        # fill in the seats
        for c in range(no_seats_per_row_per_side):
            for r in range(no_rows-1, -1, -1):
                self.map[r+1][c] = self.passengers[r*2*no_seats_per_row_per_side + c]
                self.map[r+1][2*no_seats_per_row_per_side - c] = self.passengers[(r+1)*2*no_seats_per_row_per_side - c - 1]
    
    def print_map(self):
        '''Prints the current plane map.'''
        
        for r in range(self.no_rows_map):
            current_row = ""
            for c in range(self.no_cols_map):
                if self.map[r][c] != -1:
                    l = len(str(self.map[r][c].id))
                    spaces = "  "
                    for i in range(3-l):
                        spaces += " "
                    current_row += spaces + str(self.map[r][c].id)
                elif r in [0, self.no_rows_map-2, self.no_rows_map-1] and c != no_seats_per_row_per_side:
                    # these are unaccessible places
                    current_row += "  xxx"
                else:
                    current_row += "  ___"
            print(current_row)
    
    def reset_moved(self):
        '''Resets moved to only 0'''
        
        for p in self.moved:
            self.moved[p] = 0
    
    def nobody_on_row(self, r):
        '''Checks if there are no passengers on row r.
        True --> nobody on row r
        False --> sombody is on row r'''
        
        found_somebody = False
        for c in range(self.no_cols_map):
            if self.map[r][c] != -1:
                found_somebody = True
        
        return not found_somebody
    
    def move(self, passenger_position):
        '''The passenger currently on the position passenger_position, and can start loading their luggage.
        They do one step in their itinerary.'''
                  
        row, column = passenger_position
        passenger = self.map[row][column]
          
        
        # keep track if somebody moved
        somebody_moved = False
        
        # if the passenger already moved this round, stop
        if self.moved[passenger] == 1:
            return somebody_moved
        
        # Case 1: they need to unload their luggage
        if passenger.itinerary[0] == "unload_luggage":
            if passenger.remaining_unloading_luggage:
                passenger.remaining_unloading_luggage -= 1
                passenger.itinerary.pop(0)
                self.moved[passenger] = 1
                somebody_moved = True

        # Case 2: they need to advance
        else:
            # the position the passeger needs to move to
            move_to = np.array(passenger_position) + np.array(passenger.itinerary[0])
            move_to = [int(i) for i in move_to]

            if self.map[move_to[0]][move_to[1]] == -1:           
                # move the passenger (unless they exit the plane)
                if move_to[0] != -1:
                    self.map[move_to[0]][move_to[1]] = passenger
                self.map[passenger_position[0]][passenger_position[1]]  = -1

                # remove that move from their itinerary
                passenger.itinerary.pop(0)
                    
                # the passenger moved
                self.moved[passenger] = 1
                somebody_moved = True
                

        return somebody_moved   
    
    def one_iteration(self):
        '''One time period passed.
        1) each agent that can exit the plane exits the plane
        2) passengers that need to unload to this
        3) passengers advance on their row (without getting on the aisle)
        4) depending on the priority, agents advance
        '''
        
        # 0) So far, nobody moved in this iteration
        self.reset_moved()
        
        # Everybody can move at most once
        progress_this_iteration = False
        somebody_moved = True
        
        while somebody_moved:
            somebody_moved = False

            # 1) passengers that need to unload do that (note, they must be on the aisle)
            for r in range(self.no_rows_map-1, -1, -1):
                c = no_seats_per_row_per_side
                if self.map[r][c] != -1 and self.map[r][c].itinerary[0] == "unload_luggage":
                    m = self.move((r,c))
                    if m: somebody_moved = True

            # 2) passengers can advance on their row (without getting on the aisle, do this)
            def advance_on_row(r):
                progress = False
                for c_change in range(2, no_seats_per_row_per_side +1):
                    cols = [no_seats_per_row_per_side - c_change, no_seats_per_row_per_side + c_change] if c_change else [no_seats_per_row_per_side]
                    for c in cols:
                        if self.map[r][c] != -1:
                            m = self.move((r,c))
                            if m: progress = True
                return progress

            for r in range(self.no_rows_map):
                m = advance_on_row(r)
                if m: somebody_moved = True

           # 3) the other agents move (depending on their priority)
            if self.priority == 'front':
                # Use the space here to write the rest of the moves for the agents with priority front
                # Hint: you might find the function nobody_on_row helpful
                
                
            
                #for passenger in self.passengers:
                #    if (self.nobody_on_row(passenger.row_no-1)==True):
                #        
                #print (progress_this_iteration)
                self.move((1,2))
                self.move((1,3))
                return 'Function not implemented'

                    
            elif self.priority == 'back':
                # Use the space here to write the rest of the moves for the agents with priority front
                return 'Function not implemented'
            
            if somebody_moved:
                
                progress_this_iteration = True
                
        return progress_this_iteration



# how many seconds python should wait between printing the next step of the interation
sleep_time_between_prints = 1


class Db_Simulation:
    def __init__ (self, random_seed = 97, priority = 'front', print_map = True):
        # 1)  wheter there are itnermediate prints of themap while simulating
        self.print_map = print_map
        
        # 2) parameters for the simulation
        # the ordering of passengers - random by default
        self.priority = priority
        
        # the random seed
        self.seed = random_seed
        
        # 3) statistics keept during simulation
        # the number of iterations until the plane is full
        self.no_iterations = -1
    
    def run(self):
        '''This function runs a simulation with the defined parameters'''
        # 0) set the random seed
        np.random.seed(self.seed)
        
        # 1) define a plane
        pl = Db_Plane(priority = self.priority)
        
        # 2) run the simulation, updating the statistics
        still_arranging = True
        while still_arranging:

            self.no_iterations += 1
            if self.print_map:
                sleep(sleep_time_between_prints)
                clear_output(wait = True)
                print ("Iteration #", self.no_iterations)
                pl.print_map()
            still_arranging = pl.one_iteration()
        
        return self.no_iterations

Db_Simulation(97,'front', True).run()