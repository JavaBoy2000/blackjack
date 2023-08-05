import random
import matplotlib.pyplot as plt
import numpy as np
import time
import math

start_time = time.time()

'''
def generate_shoe(deck_count): # for later if you need it
    cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    shoe = cards * 4 * deck_count
    random.shuffle(shoe)
    return shoe

def generate_player_hand(shoe):
    players_hand = [shoe.pop(0), shoe.pop(0)]
    return players_hand
'''

def print_hand(hand):
    str_hand = ""
    for card in hand:
        str_hand += str(card)
        str_hand += " "
        #print(card, end = ' ')
    return str_hand.rstrip()

def count_update(curr_hand):
    curr_hand_count = 0
    for card in curr_hand:
        if card in [2, 3, 4, 5, 6]:
            curr_hand_count += 1
    for card in curr_hand:
        if card in [7, 8, 9]:
            curr_hand_count += 0
    for card in curr_hand:
        if card in [10, "A"]:
            curr_hand_count -= 1
    return curr_hand_count

def true_count_converter(true_count):
    if true_count < 0:
        #print("true_count: " + str(true_count))
        true_count = math.ceil(true_count)
        #print("true_count ceiled: " + str(true_count))
    elif true_count >= 0:
        #print("true_count: " + str(true_count))
        true_count = math.floor(true_count)
        #print("true_count floored: " + str(true_count))
    return true_count

def ace_converter(players_hand):
    if "A" not in players_hand: # hard hand check
        hand_total = sum(players_hand)
        return {"hand_total" : hand_total, "sorted_players_hand" : players_hand}

    if players_hand == ["A", 10] or players_hand == [10, "A"]:
        hand_total = 21
        players_hand = [{"A" : 11}, 10]
        return {"hand_total" : hand_total, "sorted_players_hand" : players_hand}

    int_list = []
    for card in players_hand:
        if type(card) != str: # checks card isn't "A"
            int_list.append(card) # appends non-"A" cards
    sorted_players_hand = (["A"] * players_hand.count("A")) + int_list

    if "A" in sorted_players_hand:
        for i in range(0, len(sorted_players_hand)):
            if sorted_players_hand[i] == "A":
                sorted_players_hand[i] = {"A" : 11}
        hand_total = 0
        ace_as_11 = 0
        for element in sorted_players_hand:
            if type(element) == dict:
                hand_total += element["A"]
                ace_as_11 += 1
            else:
                hand_total += element # adds remaining integers at end of list
        if hand_total > 21 and ace_as_11 >= 2:
            for i in range(0, len(sorted_players_hand)):
                if type(sorted_players_hand[i]) == dict and ace_as_11 >= 2:
                    sorted_players_hand[i] = {"A" : 1}
                    ace_as_11 -= 1
            hand_total = 0
            for element in sorted_players_hand:
                if type(element) == dict:
                    hand_total += element["A"]
                else:
                    hand_total += element
        if sum(int_list) >= 10: # if the sum of non-"A" cards is greater than or equal to 10 all "A" cards must become 1
            # changed from > to >=, this seems to have fixed the A A 10 edge case
            for i in range(0, len(sorted_players_hand)):
                if type(sorted_players_hand[i]) == dict:
                    sorted_players_hand[i] = {"A" : 1}
            hand_total = 0
            for element in sorted_players_hand:
                if type(element) == dict:
                    hand_total += element["A"]
                else:
                    hand_total += element
        #print(sorted_players_hand)
        #print("hand_total: " + str(hand_total))
    return {"hand_total" : hand_total, "sorted_players_hand" : sorted_players_hand}

def soft_hand_check(pre_converted_players_hand):
    converted_players_hand = ace_converter(pre_converted_players_hand)["sorted_players_hand"]
    num_dict = 0
    for element in converted_players_hand:
        if type(element) == dict: # if an element is a dict it's an ace
            num_dict += 1
    if num_dict == 0: # no aces
        #print(pre_converted_players_hand)
        #print("hard " + str(sum(converted_players_hand)))
        return False
    if num_dict == 1 and len(converted_players_hand) == 2: # regular soft pair i.e. ["A", 9]
        #print("soft " + str(ace_converter(pre_converted_players_hand)["hand_total"]))
        return True
    num_dicts = 0
    num_ones = 0
    for element in converted_players_hand:
        if type(element) == dict:
            num_dicts += 1
            if element["A"] == 1:
                num_ones += 1
    if num_ones == num_dicts: # all "A" in hand are 1 so hand is hard
        #print(pre_converted_players_hand)
        #print("hard " + str(ace_converter(pre_converted_players_hand)["hand_total"]))
        return False
    else: # one "A" is an 11 so the hand is soft
        #print(pre_converted_players_hand)
        #print("soft " + str(ace_converter(pre_converted_players_hand)["hand_total"]))
        return True

# "Y" : Split the Pair
# "Y/N" : Split if "Double After Split (DAS)" is offered, otherwise don't split
# "N" : Don't Split the Pair
# "H" : Hit
# "S" : Stand
# "D" : Double if allowed, otherwise hit
# "Ds" : Double if allowed, otherwise stand
# "SUR" : Surrender

