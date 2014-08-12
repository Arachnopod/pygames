"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level

Author: John Liu
Date: 2014-05-Jul
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """    
    
    values = [0] * max(hand)
    for dummy_idx in hand:
        values[dummy_idx-1] += dummy_idx
            
    return max(values)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    die_avg = 0.
    possible_free = gen_all_sequences(range(1,num_die_sides+1), num_free_dice)
    
    for seq in possible_free:
        die_avg += score(held_dice + seq)
    
    die_avg /= len(possible_free)
                         
    return die_avg


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    length = len(hand)
    for dummy_idx in range(length):
        temp_set = set()
        for partial_seq in answer_set:
            if len(partial_seq) < 1:
                min_idx = 0
            else:
                min_idx = partial_seq[-1]
            for item in range(min_idx,length):
                if item not in partial_seq:
                    new_sequence = list(partial_seq)
                    new_sequence.append(item)
                    temp_set.add(tuple(new_sequence))
        answer_set = answer_set.union(temp_set)
    
    my_set = set([()])
    for dummy_idx in answer_set:
        temp_seq = []
        for dummy_y in dummy_idx:
            temp_seq.append(hand[dummy_y])
        my_set.add(tuple(temp_seq))
        
    return my_set



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    answer = [0,()]
    answer_set = gen_all_holds(hand)

    for each_answer in answer_set:
        value = expected_value(each_answer,num_die_sides,len(hand)-len(each_answer))
        if value >= answer[0]:
            answer[0] = value
            answer[1] = each_answer
   
    return tuple(answer)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
                                   
run_example()

#print strategy((1,), 6)
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    



