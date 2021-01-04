import cProfile 
import pstats 

class CupGame():
    def __init__(self, cup_list):
        self.cup_list = cup_list
        self.curr_cup_indx = 0
        self.cup_list_len = len(cup_list)

    def play_round(self):
        curr_cup_val = self.cup_list[self.curr_cup_indx]
        pickup = self.cup_list[self.curr_cup_indx+1:self.curr_cup_indx+4]
        pickup_wraps = False
        if len(pickup) < 3:
            pickup_wraps = True
            add_chars = 3 - len(pickup)
            pickup.extend(self.cup_list[:add_chars])
        
        # hacky
        if curr_cup_val - 1 not in pickup and curr_cup_val - 1 > 0:
            dest_val = curr_cup_val - 1
        elif curr_cup_val - 2 not in pickup and curr_cup_val - 2 > 0:
            dest_val = curr_cup_val - 2
        elif curr_cup_val - 3 not in pickup and curr_cup_val - 3 > 0:
            dest_val = curr_cup_val - 3
        else:
            dest_val = max([x for x in self.cup_list if x not in pickup]) # should be accessed rarely

        [self.cup_list.remove(x) for x in pickup]
        
        dest_indx = self.cup_list.index(dest_val) # this is the slowstep

        [self.cup_list.insert(dest_indx + 1, x) for x in reversed(pickup)]

        if not pickup_wraps:
            if dest_indx < self.curr_cup_indx:
                self.curr_cup_indx += 3
        else:
            self.curr_cup_indx = self.cup_list.index(curr_cup_val) # should happen rarely

        self.curr_cup_indx = (self.curr_cup_indx + 1) % self.cup_list_len
    
    def play_game(self, rounds):
        for x in range(rounds):
            if x % 1000 == 0:
                print(f'{x} out of {rounds} completed for {round(100 * x / rounds,2)}%')
            self.play_round()
            # input('press enter')

    def get_string_rep(self, start_val):
        start_indx = self.cup_list.index(start_val)
        order_cups = self.cup_list[start_indx+1:] + self.cup_list[:start_indx]
        return ''.join([str(x) for x in order_cups])

        
    def get_star_cups(self, start_val):
        start_indx = self.cup_list.index(start_val)
        order_cups = self.cup_list[start_indx+1:] + self.cup_list[:start_indx]
        return order_cups[0] * order_cups[1]



if __name__ == '__main__':
    raw_in = '942387615'
    # raw_in = '389125467'

    my_input = [int(x) for x in raw_in]
    cup_game = CupGame(my_input)
    cup_game.play_game(100)
    print(f'P1 Answer: {cup_game.get_string_rep(1)}')

    long_game = list(range(1000000))
    long_game[0:len(my_input)] = my_input
    
    cup_game = CupGame(long_game)
    
    # was profiling smaller cases to optimize
    # slowstep is a list.index() i can't remove \_(*_*)_/

    profile = cProfile.Profile()    
    profile.runcall(cup_game.play_game, 10000000)
    ps = pstats.Stats(profile)
    ps.print_stats()

    print(f'P2 Answer: {cup_game.get_star_cups(1)}')
    