DAS_boolean = True # make this into input later
def basic_strategy(players_hand, dealers_hand, true_count): # implement to turn off LS here
    dealer_upcard = dealers_hand[0]
    # implement some house rules for doubling down here
    if len(players_hand) == 2:
        DAS_boolean = True
    else:
        DAS_boolean = False
    # I think we have to make a 21 case here too, I don't think so. Look at this later
    # Gotta be an easier way to do this
    if ace_converter(players_hand)["hand_total"] == 21 and soft_hand_check(players_hand) and len(players_hand) == 2:
        #print("Blackjack!")
        return "S"
    if ace_converter(players_hand)["hand_total"] == 21 and soft_hand_check(players_hand) and len(players_hand) != 2: # (2 3 5 A)
        #print("soft 21 but not blackjack")
        return "S"
    if ace_converter(players_hand)["hand_total"] == 21 and not soft_hand_check(players_hand) and len(players_hand) != 2:
        #print("hard 21 not blackjack!")
        return "S"
    if players_hand == ["A", "A"]: # aces only get one card dealt after splitting and no resplitting
        return "Y"
    if players_hand == [10, 10]:
        return "S"
    if players_hand == [9, 9]:
        if dealer_upcard in [7, 10, "A"]:
            return "S"
        else:
            return "Y"
    if players_hand == [8, 8]:
        return "Y"
    if players_hand == [7, 7]:
        if dealer_upcard in [2, 3, 4, 5, 6, 7]:
            return "Y"
        else:
            return "H"
    if players_hand == [6, 6]:
        if dealer_upcard == 2 and DAS_boolean:
            return "Y"
        if dealer_upcard in [3, 4, 5, 6]:
            return "Y"
        else:
            return "H"
    if players_hand == [4, 4]:
        if dealer_upcard in [5, 6] and DAS_boolean:
            return "Y"
        else:
            return "H"
    if players_hand == [3, 3] or players_hand == [2, 2]:
        if dealer_upcard in [2, 3] and DAS_boolean:
            return "Y"
        if dealer_upcard in [4, 5, 6, 7]:
            return "Y"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 20 and soft_hand_check(players_hand):
        return "S"
    if ace_converter(players_hand)["hand_total"] == 19 and soft_hand_check(players_hand):
        if dealer_upcard == 4 and DAS_boolean and true_count >= 3: # deviation
            return "D"
        if dealer_upcard == 5 and DAS_boolean and true_count >= 1: # deviation
            return "D"
        if dealer_upcard == 6 and true_count > 0: # deviation
            return "S"
        if dealer_upcard == 6 and DAS_boolean:
            return "D"
        else:
            return "S"
    if ace_converter(players_hand)["hand_total"] == 18 and soft_hand_check(players_hand):
        if dealer_upcard in [2, 3, 4, 5, 6] and DAS_boolean:
            return "D"
        else:
            return "S"
        if dealer_upcard in [7, 8]:
            return "S"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 17 and soft_hand_check(players_hand):
        if dealer_upcard in [3, 4, 5, 6] and DAS_boolean:
            return "D"
        if dealer_upcard == 2 and DAS_boolean and true_count >= 1: # deviation
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 16 and soft_hand_check(players_hand):
        if dealer_upcard in [4, 5, 6] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 15 and soft_hand_check(players_hand):
        if dealer_upcard in [4, 5, 6] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 14 and soft_hand_check(players_hand):
        if dealer_upcard in [5, 6] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 13 and soft_hand_check(players_hand):
        if dealer_upcard in [5, 6] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] >= 17 and not soft_hand_check(players_hand):
        return "S"
    if ace_converter(players_hand)["hand_total"] == 16 and not soft_hand_check(players_hand):
        if dealer_upcard == 9 and true_count >= 4: # deviation
            return "S"
        if dealer_upcard == 10 and true_count > 0: # deviation
            return "S"
        if dealer_upcard == "A" and true_count >= 3: # deviation
            return "S"
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        if dealer_upcard in [9, 10, "A"] and len(players_hand) == 2:
            return "H" # change back to SUR
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 15 and not soft_hand_check(players_hand):
        if dealer_upcard == 10 and true_count >= 4: # deviation
            return "S"
        if dealer_upcard == "A" and true_count >= 5: # deviation
            return "S"
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        if dealer_upcard in [10] and len(players_hand) == 2:
            return "H" # change back to SUR
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 14 and not soft_hand_check(players_hand):
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 13 and not soft_hand_check(players_hand):
        if dealer_upcard == 2 and true_count <= -1:
            return "H"
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 12 and not soft_hand_check(players_hand):
        if dealer_upcard == 2 and true_count >= 3:
            return "S"
        if dealer_upcard == 3 and true_count >= 2:
            return "S"
        if dealer_upcard == 4 and true_count < 0:
            return "H"
        if dealer_upcard in [4, 5, 6]:
            return "S"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 11 and not soft_hand_check(players_hand):
        if DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 10 and not soft_hand_check(players_hand):
        if dealer_upcard == 10 and true_count >= 4 and DAS_boolean:
            return "D"
        if dealer_upcard == "A" and true_count >= 3 and DAS_boolean:
            return "D"
        if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 9 and not soft_hand_check(players_hand):
        if dealer_upcard == 2 and true_count >= 1 and DAS_boolean:
            return "D"
        if dealer_upcard == 7 and true_count >= 3 and DAS_boolean:
            return "D"
        if dealer_upcard in [3, 4, 5, 6] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 8 and not soft_hand_check(players_hand):
        if dealer_upcard == 6 and true_count >= 2 and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] < 8 and not soft_hand_check(players_hand):
        return "H"



