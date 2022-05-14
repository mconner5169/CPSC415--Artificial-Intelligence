'''
CPSC 415 -- Homework #4 support file
Morgan Conner, University of Mary Washington, fall 2021
'''

from wumpus import ExplorerAgent

import random

class KB():

    def __init__(self):
        self.finish_space = []
        self.safe_spaces = set()
        self.stench_spaces = []
        self.wumpus_space = []
        self.possible_wumpus = set()
        self.breeze_spaces = []
        self.pit_spaces = set()
        self.possible_pits = []
        self.bump_spaces = []
        self.have_gold = False
        self.mapping = [['NotVisited' for i in range(4)] for j in range(4)]


    def safe_space_detected_at(self, loc):
        x = loc[0]
        y = loc[1]
        self.mapping[x][y] = 'Safe'
        self.safe_spaces.add(loc)

    def breeze_detected_at(self, loc):
        x = loc[0]
        y = loc[1]
        if self.mapping[x][y] == 'Breeze':
            return True
        else:
            self.mapping[x][y] = 'Breeze'
            self.breeze_spaces.append(loc)
            return False

    def stentch_detected_at(self, loc):
        x = loc[0]
        y = loc[1]
        self.mapping[x][y] = 'Stench'
        self.stench_spaces.append(loc)

    def bump_detected_at(self, loc, _facing_direction):
        x = loc[0]
        y = loc[1]

        if _facing_direction == 'Up':
            if y != 3:
                self.mapping[x][y+1] = 'Wall'
                self.bump_spaces.append(loc)
        elif _facing_direction == 'Down':
            if y != 0:
                self.mapping[x][y-1] = 'Wall'
                self.bump_spaces.append(loc)
        elif _facing_direction == 'Right':
            if x != 3:
                self.mapping[x+1][y] = 'Wall'
                self.bump_spaces.append(loc)
        elif _facing_direction == 'Left':
            if x != 0:
                self.mapping[x-1][y] = 'Wall'
                self.bump_spaces.append(loc)

    def is_space_safe(self, loc):
        x = loc[0]
        y = loc[1]
        try:
            if (self.mapping[x][y] == 'Safe') or (loc in self.safe_spaces):
                return True
        except IndexError:
            pass
        return False

    def is_space_notVisited(self, loc):
        x = loc[0]
        y = loc[1]
        if self.mapping[x][y] == 'NotVisited':
            return True
        return False

    def find_safe_space(self, loc, _facing_direction, future_actions):
        x = loc[0]
        y = loc[1]

        #Finds location of safe space relative to player's location
        safe_space_right = self.is_space_safe((x+1,y))
        safe_space_left = self.is_space_safe((x-1,y))
        safe_space_up = self.is_space_safe((x,y+1))
        safe_space_down = self.is_space_safe((x,y-1))

        #Records series of actions to reach safe space
        if ((safe_space_right and _facing_direction == 'Right') or (safe_space_left and _facing_direction == 'Left') or (safe_space_up and _facing_direction == 'Up') or (safe_space_down and _facing_direction == 'Down')):
            future_actions.extend(['Forward'])
            return
        elif ((safe_space_right and _facing_direction == 'Up') or (safe_space_up and _facing_direction == 'Left') or (safe_space_down and _facing_direction == 'Right') or (safe_space_left and _facing_direction == 'Down')):
            future_actions.extend(['TurnRight', 'Forward'])
            return
        elif ((safe_space_right and _facing_direction == 'Left') or (safe_space_left and _facing_direction == 'Right') or (safe_space_up and _facing_direction == 'Down') or (safe_space_down and _facing_direction == 'Up')):
            future_actions.extend(['TurnRight', 'TurnRight', 'Forward'])
            return
        elif ((safe_space_right and _facing_direction == 'Down') or (safe_space_left and _facing_direction == 'Up') or (safe_space_up and _facing_direction == 'Right') or (safe_space_down and _facing_direction == 'Left')):
            future_actions.extend(['TurnLeft', 'Forward'])
            return
        else:
            self.find_notVisited_space(loc, _facing_direction, future_actions)
            return

    def find_spaces_home(self, loc, _facing_direction, future_actions):
        x = loc[0]
        y = loc[1]

        #safe_space_left = self.is_space_safe((x-1,y))
        #safe_space_down = self.is_space_safe((x,y-1))

        if (self.mapping[x][y-1] != 'Pit') or (self.mapping[x][y-1] != 'Wumpus'):
            safe_space_down = True
        else:
            safe_space_down = False
        if (self.mapping[x-1][y] != 'Pit') or (self.mapping[x-1][y] != 'Wumpus'):
            safe_space_left = True
        else:
            safe_space_left = False

        if ((safe_space_left and _facing_direction == 'Left') or (safe_space_down and _facing_direction == 'Down')):
            future_actions.extend(['Forward'])
            return
        if ((safe_space_down and _facing_direction == 'Right') or (safe_space_left and _facing_direction == 'Down')):
            future_actions.extend(['TurnRight', 'Forward'])
            return
        if ((safe_space_left and _facing_direction == 'Right') or (safe_space_down and _facing_direction == 'Up')):
            future_actions.extend(['TurnRight', 'TurnRight', 'Forward'])
            return
        if ((safe_space_left and _facing_direction == 'Up') or (safe_space_down and _facing_direction == 'Left')):
            future_actions.extend(['TurnLeft', 'Forward'])
            return

        if (safe_space_down == False) and (safe_space_left == False):
            self.find_notVisited_space(loc, _facing_direction, future_actions)

    def find_notVisited_space(self, loc, _facing_direction, future_actions):
        x = loc[0]
        y = loc[1]

        notVisited_space_right = None
        notVisited_space_left = None
        notVisited_space_up = None
        notVisited_space_down = None

        #Finds location of safe space relative to player's location
        if x < 3:
            notVisited_space_right = self.is_space_notVisited((x+1,y))
        if x > 0:
            notVisited_space_left = self.is_space_notVisited((x-1,y))
        if y < 3:
            notVisited_space_up = self.is_space_notVisited((x,y+1))
        if y > 0:
            notVisited_space_down = self.is_space_notVisited((x,y-1))

        #Space that's not visited is not close to player
        spaceVisited_count = 0
        if notVisited_space_down == False:
            spaceVisited_count += 1 
        if notVisited_space_right == False:
            spaceVisited_count += 1
        if notVisited_space_up == False:
            spaceVisited_count += 1
        if notVisited_space_left == False:
            spaceVisited_count += 1

        if spaceVisited_count == 4:
            return False
        else:
            #Records series of actions to reach a notVisited space
            if ((notVisited_space_right and _facing_direction == 'Right') or (notVisited_space_left and _facing_direction == 'Left') or (notVisited_space_up and _facing_direction == 'Up') or (notVisited_space_down and _facing_direction == 'Down')):
                future_actions.extend(['Forward'])
                return
            elif ((notVisited_space_right and _facing_direction == 'Up') or (notVisited_space_up and _facing_direction == 'Left') or (notVisited_space_down and _facing_direction == 'Right') or (notVisited_space_left and _facing_direction == 'Down')):
                future_actions.extend(['TurnRight', 'Forward'])
                return
            elif ((notVisited_space_right and _facing_direction == 'Left') or (notVisited_space_left and _facing_direction == 'Right') or (notVisited_space_up and _facing_direction == 'Down') or (notVisited_space_down and _facing_direction == 'Up')):
                future_actions.extend(['TurnRight', 'TurnRight', 'Forward'])
                return
            elif ((notVisited_space_right and _facing_direction == 'Down') or (notVisited_space_left and _facing_direction == 'Up') or (notVisited_space_up and _facing_direction == 'Right') or (notVisited_space_down and _facing_direction == 'Left')):
                future_actions.extend(['TurnLeft', 'Forward'])
                return
            else:
                future_actions.extend(['Forward'])
                return

    def find_pit(self, loc):
        x = loc[0]
        y = loc[1]
        num_of_breezes = 0

        try:
            if (self.mapping[x][y] == 'Breeze' and ((self.mapping[x+1][y-1]) or (self.mapping[x+1][y+1]) or (self.mapping[x+2][y])) == 'Breeze'):
                self.mapping[x+1][y] = 'Pit' #player is on left side of pit
                self.pit_spaces.add((x+1,y))
                try:
                    self.possible_pits.remove((x+1,y))
                except ValueError:
                    pass
            else:
                self.find_possible_pit(x,y,'right') #pit is right of player

            if (self.mapping[x][y] == 'Breeze' and ((self.mapping[x-2][y]) or (self.mapping[x+1][y+1]) or (self.mapping[x-1][y-1])) == 'Breeze'):
                self.mapping[x-1][y] = 'Pit' #player is on right side of pit
                self.pit_spaces.add((x-1,y))
                try:
                    self.possible_pits.remove((x-1,y))
                except ValueError:
                    pass
            else:
                self.find_possible_pit(x,y,'left') #pit is left of player

            if (self.mapping[x][y] == 'Breeze' and ((self.mapping[x][y-2]) or (self.mapping[x+1][y-1]) or (self.mapping[x-1][y-1])) == 'Breeze'):
                self.mapping[x][y-1] = 'Pit' #player is above pit
                self.pit_spaces.add((x,y-1))
                try:
                    self.possible_pits.remove((x,y-1))
                except ValueError:
                    pass
            else:
                self.find_possible_pit(x,y,'down') #pit below player

            if (self.mapping[x][y] == 'Breeze' and ((self.mapping[x][y+2]) or (self.mapping[x-1][y+1]) or (self.mapping[x+1][y+1])) == 'Breeze'):
                self.mapping[x][y+1] = 'Pit' #player is below pit
                self.pit_spaces.add((x,y+1))
                try:
                    self.possible_pits.remove((x,y+1))
                except ValueError:
                    pass
            else:
                self.find_possible_pit(x,y,'up') #pit is above player
        except IndexError:
            pass

    def find_possible_pit(self,x,y,possible_pit_loc):
        if possible_pit_loc == 'right':
            if (x + 1) != 4:
                if self.mapping[x+1][y] == 'NotVisited':
                    self.mapping[x+1][y] = 'P?'
                    self.possible_pits.append((x+1,y))
        if possible_pit_loc == 'left':
            if (x - 1) != -1:
                if self.mapping[x-1][y] == 'NotVisited':
                    self.mapping[x-1][y] = 'P?'
                    self.possible_pits.append((x-1,y))
        if possible_pit_loc == 'down':
            if (y - 1) != -1:
                if self.mapping[x][y-1] == 'NotVisited':
                    self.mapping[x][y-1] = 'P?'
                    self.possible_pits.append((x,y-1))
        if possible_pit_loc == 'up':
            if (y + 1) != 4:
                if self.mapping[x][y+1] == 'NotVisited':
                    self.mapping[x][y+1] = 'P?'
                    self.possible_pits.append((x,y+1))

        #If one possible pit detected then it must be a pit
        if len(self.possible_pits) == 1:
            loc = self.possible_pits[0]
            self.pit_spaces.add((loc[0],loc[1]))
            self.possible_pits.remove(loc)
            self.mapping[loc[0]][loc[1]] = 'Pit'

    def find_wumpus(self,loc):
        x = loc[0]
        y = loc[1]

        if (loc[0] - 1) != -1:
            self.possible_wumpus.add((x-1, y))
            if self.mapping[x-1][y] == 'NotVisited':
                self.mapping[x-1][y] = 'W?'
        if (loc[0] + 1) != 4:
            self.possible_wumpus.add((x+1, y))
            if self.mapping[x+1][y] == 'NotVisited':
                self.mapping[x+1][y] = 'W?'
        if (loc[1] - 1) != -1:
            self.possible_wumpus.add((x,y-1))
            if self.mapping[x][y-1] == 'NotVisited':
                self.mapping[x][y-1] = 'W?'
        if (loc[1] + 1) != 4:
            self.possible_wumpus.add((x,y+1))
            if self.mapping[x][y+1] == 'NotVisited':
                self.mapping[x][y+1] = 'W?'

        #wumpus can't be in a pit
        for pit in self.pit_spaces:
            if pit in self.possible_wumpus:
                self.possible_wumpus.remove(pit)
                self.mapping[pit[0]][pit[1]] = 'Pit'
        for safe in self.safe_spaces:
            if safe in self.possible_wumpus:
                self.possible_wumpus.remove(safe)
                self.mapping[safe[0]][safe[1]] = 'Safe'

        #If one possible wumpus detected then it must be a wumpus
        if len(self.possible_wumpus) == 1:
            li = list(self.possible_wumpus)
            loc = li[0]
            self.wumpus_space.append((loc[0],loc[1]))
            self.mapping[loc[0]][loc[1]] = 'Wumpus'
            for space in self.stench_spaces:
                self.mapping[space[0]][space[1]] = 'Safe'
                self.safe_spaces.add((space[0],space[1]))
            self.possible_wumpus.clear()


    def no_wumpus_at(self,loc, player_dir):
        x = loc[0]
        y = loc[1]
        if player_dir == 'Up':
            remove_loc = (x,y+1)
        elif player_dir == 'Down':
            remove_loc = (x,y-1)
        elif player_dir == 'Right':
            remove_loc = (x+1,y)
        elif player_dir == 'Left':
            remove_loc = (x-1,y)

        if remove_loc in self.possible_wumpus:
            self.possible_wumpus.remove(remove_loc)
            self.mapping[remove_loc[0]][remove_loc[1]] = 'Safe'
        self.safe_spaces.add(remove_loc)

    def wumpus_is_dead(self):
        self.safe_spaces.update(self.stench_spaces)
        self.safe_spaces.update(self.possible_wumpus)
        self.stench_spaces.clear()
        self.possible_wumpus.clear()

        for loc in self.safe_spaces:
            x = loc[0]
            y = loc[1]
            self.mapping[x][y] = 'Safe'

    def grab_for_gold(self, loc):
        self.have_gold = True
        self.safe_spaces.add(loc)
        self.mapping[loc[0]][loc[1]] = 'Gold'
        return 'Grab'

