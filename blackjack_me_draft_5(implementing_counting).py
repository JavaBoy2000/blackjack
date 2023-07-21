import random
import matplotlib.pyplot as plt
import time
import math

start_time = time.time()

def generate_shoe(deck_count): # for later if you need it
    cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    shoe = cards * 4 * deck_count
    random.shuffle(shoe)
    return shoe

def generate_player_hand(shoe):
    players_hand = [shoe.pop(0), shoe.pop(0)]
    return players_hand

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
def basic_strategy(players_hand, dealers_hand): # can turn off LS here
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
    if players_hand == [5, 5]:
        if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9]:
            return "D"
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
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        if dealer_upcard in [9, 10, "A"] and len(players_hand) == 2:
            return "SUR"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 15 and not soft_hand_check(players_hand):
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        if dealer_upcard in [10] and len(players_hand) == 2:
            return "SUR"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 14 and not soft_hand_check(players_hand):
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 13 and not soft_hand_check(players_hand):
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "S"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 12 and not soft_hand_check(players_hand):
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
        if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] == 9 and not soft_hand_check(players_hand):
        if dealer_upcard in [3, 4, 5, 6] and DAS_boolean:
            return "D"
        else:
            return "H"
    if ace_converter(players_hand)["hand_total"] <= 8 and not soft_hand_check(players_hand):
        return "H"




def play_dealer(dealers_hand, player_bust, late_surrender_boolean, player_blackjack_boolean, shoe):
    dealer_blackjack_boolean = False
    dealer_bust = False
    # insurance_check = False # might need this later
    dealer_upcard = dealers_hand[0]
    #print("soft_hand_check(" + str(print_hand(dealers_hand)) + "): " + str(soft_hand_check(dealers_hand)))
    if player_bust or late_surrender_boolean or player_blackjack_boolean:
        return {
                    "dealers_hand" : dealers_hand ,
                    "dealer_bust" : dealer_bust ,
                    "shoe" : shoe
                } # end dealer stuff
    if soft_hand_check(dealers_hand): # hand is soft so hit cause H17
        #print("dealers_hand: " + str(print_hand(dealers_hand)))
        #print("dealer has a soft " + str(ace_converter(dealers_hand)["hand_total"]))
        if ace_converter(dealers_hand)["hand_total"] == 21 and len(dealers_hand) == 2:
            #print("dealer has blackjack")
            dealer_blackjack_boolean = True # return this
        while ace_converter(dealers_hand)["hand_total"] <= 17:
            #print("dealer hits with (" + str(print_hand(dealers_hand)) + "), a soft " + str(ace_converter(dealers_hand)["hand_total"]))
            dealers_hand.append(shoe.pop(0))
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
            dealers_hand.append(shoe.pop(0))
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
                "shoe" : shoe
            } # end dealer stuff

def play_player(shoe, count, deck_count):
    players_hand = [shoe.pop(0), shoe.pop(0)]
    count += count_update(players_hand)
    dealers_hand = [shoe.pop(0), shoe.pop(0)]
    count += count_update(dealers_hand)
    decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
    true_count = count / decks_remaining
    dealer_upcard = dealers_hand[0]
    player_bust = False
    late_surrender_boolean = False
    player_blackjack_boolean = False
    dealer_blackjack_boolean = False
    double_boolean = False
    split_boolean = False
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
        if basic_strategy(players_hand, dealers_hand) == "SUR":
            late_surrender_boolean = True
            break
        if basic_strategy(players_hand, dealers_hand) == "Y":
            split_boolean = True
            break
        if basic_strategy(players_hand, dealers_hand) == "H":
            #print("You hit with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            card = shoe.pop(0)
            players_hand.append(card)
            count += count_update([card]) # will this work?
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            true_count = count / decks_remaining
            #print("players_hand: " + str(print_hand(players_hand)))
            continue # should restart while loop and check while loop condition
        if basic_strategy(players_hand, dealers_hand) == "S":
            #print("You stand with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            break
        if basic_strategy(players_hand, dealers_hand) == "D":
            #print("You double with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
            double_boolean = True
            card = shoe.pop(0)
            players_hand.append(card)
            count += count_update([card]) # will this work?
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            true_count = count / decks_remaining
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
                "true_count" : round(true_count, 5)
            }