def play_dealer(dealers_hand, player_bust, late_surrender_boolean, player_blackjack_boolean, shoe, count, deck_count, dict_count_frequency):
    dealer_blackjack_boolean = False
    dealer_bust = False
    # insurance_check = False # might need this later
    dealer_upcard = dealers_hand[0]
    #print("soft_hand_check(" + str(print_hand(dealers_hand)) + "): " + str(soft_hand_check(dealers_hand)))
    decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
    cards_remaining = len(shoe)
    true_count = count / decks_remaining
    true_count = true_count_converter(true_count)
    #print()
    #print("dealers_hand: " + str(print_hand(dealers_hand)))
    #print("running_count received at start of play_dealer: " + str(count))
    #print("decks_remaining at start of play_dealer: " + str(decks_remaining))
    #print("cards_remaining at start of play_dealer: " + str(cards_remaining))
    #print("true_count calculated at start of play_dealer: " + str(true_count))
    if player_bust or late_surrender_boolean or player_blackjack_boolean:
        return {
                    "dealers_hand" : dealers_hand ,
                    "dealer_bust" : dealer_bust ,
                    "shoe" : shoe ,
                    "count" : count ,
                    "true_count" : true_count ,
                    "dict_count_frequency" : dict_count_frequency
                } # end dealer stuff
    if soft_hand_check(dealers_hand): # hand is soft so hit cause H17
        #print("dealers_hand: " + str(print_hand(dealers_hand)))
        #print("dealer has a soft " + str(ace_converter(dealers_hand)["hand_total"]))
        if ace_converter(dealers_hand)["hand_total"] == 21 and len(dealers_hand) == 2:
            #print("dealer has blackjack")
            dealer_blackjack_boolean = True # return this
        while ace_converter(dealers_hand)["hand_total"] <= 17:
            #print("dealer hits with (" + str(print_hand(dealers_hand)) + "), a soft " + str(ace_converter(dealers_hand)["hand_total"]))
            card = shoe.pop(0)
            dealers_hand.append(card)
            count += count_update([card])
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            cards_remaining = len(shoe)
            true_count = count / decks_remaining
            true_count = true_count_converter(true_count)
            dict_count_frequency[true_count] += 1
            #print("dealers_hand: " + str(print_hand(dealers_hand)))
            #print("running_count in soft_hand_check of play_dealer: " + str(count))
            #print("decks_remaining in soft_hand_check of play_dealer: " + str(decks_remaining))
            #print("cards_remaining in soft_hand_check of play_dealer: " + str(cards_remaining))
            #print("true_count calculated in soft_hand_check of play_dealer: " + str(true_count))
            if soft_hand_check(dealers_hand):
                continue
            else:
                break
        #if ace_converter(dealers_hand)["hand_total"] > 17: # maybe check that it is lower than 22 too?
            #print("dealer stands with (" + str(print_hand(dealers_hand)) + "), a soft " + str(ace_converter(dealers_hand)["hand_total"]))
    if not soft_hand_check(dealers_hand): # hand is hard so stop at 17
        #print("dealers_hand: " + str(print_hand(dealers_hand)))
        #print("dealer has a hard " + str(ace_converter(dealers_hand)["hand_total"]))
        #if ace_converter(dealers_hand)["hand_total"] >= 17 and len(dealers_hand) == 2: # i.e a (10 8) or (9 8) etc.
            #print("dealer stands on " + str(ace_converter(dealers_hand)["hand_total"]))
        while ace_converter(dealers_hand)["hand_total"] <= 16: # i.e. a (10 5) etc.
            #print("dealer hits with (" + str(print_hand(dealers_hand)) + "), a hard " + str(ace_converter(dealers_hand)["hand_total"]))
            card = shoe.pop(0)
            #print("card: " + str(card))
            dealers_hand.append(card)
            count += count_update([card])
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            cards_remaining = len(shoe)
            true_count = count / decks_remaining
            true_count = true_count_converter(true_count)
            dict_count_frequency[true_count] += 1
            #print("dealers_hand: " + str(print_hand(dealers_hand)))
            #print("running_count in not soft_hand_check of play_dealer: " + str(count))
            #print("decks_remaining in not soft_hand_check of play_dealer: " + str(decks_remaining))
            #print("cards_remaining in not soft_hand_check of play_dealer: " + str(cards_remaining))
            #print("true_count calculated in not soft_hand_check of play_dealer: " + str(true_count))
            #print("dealer has (" + str(print_hand(dealers_hand)) + "), a hard " + str(ace_converter(dealers_hand)["hand_total"]))
            if ace_converter(dealers_hand)["hand_total"] > 21:
                #print("dealer busts with (" + str(print_hand(dealers_hand)) + "), a hard " + str(ace_converter(dealers_hand)["hand_total"]))
                dealer_bust = True # return this
                break
            if ace_converter(dealers_hand)["hand_total"] >= 17:
                #print("dealer stands with (" + str(print_hand(dealers_hand)) + "), a hard " + str(ace_converter(dealers_hand)["hand_total"]))
                break
    return {
                "dealers_hand" : dealers_hand ,
                "dealer_bust" : dealer_bust ,
                "shoe" : shoe ,
                "count" : count ,
                "true_count" : true_count ,
                "dict_count_frequency" : dict_count_frequency
            } # end dealer stuff

def play_player(shoe, count, deck_count, dict_count_frequency):
    players_hand = [shoe.pop(0), shoe.pop(0)]
    count += count_update(players_hand)
    dealers_hand = [shoe.pop(0), shoe.pop(0)]
    count += count_update(dealers_hand)
    decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
    cards_remaining = len(shoe)
    true_count = count / decks_remaining
    true_count = true_count_converter(true_count)
    #print("players_hand: " + str(print_hand(players_hand)))
    #print("dealers_hand: " + str(print_hand(dealers_hand)))
    #print("running_count at start of play_player: " + str(count))
    #print("decks_remaining at start of play_player: " + str(decks_remaining))
    #print("cards_remaining at start of play_player: " + str(cards_remaining))
    #print("true_count calculated at start of play_player: " + str(true_count))
    dict_count_frequency[true_count] += 1
    dealer_upcard = dealers_hand[0]
    player_bust = False
    late_surrender_boolean = False
    player_blackjack_boolean = False
    dealer_blackjack_boolean = False
    double_boolean = False
    split_boolean = False
    ace_split_boolean = False
    #if dealer_upcard == "A":
        #print("Dealer: Would you like insurance")
        #print("Player: No, unless the true count is +3 or higher")
    while ace_converter(players_hand)["hand_total"] <= 21: # player
        if players_hand == ["A", 10] or players_hand == [10, "A"]:
            player_blackjack_boolean = True
            #print("player has blackjack")
            break
        if dealers_hand == ["A", 10] or dealers_hand == [10, "A"]:
            dealer_blackjack_boolean = True
            #print("dealer has blackjack")
            break
        if basic_strategy(players_hand, dealers_hand, true_count) == "SUR":
            late_surrender_boolean = True
            break
        if basic_strategy(players_hand, dealers_hand, true_count) == "Y":
            split_boolean = True
            break
        if basic_strategy(players_hand, dealers_hand, true_count) == "H":
            #print("You hit with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            card = shoe.pop(0)
            players_hand.append(card)
            count += count_update([card]) # will this work?
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            cards_remaining = len(shoe)
            true_count = count / decks_remaining
            true_count = true_count_converter(true_count)
            dict_count_frequency[true_count] += 1
            #print("players_hand: " + str(print_hand(players_hand)))
            #print("running_count in hitting conditional of play_player: " + str(count))
            #print("decks_remaining in hitting conditional of play_player: " + str(decks_remaining))
            #print("cards_remaining in hitting conditional of play_player: " + str(cards_remaining))
            #print("true_count calculated in hitting conditional of play_player: " + str(true_count))
            #print("players_hand: " + str(print_hand(players_hand)))
            continue # should restart while loop and check while loop condition
        if basic_strategy(players_hand, dealers_hand, true_count) == "S":
            #print("You stand with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            break
        if basic_strategy(players_hand, dealers_hand, true_count) == "D":
            #print("You double with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            double_boolean = True
            card = shoe.pop(0)
            players_hand.append(card)
            count += count_update([card]) # will this work?
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            cards_remaining = len(shoe)
            true_count = count / decks_remaining
            true_count = true_count_converter(true_count)
            dict_count_frequency[true_count] += 1
            #print("players_hand: " + str(print_hand(players_hand)))
            #print("running_count in doubling conditional of play_player: " + str(count))
            #print("decks_remaining in doubling conditional of play_player: " + str(decks_remaining))
            #print("cards_remaining in doubling conditional of play_player: " + str(cards_remaining))
            #print("true_count calculated in doubling conditional of play_player: " + str(true_count))
            break
    if ace_converter(players_hand)["hand_total"] > 21:
        #print("players_hand: " + str(print_hand(players_hand)))
        #print("You have busted with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]))
        player_bust = True
    return {
                "players_hand" : players_hand ,
                "dealers_hand" : dealers_hand ,
                "late_surrender_boolean" : late_surrender_boolean ,
                "player_blackjack_boolean" : player_blackjack_boolean ,
                "dealer_blackjack_boolean" : dealer_blackjack_boolean ,
                "double_boolean" : double_boolean ,
                "split_boolean" : split_boolean ,
                "player_bust" : player_bust ,
                "shoe" : shoe ,
                "count" : count ,
                "decks_remaining" : round(decks_remaining, 5) ,
                "true_count" : true_count ,
                "ace_split_boolean" : ace_split_boolean ,
                "dict_count_frequency" : dict_count_frequency
            }

