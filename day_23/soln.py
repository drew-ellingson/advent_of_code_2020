import copy

class CupGame():    
    # relying on unique cup labels throughout
    def __init__(self, cup_list):
        self.cup_list = cup_list
        self.curr_cup_indx = 0
        self.curr_cup_val = cup_list[0]

    def play_round(self, verbose=False):
        curr_cup_list = self.cup_list
        
        if self.curr_cup_indx + 4 <= len(curr_cup_list): 
            pickup = self.cup_list[self.curr_cup_indx+1:self.curr_cup_indx+4]
        else:
            pickup_p1 = self.cup_list[self.curr_cup_indx:]
            pickup_p1.remove(self.curr_cup_val)
            pickup_p2 = self.cup_list[: 3-len(pickup_p1)]
            pickup = pickup_p1 + pickup_p2
        
        rem_cup_list = [x for x in self.cup_list if x not in pickup]
        
        try:
            dest_indx = max([(i,x) for (i,x) in enumerate(rem_cup_list) if x < self.curr_cup_val], key=lambda k: k[1])[0]
        except ValueError:
            dest_indx = max(enumerate(rem_cup_list), key = lambda k: k[1])[0]
         
        try:
            new_cup_list = rem_cup_list[:dest_indx+1] + pickup + rem_cup_list[dest_indx+1:]
        except IndexError:  # dest indx is last in list
            new_cup_list = pickup + rem_cup_list
        
        self.cup_list = new_cup_list 

        curr_cup_indx = self.cup_list.index(self.curr_cup_val)
        self.curr_cup_indx = (curr_cup_indx + 1) % len(self.cup_list)
        self.curr_cup_val = self.cup_list[self.curr_cup_indx]

        if verbose:
            print(f'\tcurr cup list: {curr_cup_list}')
            print(f'\tpickup: {pickup}')
            print(f'\tdest index and val: {dest_indx}, {rem_cup_list[dest_indx]}')
            print(f'\tnew cup list: {new_cup_list}')
            print(f'\tcurr cup indx and val: {self.curr_cup_indx}, {self.curr_cup_val}')
            print('\n')
    
    def play_game(self, rounds, verbose=False):
        for x in range(rounds):
            if verbose:
                print(f'Round {x+1}')
            if x % 1000 == 0:
                print(f'{x} out of {rounds} completed for {round(100 * x / rounds,2)}%')
            self.play_round(verbose=verbose)

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
    cup_game.play_game(100, verbose=True)
    print(f'P1 Answer: {cup_game.get_string_rep(1)}')

    long_game = list(range(1000000))
    long_game[0:len(my_input)] = my_input
    
    cup_game = CupGame(long_game)
    cup_game.play_game(10000000)
    print(f'P2 Answer: {cup_game.get_star_cups(1)}')
    