def split(players_hand, dealers_hand, shoe, count):
    # we can hard code three splits, three splits is usually the max in casinos
    # I don't want to hard code three splits, yeah I know
    dict_a = {}
    double_boolean = False
    player_bust = False
    count += count_update(dealers_hand)
    decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
    true_count = count / decks_remaining
    if players_hand == ["A", "A"]: # no RSA
        count += count_update(players_hand)
        split_players_hand = [[players_hand[0]], [players_hand[1]]]
        #print("in the split function for aces")
        #print(split_players_hand)
        i = 0
        # fix it to where a "natural" doesn't get paid 3:2
        # use boolean that gets returned and then used in play_decision
        for players_hand in split_players_hand:
            card = shoe.pop(0)
            split_players_hand[i].append(card)
            count += count_update([card])
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            true_count = count / decks_remaining
            dict_a[i] = {
                            "players_hand" : split_players_hand[i] ,
                            "dealers_hand" : dealers_hand ,
                            "double_boolean" : double_boolean ,
                            "player_bust" : player_bust ,
                            "shoe" : shoe ,
                            "count" : count ,
                            "decks_remaining" : round(decks_remaining, 5) ,
                            "true_count" : round(true_count, 5)
                        }
            i += 1
        return dict_a
    split_players_hand = [[players_hand[0]], [players_hand[1]]] # this is the first hard coded split we can do two more
    num_splits = 1
    #print("You are in the split function")
    #print(split_players_hand)
    i = 0
    count += count_update(players_hand)
    for players_hand in split_players_hand:
        card = shoe.pop(0)
        split_players_hand[i].append(card)
        count += count_update([card])
        decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
        true_count = count / decks_remaining
        i += 1
    i = 0
    for players_hand in split_players_hand: # second split, one more
        if basic_strategy(players_hand, dealers_hand) == "Y":
            num_splits += 1
            #print("You are in the second split")
            split_players_hand_2 = [[split_players_hand[i][0]], [split_players_hand[i][1]]]
            count += count_update([split_players_hand[i][0]])
            #print(split_players_hand_2)
            for j in range(0, len(split_players_hand_2)):
                card = shoe.pop(0)
                split_players_hand_2[j].append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                true_count = count / decks_remaining
                #print(split_players_hand_2)
            if i == 0:
                split_players_hand_2.append(split_players_hand[i + 1])
            if i == 1:
                split_players_hand_2.append(split_players_hand[i - 1])
            split_players_hand = split_players_hand_2
            break
        i += 1
    #print(split_players_hand)
    #print("num_splits: " + str(num_splits))
    i = 0
    for players_hand in split_players_hand: # third split, no more splits
        # I think this third split splicing for the lists is wrong
        if basic_strategy(split_players_hand[i], dealers_hand) == "Y":
            num_splits += 1
            #print("You are in the third split")
            split_players_hand_3 = [[split_players_hand[i][0]], [split_players_hand[i][1]]]
            count += count_update([split_players_hand[i][1]])
            #print(split_players_hand_2)
            for j in range(0, len(split_players_hand_3)):
                card = shoe.pop(0)
                split_players_hand_3[j].append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                true_count = count / decks_remaining
                #print(split_players_hand_3)
            if i == 0:
                split_players_hand_3.append(split_players_hand[i + 1])
                split_players_hand_3.append(split_players_hand[i + 2])
            if i == 1:
                split_players_hand_3.append(split_players_hand[i - 1])
                split_players_hand_3.append(split_players_hand[i + 1])
            if i == 2:
                split_players_hand_3.append(split_players_hand[i - 1])
                split_players_hand_3.append(split_players_hand[i - 2])
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
            result = basic_strategy(players_hand, dealers_hand)
            if num_splits >= 3:
                if players_hand == [9, 9]:
                    result = "S"
                if players_hand == [8, 8] or players_hand == [7, 7]:
                    if dealers_hand[0] in [2, 3, 4, 5, 6]:
                        result = "S"
                    else:
                        result = "H"
                if players_hand == [6, 6]:
                    if dealers_hand[0] in [4, 5, 6]: # need deviations here
                        result = "S"
                    else:
                        result = "H"
                if players_hand == [4, 4] or players_hand == [3, 3] or players_hand == [2, 2]:
                    result = "H"
            if result == "SUR":
                #print("You can't late surrender after you've split, your only choice is to hit")
                #print("You hit with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
                card = shoe.pop(0)
                players_hand.append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                true_count = count / decks_remaining
                continue # should restart while loop, I think it rechecks the while loop condition when it restarts
            if result == "H":
                #print("You hit with (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]) + ", against a " + str(dealers_hand[0]))
                card = shoe.pop(0)
                players_hand.append(card)
                count += count_update([card])
                decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
                true_count = count / decks_remaining
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
                true_count = count / decks_remaining
                double_boolean = True
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
                        "true_count" : round(true_count, 5)
                    }
        #split_players_hand[i] = players_hand
        i += 1
    return dict_a



