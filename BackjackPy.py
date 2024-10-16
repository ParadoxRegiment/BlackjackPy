import inquirer
import random
import time
import sys

deck = [["1-S", "2-S", "3-S", "4-S", "5-S", "6-S", "7-S", "8-S", "9-S", "10-S", "J-S", "Q-S", "K-S"],
        ["1-C", "2-C", "3-C", "4-C", "5-C", "6-C", "7-C", "8-C", "9-C", "10-C", "J-C", "Q-C", "K-C"],
        ["1-H", "2-H", "3-H", "4-H", "5-H", "6-H", "7-H", "8-H", "9-H", "10-H", "J-H", "Q-H", "K-H"],
        ["1-D", "2-D", "3-D", "4-D", "5-D", "6-D", "7-D", "8-D", "9-D", "10-D", "J-D", "Q-D", "K-D"]]

def pullCard():
    card_set = random.randint(0, 3)
    number = random.randint(0, 12)
    card_check = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    if deck[card_set][number] == "0":
        return pullCard()
    
    pulled_card = deck[card_set][number]
    points = 0
    
    for val in card_check:
        if val in pulled_card:
            try:
                points = int(val)
            except ValueError:
                points = 10
            deck[card_set][number] = "0"

    return pulled_card, points

class blackjackPlayer():
    
    def __init__(cls):
        cls._player_hand = []
        cls._player_points = 0
        cls._player_total = 500

class blackjackDealer():
    
    def __init__(cls):
        cls._dealer_hand = []
        cls._dealer_points = 0
        
class blackjackGame():
    
    def __init__(cls):
        cls.player = blackjackPlayer()
        cls.dealer = blackjackDealer()
        cls.player_bet = ""
    
    def _display_hands_points(cls, game_round : int, game_end = False):
        print(f"\nRound {game_round}")
        print("\nDealer's hand")
        print("-------------")
        
        if game_end == True:
            print(*cls.dealer._dealer_hand, sep = ", ")
            print(f"{cls.dealer._dealer_points} points")
        else:
            if game_round == 0:
                print(cls.dealer._dealer_hand[0], "X", sep = ", ")
            elif game_round >= 1 and game_round < len(cls.dealer._dealer_hand):
                print(*cls.dealer._dealer_hand[0:game_round] + ["X"], sep = ", ")
            elif game_round > len(cls.dealer._dealer_hand):
                print(*cls.dealer._dealer_hand[0:-1] + ["X"], sep = ", ")
        # print(f"{cls.dealer._dealer_points} points")
        
        print("\nPlayer's hand")
        print("-------------")
        print(*cls.player._player_hand, sep = ", ")
        print(f"{cls.player._player_points} points")
        
    def start_game(cls):
        print(f"Player's total money: ${cls.player._player_total}")
        cls.player_bet = input("Enter a bet less than or equal to your total money: ")
        try:
            cls.player_bet = int(cls.player_bet)
        except ValueError:
            print("Please type in a numerical value only (no letters or special characters).\n")
            return cls.start_game()
        
        print("\nDrawing dealer's cards...")
        for i in range(2):
            dealer_card, dealer_points = pullCard()
            cls.dealer._dealer_hand.append(dealer_card)
            cls.dealer._dealer_points += dealer_points
        time.sleep(3)
        # print(cls.dealer._dealer_hand)
        
        print("\nDrawing player's cards...")
        for i in range(2):
            player_card, player_points = pullCard()
            cls.player._player_hand.append(player_card)
            cls.player._player_points += player_points
        time.sleep(3)

        # cls._display_hands_points(1)
    
    def game_hit(cls, who_hits : str):
        card, points = pullCard()
        
        match who_hits:
            case "player":
                cls.player._player_hand.append(card)
                cls.player._player_points += points
            case "dealer":
                print("Dealer hits.")
                cls.dealer._dealer_hand.append(card)
                cls.dealer._dealer_points += points