def split(players_hand, dealers_hand, shoe, count, dict_count_frequency):
    # we can hard code three splits, three splits is usually the max in casinos
    # I don't want to hard code three splits, yeah I know
    dict_a = {}
    double_boolean = False
    player_bust = False
    ace_split_boolean = False
    #count += count_update(dealers_hand) # count gets updated from sim
    decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
    cards_remaining = len(shoe)
    true_count = count / decks_remaining
    true_count = true_count_converter(true_count)
    dict_count_frequency[true_count] += 1
    #print("players_hand in split: " + str(print_hand(players_hand)))
    #print("running_count given to split at start of split: " + str(count))
    #print("decks_remaining at start of split: " + str(decks_remaining))
    #print("cards_remaining at start of split: " + str(cards_remaining))
    #print("true_count calculated at start of split: " + str(true_count))
    if players_hand == ["A", "A"]: # no RSA
        #count += count_update(players_hand) # this gets updated in play_player, nice
        split_players_hand = [[players_hand[0]], [players_hand[1]]]
        #print("in the split function for aces")
        #print(split_players_hand)
        i = 0
        # fix it to where a "natural" doesn't get paid 3:2
        # use boolean that gets returned and then used in play_decision, nice
        for players_hand in split_players_hand:
            card = shoe.pop(0)
            split_players_hand[i].append(card)
            count += count_update([card])
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            cards_remaining = len(shoe)
            true_count = count / decks_remaining
            true_count = true_count_converter(true_count)
            dict_count_frequency[true_count] += 1
            ace_split_boolean = True
            #print("players_hand in ace split: " + str(print_hand(players_hand)))
            #print("running_count in ace split: " + str(count))
            #print("decks_remaining in ace split: " + str(decks_remaining))
            #print("cards_remaining in ace split: " + str(cards_remaining))
            #print("true_count calculated in ace split: " + str(true_count))
            dict_a[i] = {
                            "players_hand" : split_players_hand[i] ,
                            "dealers_hand" : dealers_hand ,
                            "double_boolean" : double_boolean ,
                            "player_bust" : player_bust ,
                            "shoe" : shoe ,
                            "count" : count ,
                            "decks_remaining" : round(decks_remaining, 5) ,
                            "true_count" : true_count ,
                            "ace_split_boolean" : ace_split_boolean ,
                            "dict_count_frequency" : dict_count_frequency
                        }
            i += 1
        return dict_a
    split_players_hand = [[players_hand[0]], [players_hand[1]]] # this is the first hard coded split we can do two more
    num_splits = 1
    #print("You are in the split function")
    #print(split_players_hand)
    i = 0
    #count += count_update(players_hand) # gets updated in play_player
    for players_hand in split_players_hand: # first hard coded split
        card = shoe.pop(0)
        split_players_hand[i].append(card)
        count += count_update([card])
        decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
        cards_remaining = len(shoe)
        true_count = count / decks_remaining
        true_count = true_count_converter(true_count)
        dict_count_frequency[true_count] += 1
        #print("players_hand in first split: " + str(print_hand(players_hand)))
        #print("running_count in first split: " + str(count))
        #print("decks_remaining in first split: " + str(decks_remaining))
        #print("cards_remaining in first split: " + str(cards_remaining))
        #print("true_count calculated in first split: " + str(true_count))
        #print(split_players_hand)
        i += 1
    i = 0
    for players_hand in split_players_hand: # second split, one more
        if basic_strategy(players_hand, dealers_hand, true_count) == "Y":
            num_splits += 1
            #print("You are in the second split")
            split_players_hand_2 = [[split_players_hand[i][0]], [split_players_hand[i][1]]]
            #count += count_update([split_players_hand[i][0]]) # unnecessary because it's updated in the first split
            #print(split_players_hand_2)
            for j in range(0, len(split_players_hand_2)):
                card = shoe.pop(0)
                split_players_hand_2[j].append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                cards_remaining = len(shoe)
                true_count = count / decks_remaining
                true_count = true_count_converter(true_count)
                dict_count_frequency[true_count] += 1
                #print("players_hand in second split: " + str(print_hand(players_hand)))
                #print("running_count in second split: " + str(count))
                #print("decks_remaining in second split: " + str(decks_remaining))
                #print("cards_remaining in second split: " + str(cards_remaining))
                #print("true_count calculated in second split: " + str(true_count))
                #print(split_players_hand_2)
            if i == 0:
                split_players_hand_2.append(split_players_hand[i + 1])
                #print("in the i == 0 conditional of the second split")
                #print(split_players_hand_2)
            if i == 1:
                split_players_hand_2.append(split_players_hand[i - 1])
                #print("in the i == 1 conditional of the second split")
                #print(split_players_hand_2)
            split_players_hand = split_players_hand_2
            break
        i += 1
    #print(split_players_hand)
    #print("num_splits: " + str(num_splits))
    i = 0
    for players_hand in split_players_hand: # third split, no more splits
        # I think this third split splicing for the lists is wrong
        if basic_strategy(split_players_hand[i], dealers_hand, true_count) == "Y":
            num_splits += 1
            #print("You are in the third split")
            split_players_hand_3 = [[split_players_hand[i][0]], [split_players_hand[i][1]]]
            #count += count_update([split_players_hand[i][1]]) # same reason this is commented out in the second split
            #print(split_players_hand_2)
            for j in range(0, len(split_players_hand_3)):
                card = shoe.pop(0)
                split_players_hand_3[j].append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                cards_remaining = len(shoe)
                true_count = count / decks_remaining
                true_count = true_count_converter(true_count)
                dict_count_frequency[true_count] += 1
                #print("players_hand in third split: " + str(print_hand(players_hand)))
                #print("running_count in third split: " + str(count))
                #print("decks_remaining in third split: " + str(decks_remaining))
                #print("cards_remaining in third split: " + str(cards_remaining))
                #print("true_count calculated in third split: " + str(true_count))
                #print(split_players_hand_3)
            if i == 0: # I gotta make sure all these conditionals work properly
                split_players_hand_3.append(split_players_hand[i + 1])
                split_players_hand_3.append(split_players_hand[i + 2])
                #print("in the i == 0 conditional of the third split")
                #print(split_players_hand_3)
            if i == 1:
                split_players_hand_3.append(split_players_hand[i - 1])
                split_players_hand_3.append(split_players_hand[i + 1])
                #print("in the i == 1 conditional of the third split")
                #print(split_players_hand_3)
            if i == 2:
                split_players_hand_3.append(split_players_hand[i - 1])
                split_players_hand_3.append(split_players_hand[i - 2])
                #print("in the i == 2 conditional of the third split")
                #print(split_players_hand_3)
            split_players_hand = split_players_hand_3
            break
        i += 1
    #print(split_players_hand)
    #print("num_splits: " + str(num_splits))
    i = 0
    result = "N/A"
    for players_hand in split_players_hand:
        while ace_converter(players_hand)["hand_total"] <= 21: # player
            #print("You have (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            result = basic_strategy(players_hand, dealers_hand, true_count)
            if num_splits >= 3: # have to do deviations here
                if players_hand == [9, 9]:
                    result = "S"
                if players_hand == [8, 8]:
                    if dealers_hand[0] == 9 and true_count >= 4: # deviation
                        result = "S"
                    if dealers_hand[0] == 10 and true_count > 0: # deviation
                        result = "S"
                    if dealers_hand[0] == "A" and true_count >= 3: # deviation
                        result = "S"
                    if dealers_hand[0] in [2, 3, 4, 5, 6]:
                        result = "S"
                    else:
                        result = "H"
                if players_hand == [7, 7]:
                    if dealers_hand[0] in [2, 3, 4, 5, 6]:
                        result = "S"
                    else:
                        result = "H"
                if players_hand == [6, 6]:
                    if dealers_hand[0] == 2 and true_count >= 3:
                        result = "S"
                    if dealers_hand[0] == 3 and true_count >= 2:
                        result = "S"
                    if dealers_hand[0] == 4 and true_count < 0:
                        result = "H"
                    if dealers_hand[0] in [4, 5, 6]:
                        result = "S"
                    else:
                        result = "H"
                if players_hand == [4, 4]:
                    if dealers_hand == 6 and true_count >= 2:
                        result = "D"
                    else:
                        result = "H"
                if players_hand == [3, 3] or players_hand == [2, 2]:
                    result = "H"
            if result == "SUR":
                #print("You can't late surrender after you've split, your only choice is to hit")
                #print("You hit with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
                card = shoe.pop(0)
                players_hand.append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                cards_remaining = len(shoe)
                true_count = count / decks_remaining
                true_count = true_count_converter(true_count)
                dict_count_frequency[true_count] += 1
                #print("players_hand after splits and in SUR conditional: " + str(print_hand(players_hand)))
                #print("running_count after splits and in SUR conditional: " + str(count))
                #print("decks_remaining after splits and in SUR conditional: " + str(decks_remaining))
                #print("cards_remaining after splits and in SUR conditional: " + str(cards_remaining))
                #print("true_count calculated after splits and in SUR conditional: " + str(true_count))
                continue # should restart while loop, I think it rechecks the while loop condition when it restarts
            if result == "H":
                #print("You hit with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
                card = shoe.pop(0)
                players_hand.append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                cards_remaining = len(shoe)
                true_count = count / decks_remaining
                true_count = true_count_converter(true_count)
                dict_count_frequency[true_count] += 1
                #print("players_hand after splits and in H conditional: " + str(print_hand(players_hand)))
                #print("running_count after splits and in H conditional: " + str(count))
                #print("decks_remaining after splits and in H conditional: " + str(decks_remaining))
                #print("cards_remaining after splits and in H conditional: " + str(cards_remaining))
                #print("true_count calculated after splits and in H conditional: " + str(true_count))
                continue
            if result == "S":
                #print("You stand with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
                break
            if result == "D":
                #print("You double with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
                card = shoe.pop(0)
                players_hand.append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                cards_remaining = len(shoe)
                true_count = count / decks_remaining
                true_count = true_count_converter(true_count)
                double_boolean = True
                dict_count_frequency[true_count] += 1
                #print("players_hand after splits and in D conditional: " + str(print_hand(players_hand)))
                #print("running_count after splits and in D conditional: " + str(count))
                #print("decks_remaining after splits and in D conditional: " + str(decks_remaining))
                #print("cards_remaining after splits and in D conditional: " + str(cards_remaining))
                #print("true_count calculated after splits and in D conditional: " + str(true_count))
                break
        if ace_converter(players_hand)["hand_total"] > 21:
            #print("players_hand: " + str(print_hand(players_hand)))
            #print("You have busted with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]))
            player_bust = True
            break
        dict_a[i] = {
                        "players_hand" : players_hand ,
                        "dealers_hand" : dealers_hand ,
                        "double_boolean" : double_boolean ,
                        "player_bust" : player_bust ,
                        "shoe" : shoe ,
                        "count" : count ,
                        "decks_remaining" : round(decks_remaining, 5) ,
                        "true_count" : true_count ,
                        "ace_split_boolean" : ace_split_boolean ,
                        "dict_count_frequency" : dict_count_frequency
                    }
        #split_players_hand[i] = players_hand
        i += 1
    return dict_a