class mconner_ExplorerAgent(ExplorerAgent):

    def __init__(self):
        super().__init__()
        self.kb = KB()
        self.start_space = (0,0)
        self.current_space = (0,0)
        self.previous_space = (0,0)
        self.future_actions = []
        self.move_count = 0
        self.max_move_count = 100

    def program(self, percept):
        stench_percept = False
        breeze_percept = False
        glitter_percept = False
        bump_percept = False
        scream_percept = False
        self.kb.finish_space = self.start_space

        #label start space as safe space
        action = 'Forward' #default action

        #if self.move_count >= self.max_move_count:
        #    return 'Quit'
        #Check and do future actions before anything else
        if len(self.future_actions) > 0:
            action = self.future_actions.pop(0)
            if action == 'Forward':
                self.update_player_loc()
        #    self.move_count += 1
            return action

        #check things in percept to determine which one to do first
        none_counter = 0 #counts number of None in percept
        for element in percept:
            if element  == 'Stench':
                stench_percept = True
            elif element == 'Breeze':
                breeze_percept = True
            elif element == 'Glitter':
                glitter_percept = True
            elif element == 'Bump':
                bump_percept = True
            elif element == 'Scream':
                scream_percept = True
            else:
                none_counter += 1


        #Goes to notVisited or safe spot if player doesn't have gold
        if (none_counter == 5) and (self.kb.have_gold == False):
            if self.start_space not in self.kb.safe_spaces:
                self.kb.safe_space_detected_at(self.start_space)

            self.kb.safe_space_detected_at(self.current_space)
            notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
            if notVisited_space_is_neighbor == False:
                self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
            action = self.future_actions.pop(0)
            if action == 'Forward':
                self.update_player_loc()
            #self.move_count += 1
            return action

        #Glitter detected
        if glitter_percept:
            action = self.kb.grab_for_gold(self.current_space)
            self.current_space = self.previous_space
            return action

        #Bump detected
        elif bump_percept and self.kb.have_gold == False:
            self.kb.bump_detected_at(self.current_space, self._facing_direction)
            #Climb if I'm trapped
            if ((self.current_space == self.start_space) and (self.kb.mapping[self.current_space[0]+1][self.current_space[1]] and self.kb.mapping[self.current_space[0]][self.current_space[1]+1])) == 'Wall':
                return 'Climb'
            elif self.current_space == self.start_space:
                return 'Climb'
            
            self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
            #pick notVisited spot if there's no safe spot
            if len(self.future_actions) == 0:
                notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
                action = self.future_actions.pop(0)
            else:
                action = self.future_actions.pop(0)
            if action == 'Forward':
                self.update_player_loc()
            #self.move_count += 1
            return action

        #Stench Only
        elif stench_percept and len(self._holding) >=1 and(breeze_percept and glitter_percept and bumb_percept and scream_percept) == False:
            self.kb.stentch_detected_at(self.current_space)
            self.kb.find_wumpus(self.current_space)
            if len(self._holding) >= 1:
                action = 'Shoot'
            else:
                self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
                #pick notVisited spot if there's no safe spot
                if len(self.future_actions) == 0:
                    notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
                    action = self.future_actions.pop(0)
                else:
                    action = 'Forward'
                if action == 'Forward':
                    self.update_player_loc()
                #self.move_count += 1
            return action

        #Wumpus dies
        elif stench_percept == False and scream_percept and self.kb.have_gold == False:
            self.kb.wumpus_is_dead()
            action = 'Forward'
            self.update_player_loc()
            #self.move_count += 1
            return action

        #Shot arrow and Wumpus still alive
        elif stench_percept and (len(self._holding) < 1 and scream_percept == False):
            self.kb.no_wumpus_at(self.current_space, self._facing_direction)
            notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
            if notVisited_space_is_neighbor == False:
                self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
                action = self.future_actions.pop(0)
            else:
                action = self.future_actions.pop(0)
            if action == 'Forward':
                self.update_player_loc()
            #self.move_count += 1
            return action

        #Breeze only
        elif breeze_percept and (stench_percept and glitter_percept and bumb_percept and scream_percept) == False:
            already_detected = self.kb.breeze_detected_at(self.current_space)
            #Leave if breeze is at start space
            if self.kb.mapping[0][0] == 'Breeze':
                return 'Climb'

            if already_detected == False:
                self.kb.find_pit(self.current_space)
                notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
                if notVisited_space_is_neighbor == False:
                    self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
                    #action = self.future_actions.pop(0)
                #else:
                action = self.future_actions.pop(0)
                if action == 'Forward':
                    self.update_player_loc()
                    #self.move_count += 1
            else:
                notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
                if notVisited_space_is_neighbor == False:
                    self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
                   # action = self.future_actions.pop(0)
                #else:
                action = self.future_actions.pop(0)
            if action == 'Forward':
                self.update_player_loc()
            #self.move_count += 1
            return action

        #Breeze and stench in same space
        elif breeze_percept and stench_percept:
            self.kb.breeze_detected_at(self.current_space)
            self.kb.find_pit(self.current_space)
            self.kb.stentch_detected_at(self.current_space)
            self.kb.find_wumpus(self.current_space)
            if len(self._holding >= 1):
                action = 'Shoot'
            else:
                self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
                if len(self.future_actions) == 0:
                    notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
                    action = self.future_actions.pop(0)
                else:
                    action = self.future_actions.pop(0)
                if action == 'Forward':
                    self.update_player_loc()
                #self.move_count += 1
            return action
                
        #Check if in finish space with gold
        elif self.kb.have_gold == True:
            self.kb.find_spaces_home(self.current_space, self._facing_direction, self.future_actions)
            try:
                action = self.future_actions.pop(0)
            except IndexError:
                pass
            else:
                action = 'Forward'
            if action == 'Forward':
                self.update_player_loc()
            #self.move_count += 1

            if self.current_space == self.start_space:
                return 'Climb'
            else:
                return action

        else:
            notVisited_space_is_neighbor = self.kb.find_notVisited_space(self.current_space, self._facing_direction, self.future_actions)
            if notVisited_space_is_neighbor == False:
                self.kb.find_safe_space(self.current_space, self._facing_direction, self.future_actions)
            action = self.future_actions.pop(0)
            if action == 'Forward':
                self.update_player_loc()
            #self.move_count += 1            
            return action


    def update_player_loc(self):
        #updates location of player
        #print("c ", self.current_space)
        #print('p ', self.previous_space)
        x = self.current_space[0]
        y = self.current_space[1]
        self.previous_space = self.current_space
        if self._facing_direction == 'Up' and (y < 3):
                self.current_space = (x,y+1)
        elif self._facing_direction == 'Down' and (y > 0):
                self.current_space = (x,y-1)
        elif self._facing_direction == 'Right' and (x < 3):
                self.current_space = (x+1,y)
        elif self._facing_direction == 'Left' and (x > 0):
                self.current_space = (x-1,y)
        else:
            self.current_space = (x,y) #hit border