class playGame():
    def __init__(cls):
        cls.game_master = blackjackGame()
        cls.game_round = 1
        cls.start_game_q = [
            inquirer.List(
                "start",
                message="Would you like to start the game",
                choices=["Yes", "No"]
                )
        ]
        
        cls.hit_stand_double_q = [
        inquirer.List(
            "play",
            message="Would you like to hit, stand, or double",
            choices=["Hit", "Stand", "Double"]
            )
        ]
        
        cls.replay_q = [
            inquirer.List(
                "restart",
                message="Would you like to play again",
                choices=["Yes", "No"]
                )
        ]
    def play_game(cls):
        start_game_ans = inquirer.prompt(cls.start_game_q)
        match start_game_ans["start"]:
            case "Yes":
                cls.game_master.start_game()
                cls.game_master._display_hands_points(0)
                return cls.game_loop()
            case "No":
                sys.exit("Player has quit the program.")
    
    def game_loop(cls):
        while cls.game_master.player._player_points < 21:
            hsd_ans = inquirer.prompt(cls.hit_stand_double_q)
            match hsd_ans["play"]:
                case "Hit":
                    cls.game_master.game_hit("player")
                    if cls.game_master.player._player_points == 21:
                        cls.game_master._display_hands_points(cls.game_round)
                        break
                    cls.game_master.game_hit("dealer")
                    cls.game_master._display_hands_points(cls.game_round)
                    cls.game_round += 1
                case "Stand":
                    while cls.game_master.dealer._dealer_points < 17:
                        print("Player stands.")
                        cls.game_master.game_hit("dealer")
                        cls.game_master._display_hands_points(cls.game_round)
                        cls.game_round += 1
                    else:
                        print("\nDealer stands.")
                    break
                case "Double":
                    temp = cls.game_master.player_bet * 2
                    if temp > cls.game_master.player._player_total:
                        print(f"Player bet is now ${cls.game_master.player._player_total}. Bet cannot exceed current total money.")
                        cls.game_master._display_hands_points(cls.game_round)
                        cls.game_round += 1
                    else:
                        cls.game_master.player_bet = temp
                        del temp
                        print(f"Player bet is now ${cls.game_master.player_bet}")
                        cls.game_master._display_hands_points(cls.game_round)
                        cls.game_round += 1
        
        cls.game_master._display_hands_points(cls.game_round, game_end=True)
        if cls.game_master.player._player_points > 21:
            print(f"\nPlayer breaks! You have lost ${cls.game_master.player_bet}.")
            cls.game_master.player._player_total -= cls.game_master.player_bet
            print(f"Your new total is ${cls.game_master.player._player_total}")
            return cls.replay_game()
        elif cls.game_master.dealer._dealer_points > 21:
            print(f"\nDealer breaks! You have won ${cls.game_master.player_bet}.")
            cls.game_master.player._player_total += cls.game_master.player_bet
            print(f"Your new total is ${cls.game_master.player._player_total}")
            return cls.replay_game()
        elif cls.game_master.dealer._dealer_points > 21 and cls.game_master.player._player_points > 21:
            print(f"\nGame is a tie! Your bet is returned to you.")
            print(f"Your new total is ${cls.game_master.player._player_total}")
        else:
            if cls.game_master.player._player_points > cls.game_master.dealer._dealer_points:
                print(f"\nPlayer wins! You have won ${cls.game_master.player_bet}")
                cls.game_master.player._player_total += cls.game_master.player_bet
                print(f"Your new total is ${cls.game_master.player._player_total}")
                return cls.replay_game()
            else:
                print(f"\nDealer wins! You have lost ${cls.game_master.player_bet}")
                cls.game_master.player._player_total -= cls.game_master.player_bet
                print(f"Your new total is ${cls.game_master.player._player_total}")
                return cls.replay_game()
        
    def replay_game(cls):
        replay_ans = inquirer.prompt(cls.replay_q)
        
        match replay_ans["restart"]:
            case "Yes":
                cls.game_master.player._player_hand = []
                cls.game_master.player._player_points = 0
                cls.game_master.dealer._dealer_hand = []
                cls.game_master.dealer._dealer_points = 0
                cls.game_round = 1
                
                cls.game_master.start_game()
                cls.game_master._display_hands_points(0)
                return cls.game_loop()
            case "No":
                print(f"Thanks for playing. Your end total is ${cls.game_master.player._player_total}.")


if __name__ == "__main__":
    game = playGame()
    game.play_game()