def play_decision(players_hand, dealers_hand, player_blackjack_boolean, dealer_blackjack_boolean, dealer_bust, bet, bet_spread, bankroll, double_boolean, player_bust, late_surrender_boolean, true_count, running_count, hands_won, hands_lost, hands_pushed, hands_surrendered, hands_played, ace_split_boolean):
    #print()
    #print("play_decision")
    #print("Player has (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]))
    #print("Dealer has (" + str(print_hand(dealers_hand)) + "), a " + str(ace_converter(dealers_hand)["hand_total"]))
    #print("running_count given to play_decision: " + str(running_count))
    #print("true_count given to play_decision: " + str(true_count))
    #print("cards_remaining: " + str(len(shoe)))
    hands_played += 1
    '''
    if true_count < 0:
        bet = bet_spread[math.ceil(true_count)]
        print("true_count ceiled: " + str(math.ceil(true_count)))
    elif true_count >= 0:
        bet = bet_spread[math.floor(true_count)]
        print("true_count floored: " + str(math.floor(true_count)))
    '''
    if ace_split_boolean:
        player_blackjack_boolean = False
        #print("Hello")
        #print(players_hand)
    if player_bust:
        #print("Player has busted (Player loses $" + str(bet) + ")")
        bankroll -= bet
        hands_lost += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    if late_surrender_boolean and dealer_blackjack_boolean:
        #print("Player chose to late surrender and Dealer has blackjack (Player loses $" + str(bet) + ")")
        bankroll -= bet
        hands_surrendered += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    if late_surrender_boolean and not dealer_blackjack_boolean:
        #print("Player chose to late surrender and Dealer does not have blackjack (Player loses $" + str(0.5 * bet) + ")")
        bankroll -= (0.5 * bet)
        hands_surrendered += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    if player_blackjack_boolean and dealer_blackjack_boolean: # both have blackjack
        #print("Player and Dealer have blackjack (Push)")
        hands_pushed += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif player_blackjack_boolean and not dealer_blackjack_boolean:
        #print("Player has blackjack but Dealer does not (Player wins $" + str(1.5 * bet) + ")")
        bankroll += (1.5 * bet)
        hands_won += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif dealer_bust and double_boolean:
        #print("Player doubled and Dealer busted (Player wins $" + str(2 * bet) + ")")
        bankroll += (2 * bet)
        hands_won += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif (ace_converter(players_hand)["hand_total"] > ace_converter(dealers_hand)["hand_total"]) and not dealer_bust and double_boolean:
        #print("Player doubled and has greater hand than Dealer (Player wins $" + str(2 * bet) + ")")
        bankroll += (2 * bet)
        hands_won += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif (ace_converter(players_hand)["hand_total"] > ace_converter(dealers_hand)["hand_total"]):
        #print("Player has a greater hand than Dealer (Player wins $" + str(bet) + ")")
        bankroll += bet
        hands_won += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif (ace_converter(players_hand)["hand_total"] < ace_converter(dealers_hand)["hand_total"]) and not dealer_bust and double_boolean:
        #print("Dealer has not busted and has a greater hand than Player who doubled (Player loses $" + str(2 * bet) + ")")
        bankroll -= (2 * bet)
        hands_lost += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif (ace_converter(players_hand)["hand_total"] < ace_converter(dealers_hand)["hand_total"]) and not dealer_bust:
        #print("Dealer has greater hand than Player and has not busted (Player loses $" + str(bet) + ")")
        bankroll -= bet
        hands_lost += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif (ace_converter(players_hand)["hand_total"] == ace_converter(dealers_hand)["hand_total"]):
        #print("Push")
        #print("bankroll: " + str(bankroll))
        #print()
        hands_pushed += 1
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    elif dealer_bust:
        #print("Dealer busted and Player has not busted (Player wins $" + str(bet) + ")")
        bankroll += bet
        hands_won += 1
        #print("bankroll: " + str(bankroll))
        #print()
        return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}
    return {"bankroll" : bankroll, "hands_won" : hands_won, "hands_lost" : hands_lost, "hands_pushed" : hands_pushed, "hands_surrendered" : hands_surrendered, "hands_played" : hands_played}

