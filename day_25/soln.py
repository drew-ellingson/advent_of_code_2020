import math 

class Hand():
    DIV_NUM = 20201227
    INIT_SUBJ_NUM = 7

    def __init__(self, public_key):
        self.public_key = public_key 
        self.loop_size = self.get_loop_size()

    @staticmethod
    def trans_one(val, subj_num):
        return (val * subj_num) % Hand.DIV_NUM

    @staticmethod
    def trans_many(val, subj_num, num):
        bin_num = [int(i) for i in bin(num)[2:]]
        val_squares = [subj_num]
        for i in range(len(bin_num) - 1):
            val_squares.append((val_squares[-1] ** 2) % Hand.DIV_NUM)
  
        bin_decomp = list(map(lambda x: x[0] * x[1], zip(bin_num, reversed(val_squares))))
        return math.prod([x for x in bin_decomp if x != 0]) % Hand.DIV_NUM


    def get_loop_size(self):
        done = False
        i, val = 0, 1
        while not done:
            val = self.trans_one(val, Hand.INIT_SUBJ_NUM)
            i += 1
            if val == self.public_key:
                return i 

def get_encryption_key(hand_1, hand_2):
    return hand_2.trans_many(1, hand_1.public_key, hand_2.loop_size)

if __name__ == '__main__':
    my_input = [2959251, 4542595]
    # my_input = [5764801, 17807724]
    card = Hand(my_input[0])
    door = Hand(my_input[1])

    print(card.get_loop_size())
    print(door.get_loop_size())

    print(get_encryption_key(card, door))