def play_decision(players_hand, dealers_hand, player_blackjack_boolean, dealer_blackjack_boolean, dealer_bust, bet_spread, bankroll, double_boolean, player_bust, late_surrender_boolean, true_count, running_count):
    #print()
    #print("play_decision")
    #print("Player has (" + str(print_hand(players_hand)) + "), a " + str(ace_converter(players_hand)["hand_total"]))
    #print("Dealer has (" + str(print_hand(dealers_hand)) + "), a " + str(ace_converter(dealers_hand)["hand_total"]))
    #print("running_count given to play_decision: " + str(running_count))
    #print("true_count given to play_decision: " + str(true_count))
    if true_count < 0:
        bet = bet_spread[math.ceil(true_count)]
        #print("true_count ceiled: " + str(math.ceil(true_count)))
    elif true_count >= 0:
        bet = bet_spread[math.floor(true_count)]
        #print("true_count floored: " + str(math.floor(true_count)))
    #print("true_count floored: " + str(math.floor(true_count)))
    if player_bust:
        #print("Player has busted (Player loses $" + str(bet) + ")")
        bankroll -= bet
        return bankroll
    if late_surrender_boolean and dealer_blackjack_boolean:
        #print("Player chose to late surrender and Dealer has blackjack (Player loses $" + str(bet) + ")")
        bankroll -= bet
        return bankroll
    if late_surrender_boolean and not dealer_blackjack_boolean:
        #print("Player chose to late surrender and Dealer does not have blackjack (Player loses $" + str(0.5 * bet) + ")")
        bankroll -= (0.5 * bet)
        return bankroll
    if player_blackjack_boolean and dealer_blackjack_boolean: # both have blackjack
        #print("Player and Dealer have blackjack (Push)")
        return bankroll
    elif player_blackjack_boolean and not dealer_blackjack_boolean:
        #print("Player has blackjack but Dealer does not (Player wins $" + str(1.5 * bet) + ")")
        bankroll += (1.5 * bet)
        return bankroll
    elif dealer_bust and double_boolean:
        #print("Player doubled and Dealer busted (Player wins $" + str(2 * bet) + ")")
        bankroll += (2 * bet)
        return bankroll
    elif (ace_converter(players_hand)["hand_total"] > ace_converter(dealers_hand)["hand_total"]) and not dealer_bust and double_boolean:
        #print("Player doubled and has greater hand than Dealer (Player wins $" + str(2 * bet) + ")")
        bankroll += (2 * bet)
        return bankroll
    elif (ace_converter(players_hand)["hand_total"] > ace_converter(dealers_hand)["hand_total"]):
        #print("Player has a greater hand than Dealer (Player wins $" + str(bet) + ")")
        bankroll += bet
        return bankroll # maybe change to returning a dictionary
    elif (ace_converter(players_hand)["hand_total"] < ace_converter(dealers_hand)["hand_total"]) and not dealer_bust and double_boolean:
        #print("Dealer has not busted and has a greater hand than Player who doubled (Player loses $" + str(2 * bet) + ")")
        bankroll -= (2 * bet)
        return bankroll
    elif (ace_converter(players_hand)["hand_total"] < ace_converter(dealers_hand)["hand_total"]) and not dealer_bust:
        #print("Dealer has greater hand than Player and has not busted (Player loses $" + str(bet) + ")")
        bankroll -= bet
        return bankroll
    elif (ace_converter(players_hand)["hand_total"] == ace_converter(dealers_hand)["hand_total"]):
        #print("Push")
        return bankroll
    elif dealer_bust:
        #print("Dealer busted and Player has not busted (Player wins $" + str(bet) + ")")
        bankroll += bet
        return bankroll
    return bankroll