'''
hl, = plt.plot([], [])

def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw()
'''

dict_count_frequency = {    -45 : 0, -44 : 0, -43 : 0, -42 : 0, -41 : 0 , -40 : 0, -39 : 0, -38 : 0, -37 : 0, -36 : 0 , -35 : 0, -34 : 0, -33 : 0, -32 : 0, -31 : 0 ,
                            -30 : 0, -29 : 0, -28 : 0, -27 : 0, -26 : 0 , -25 : 0, -24 : 0, -23 : 0, -22 : 0, -21 : 0 , -20 : 0, -19 : 0, -18 : 0, -17 : 0 ,
                            -16 : 0, -15 : 0, -14 : 0 ,
                            -13 : 0, -12 : 0, -11 : 0 ,
                            -11 : 0, -10 : 0,  -9 : 0 ,
                            -8 : 0,  -7 : 0, -6 : 0 ,
                            -5 : 0,  -4 : 0 ,
                            -3 : 0,  -2 : 0, -1 : 0 ,
                            0 : 0,   1 : 0,  2 : 0 ,
                            3 : 0,   4 : 0,  5 : 0 ,
                            6 : 0,   7 : 0,  8 : 0 ,
                            9 : 0,  10 : 0, 11 : 0 ,
                            12 : 0, 13 : 0, 14 : 0 ,
                            15 : 0, 16 : 0, 17 : 0 ,
                            18 : 0, 19 : 0, 20 : 0 ,
                            21 : 0, 22 : 0, 23 : 0 ,
                            24 : 0, 25 : 0, 26 : 0 ,
                            27 : 0, 28 : 0, 29 : 0 ,
                            30 : 0, 31 : 0, 32 : 0 ,
                            33 : 0, 34 : 0, 35 : 0 ,
                            36 : 0, 37 : 0, 38 : 0 ,
                            39 : 0, 40 : 0, 41 : 0 ,
                            42 : 0, 43 : 0, 44 : 0 ,
                            45 : 0
                        }
bet_spread = {  -45 : 10, -44 : 10, -43 : 10, -42 : 10, -41 : 10 ,
                -40 : 10, -39 : 10, -38 : 10, -37 : 10, -36 : 10 ,
                -35 : 10, -34 : 10, -33 : 10, -32 : 10, -31 : 10 ,
                -30 : 10, -29 : 10, -28 : 10, -27 : 10, -26 : 10 ,
                -25 : 10, -24 : 10, -23 : 10, -22 : 10, -21 : 10 ,
                -20 : 10, -19 : 10, -18 : 10, -17 : 10, -16 : 10 ,
                -15 : 10, -14 : 10, -13 : 10, -12 : 10, -11 : 10 ,
                -10 : 10,  -9 : 10,   -8 : 10,  -7 : 10, -6 : 10 ,
                -5 : 10,   -4 : 10,   -3 : 10,  -2 : 10, -1 : 10,
                0 : 10,   1 : 50,   2 : 80 ,
                3 : 120,   4 : 120,  5 : 120 ,
                6 : 120,   7 : 120,  8 : 120 ,
                9 : 120,  10 : 120, 11 : 120 ,
                12 : 120, 13 : 120, 14 : 120 ,
                15 : 120, 16 : 120, 17 : 120 ,
                18 : 120, 19 : 120, 20 : 120 ,
                21 : 120, 22 : 120, 23 : 120 ,
                24 : 120, 25 : 120, 26 : 120 ,
                27 : 120, 28 : 120, 29 : 120 ,
                30 : 120, 31 : 120, 32 : 120 ,
                33 : 120, 34 : 120, 35 : 120 ,
                36 : 120, 37 : 120, 38 : 120 ,
                39 : 120, 40 : 120, 41 : 120
            }