starting_bankroll = 1000000
bankroll = starting_bankroll
bet_spread = {  -25 : 0, -24 : 0, -23 : 0, -22 : 0, -21 : 0 ,
                -20 : 0, -19 : 0, -18 : 0, -17 : 0, -16 : 0 ,
                -15 : 0, -14 : 0, -13 : 0, -12 : 0, -11 : 0 ,
                -10 : 0, -9 : 0, -8 : 0, -7 : 0, -6 : 0 ,
                -5 : 0, -4 : 0, -3 : 0, -2 : 0, -1 : 0,
                0 : 0,    1 : 10,   2 : 25,
                3 : 50,   4 : 75,   5 : 100,
                6 : 100,  7 : 100,  8 : 100 ,
                9 : 100,  10 : 100, 11 : 100,
                12 : 100, 13 : 100, 14 : 100 ,
                15 : 100, 16 : 100, 17 : 100,
                18 : 100, 19 : 100, 20 : 100 ,
                21 : 100, 22 : 100, 23 : 100,
                24 : 100, 25 : 100, 26 : 100
            }
deck_count = 6
count = 0
true_count = 0
cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # need to do penetration
shoe = cards * 4 * deck_count
random.shuffle(shoe)
sims = 150000
rounds_per_hour = 70

bankroll_list = []
for i in range(0, sims):
    penetration = 75 # as a percentage, adjust here
    deck_count = 6 # adjust accordingly
    if (len(cards * 4 * deck_count) - len(shoe)) >= ((penetration / 100) * len(cards * 4 * deck_count)): # penetration
        count = 0
        true_count = 0
        cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        shoe = cards * 4 * deck_count
        random.shuffle(shoe)
    #print("len(shoe): " + str(len(shoe)))
    player_dict = play_player(shoe, count, deck_count)
    #print("len(shoe): " + str(len(shoe)))
    dealer_dict = play_dealer(player_dict["dealers_hand"], player_dict["player_bust"], player_dict["late_surrender_boolean"], player_dict["player_blackjack_boolean"], player_dict["shoe"])
    #print("len(shoe): " + str(len(shoe)))
    #print("split_boolean: " + str(player_dict["split_boolean"]))
    if player_dict["split_boolean"] == True:
        #print("You are in the player_dict[split_boolean] check")
        split_dict = split(player_dict["players_hand"], player_dict["dealers_hand"], dealer_dict["shoe"], count)
        #print("len(shoe): " + str(len(shoe)))
        for j in range(0, len(split_dict)):
            bankroll = play_decision(split_dict[j]["players_hand"], dealer_dict["dealers_hand"], player_dict["player_blackjack_boolean"], player_dict["dealer_blackjack_boolean"], dealer_dict["dealer_bust"], bet_spread, bankroll, split_dict[j]["double_boolean"], split_dict[j]["player_bust"], player_dict["late_surrender_boolean"], true_count, count)
            bankroll_list.append(bankroll)
        continue # this fixes the problem where the pair doesn't get get forgotten
        for j in range(0, len(split_dict)):
            #print(split_dict[j]["players_hand"])
            count += count_update(split_dict[j]["players_hand"])
            decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
            true_count = count / decks_remaining
            #print("running_count in SIM: " + str(count))
            #print("split_dict running_count: " + str(split_dict[j]["count"]))
            #print("split_dict decks_remaining: " + str(split_dict[j]["decks_remaining"]))
            #print("split_dict true_count: " + str(split_dict[j]["true_count"]))
        continue
    bankroll = play_decision(player_dict["players_hand"], dealer_dict["dealers_hand"], player_dict["player_blackjack_boolean"], player_dict["dealer_blackjack_boolean"], dealer_dict["dealer_bust"], bet_spread, bankroll, player_dict["double_boolean"], player_dict["player_bust"], player_dict["late_surrender_boolean"], true_count, count)
    bankroll_list.append(bankroll)
    count += count_update(player_dict["players_hand"])
    count += count_update(dealer_dict["dealers_hand"])
    decks_remaining = deck_count * (len(shoe) / (deck_count * 52))
    true_count = count / decks_remaining
    #print()
    #print("running count in SIM: " + str(count))
    #print("player_dict running_count: " + str(player_dict["count"]))
    #print("player_dict decks_remaining: " + str(player_dict["decks_remaining"]))
    #print("player_dict true_count: " + str(player_dict["true_count"]))
    #print("bankroll: " + str(bankroll))


money_made = (bankroll - starting_bankroll)
print("money_made: $" + str(money_made) + " in " + str(sims / rounds_per_hour) + "hrs")
ev = money_made / (sims / rounds_per_hour)
print("ev ($/hr) : $" + str(ev))



end_time = time.time()
print("time: " + str(round(end_time - start_time, 5)) + "s")
#y=[2,4,6,1]
plt.plot(bankroll_list)
plt.xlabel('X-axis')
#plt.ylabel('Y-axis')
plt.title("A simple line graph")
plt.show()