bankroll_list = []
sims_list = []
cards_played_total = []
#split_hands_played = 0
hands_played = 0
hands_won = 0
hands_lost = 0
hands_pushed = 0
hands_surrendered = 0
sims_amt = 1
for sims in range(0, sims_amt):
    deck_count = 6
    penetration = 85 # as a percentage, adjust here
    count = 0
    true_count = 0
    cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # need to do penetration
    cards_played = 0
    shoe = cards * 4 * deck_count
    random.shuffle(shoe)
    rounds = 25
    hands_per_hour = 70
    starting_bankroll = 15000
    bankroll = starting_bankroll
    print("sims done: " + str(sims))
    for i in range(0, rounds):
        if (len(cards * 4 * deck_count) - len(shoe)) >= ((penetration / 100) * len(cards * 4 * deck_count)): # penetration
            count = 0
            true_count = 0
            cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
            shoe = cards * 4 * deck_count
            random.shuffle(shoe)
            #print("DECK RESHUFFLED")
        #print("len(shoe): " + str(len(shoe)))
        if true_count < 0:
            bet = bet_spread[math.ceil(true_count)]
            #print("true_count ceiled: " + str(math.ceil(true_count)))
        elif true_count >= 0:
            bet = bet_spread[math.floor(true_count)]
            #print("true_count floored: " + str(math.floor(true_count)))
        player_dict = play_player(shoe, count, deck_count, dict_count_frequency)
        dict_count_frequency = player_dict["dict_count_frequency"]
        count = player_dict["count"]
        true_count = player_dict["true_count"]
        #print("len(shoe): " + str(len(shoe)))
        #print("len(shoe): " + str(len(shoe)))
        #print("split_boolean: " + str(player_dict["split_boolean"]))
        if player_dict["split_boolean"] == True:
            #print("You are in the player_dict[split_boolean] check")
            split_dict = split(player_dict["players_hand"], player_dict["dealers_hand"], player_dict["shoe"], count, dict_count_frequency)
            for j in range(0, len(split_dict)):
                #print(split_dict[j]["count"])
                count = split_dict[j]["count"]
                #print(split_dict[j]["true_count"])
                true_count = split_dict[j]["true_count"]
                dict_count_frequency = split_dict[j]["dict_count_frequency"]
                cards_played += len(split_dict[j]["players_hand"])
            #print("count: " + str(count))
            #print("true_count: " + str(true_count))
            #true_count = split_dict[-1]["true_count"]
            dealer_dict = play_dealer(player_dict["dealers_hand"], player_dict["player_bust"], player_dict["late_surrender_boolean"], player_dict["player_blackjack_boolean"], player_dict["shoe"], count, deck_count, dict_count_frequency)
            cards_played += len(dealer_dict["dealers_hand"])
            count = dealer_dict["count"]
            true_count = dealer_dict["true_count"]
            dict_count_frequency = dealer_dict["dict_count_frequency"]
            #print("len(shoe): " + str(len(shoe)))
            for j in range(0, len(split_dict)):
                bankroll_dict = play_decision(split_dict[j]["players_hand"], dealer_dict["dealers_hand"], player_dict["player_blackjack_boolean"], player_dict["dealer_blackjack_boolean"], dealer_dict["dealer_bust"], bet, bet_spread, bankroll, split_dict[j]["double_boolean"], split_dict[j]["player_bust"], player_dict["late_surrender_boolean"], true_count, count, hands_won, hands_lost, hands_pushed, hands_surrendered, hands_played, split_dict[j]["ace_split_boolean"])
                bankroll = bankroll_dict["bankroll"]
                bankroll_list.append(bankroll)
                hands_won = bankroll_dict["hands_won"]
                hands_lost = bankroll_dict["hands_lost"]
                hands_pushed = bankroll_dict["hands_pushed"]
                hands_surrendered = bankroll_dict["hands_surrendered"]
                hands_played = bankroll_dict["hands_played"]
                #dict_count_frequency = split_dict[j]["dict_count_frequency"]
                #count = split_dict[j]["count"]
                #true_count = split_dict[j]["true_count"]
                #update_line(hl, bankroll_list)
            #for j in range(0, len(split_dict)):
                #print(split_dict[j]["players_hand"])
                #count += count_update(split_dict[j]["players_hand"])
                #decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                #true_count = count / decks_remaining
                #print("running_count in SIM: " + str(count))
                #print("split_dict running_count: " + str(split_dict[j]["count"]))
                #print("split_dict decks_remaining: " + str(split_dict[j]["decks_remaining"]))
                #print("split_dict true_count: " + str(split_dict[j]["true_count"]))
            continue # this fixes the problem where the pair doesn't get get forgotten
        dealer_dict = play_dealer(player_dict["dealers_hand"], player_dict["player_bust"], player_dict["late_surrender_boolean"], player_dict["player_blackjack_boolean"], player_dict["shoe"], count, deck_count, dict_count_frequency)
        cards_played += len(dealer_dict["dealers_hand"])
        cards_played += len(player_dict["players_hand"])
        dict_count_frequency = dealer_dict["dict_count_frequency"]
        count = dealer_dict["count"]
        true_count = dealer_dict["true_count"]
        bankroll_dict = play_decision(player_dict["players_hand"], dealer_dict["dealers_hand"], player_dict["player_blackjack_boolean"], player_dict["dealer_blackjack_boolean"], dealer_dict["dealer_bust"], bet, bet_spread, bankroll, player_dict["double_boolean"], player_dict["player_bust"], player_dict["late_surrender_boolean"], true_count, count, hands_won, hands_lost, hands_pushed, hands_surrendered, hands_played, False)
        bankroll = bankroll_dict["bankroll"]
        bankroll_list.append(bankroll)
        #update_line(hl, bankroll_list)
        hands_won = bankroll_dict["hands_won"]
        hands_lost = bankroll_dict["hands_lost"]
        hands_pushed = bankroll_dict["hands_pushed"]
        hands_surrendered = bankroll_dict["hands_surrendered"]
        hands_played = bankroll_dict["hands_played"]
        #count += count_update(player_dict["players_hand"])
        #count += count_update(dealer_dict["dealers_hand"])
        #decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
        #true_count = count / decks_remaining
        if bankroll <= 0: # you went broke
            sims_list.append((-1 * starting_bankroll) + bankroll)
            cards_played_total.append(cards_played)
            break
        #print("i: " + str(i))
        if i == (rounds - 1): # end of loop
            #print("Hello")
            if bankroll > starting_bankroll:
                sims_list.append(bankroll - starting_bankroll) # profit
                cards_played_total.append(cards_played)
            else:
                sims_list.append(-1 * (starting_bankroll - bankroll)) # losses
                cards_played_total.append(cards_played)
        #print()
        #print("running count in SIM: " + str(count))
        #print("player_dict running_count: " + str(player_dict["count"]))
        #print("player_dict decks_remaining: " + str(player_dict["decks_remaining"]))
        #print("player_dict true_count: " + str(player_dict["true_count"]))
        #print("bankroll: " + str(bankroll))

#print("hands_won: " + str(hands_won))
#print("hands_lost: " + str(hands_lost))
#print("hands_pushed: " + str(hands_pushed))
#print("hands_surrendered: " + str(hands_surrendered))
print("You win %" + str(hands_won / hands_played) + " of the time.")
print("You lose %" + str(hands_lost / hands_played) + " of the time.")
print("You pushed %" + str(hands_pushed / hands_played) + " of the time.")
print("You surrendered %" + str(hands_surrendered / hands_played) + " of the time.")
print("Total percent of hands_won, hands_lost, hands_pushed, and hands_surrendered: %" + str((hands_won + hands_lost + hands_pushed + hands_surrendered) / hands_played))
print("Total hands played by addition of parts: " + str(hands_won + hands_lost + hands_pushed + hands_surrendered))
print("Total hands played from play_decision counter: " + str(hands_played))
print(sims_list)
print(cards_played_total)

broke_counter = 0
for values in sims_list:
    if values <= (-1 * starting_bankroll):
        broke_counter += 1
average_of_all_bankrolls = sum(sims_list) / sims_amt
average_hours_played_per_sim = (hands_played / hands_per_hour) / sims_amt
print("You went broke " + str(broke_counter) + " times.")
print("Your risk of ruin based on " + str(sims_amt) + " sims is %" + str(100 * (broke_counter / sims_amt)))
print("ev ($/hr): $" + str(average_of_all_bankrolls / average_hours_played_per_sim))
print("Average of all bankrolls: $" + str(average_of_all_bankrolls))
print("hands_played (" + str(hands_played) + ") / hands_per_hour (" + str(hands_per_hour) + "): " + str(hands_played / hands_per_hour))
#print("split_hands_played: " + str(split_hands_played))

total_cards_dealt = 0
for value in dict_count_frequency:
    total_cards_dealt += dict_count_frequency[value]
    print(str(value) + " : " + str(dict_count_frequency[value]))
print("total_cards_dealt: " + str(total_cards_dealt))
for value in dict_count_frequency:
    print(str(value) + " : " + str(round(dict_count_frequency[value] / total_cards_dealt, 4) * 100) + "%")

end_time = time.time()
print("time: " + str(round(end_time - start_time, 5)) + "s")
#y=[2,4,6,1]

plt.plot(bankroll_list)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title("bankroll")
plt.show()


'''
plt.axis([0, 1000, -1000, 200000])

for i in range(1000):
    y = bankroll_list[i]
    plt.scatter(i, y)
    plt.pause(0.00000001)

plt.show()
'''
