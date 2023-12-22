import random
import json #used to store data
import os #used to find the current location of .py

# Functions
#generate and shuffle
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [[rank, suit] for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

#calculate hand value function
def calculate_hand_value(hand):
    value = 0
    ace_count = 0

    for card in hand:
        rank = card[0]
        if rank in ['Jack', 'Queen', 'King']:
            value += 10
        elif rank == 'Ace':
            value += 11
            ace_count += 1
        else:
            value += int(rank)

    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1

    return value

#display hand function
def display_hand(hand, player_name):
    print(f"{player_name}'s Hand: {', '.join([f'{card[0]} of {card[1]}' for card in hand])}")

#menu function
def main_menu():
    print("Blackjack by Luke\n\n1) Play Now\n2) Settings\n3) Stats\n4) Quit")
    while True:
        user_input = input("\nPlease select an option: ")

        if user_input.isdigit() and int(user_input) in [1, 2, 3, 4]:
            return int(user_input)
        else:
            print("Invalid option. Please enter 1, 2, 3 or 4.")

#settings menu function
def settings_menu():
    print("1) Change name\n2) Number Of Decks\n3) Card Count Mode\n4) Debug Mode\n5) Back To Main Menu")
    while True:
        user_input = input("\nPlease select an option: ")

        if user_input.isdigit() and int(user_input) in [1, 2, 3, 4, 5]:
            return int(user_input)
        else:
            print("Invalid option. Please enter 1, 2, 3, 4 or 5.")

#find location of .py function
def get_script_directory():
    return os.path.dirname(os.path.realpath(__file__))

#save player data function
def save_player_data(player_data, filename='player_data.json'):
    file_path = os.path.join(get_script_directory(), filename)
    with open(file_path, 'w') as file:
        json.dump(player_data, file)

#load player data function
def load_player_data(filename='player_data.json'):
    file_path = os.path.join(get_script_directory(), filename)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

#function to update biggest win/loss and highest balacne
def highest_stat_checker():
    global player_data, current_win, current_loss
    # Check and update the stats
    if current_win > player_data['biggest_win']:
        player_data['biggest_win'] = current_win

    if current_loss > player_data['biggest_loss']:
        player_data['biggest_loss'] = current_loss

    if player_data['balance'] > player_data['highest_balance']:
        player_data['highest_balance'] = player_data['balance']

#calculate true count function
def true_count_checker(hand):
    global num_decks_left, value
    
    for card in hand:
        rank = card[0]
        if rank in ['Jack', 'Queen', 'King', 'Ace', '10']:
            value -= 1
        elif rank in ['7', '8', '9']:
            value += 0
        elif rank in ['1', '2', '3', '4', '5', '6']:
            value += 1

    if num_decks_left >= 1:
        true_count = value/num_decks_left
        return true_count
    else:
        return value
    
#calculate decks left function
def number_decks_left():
    global num_decks, num_decks_left, cards_played

    original_total = num_decks * 52
    current_total = original_total - cards_played
    num_decks_left = (current_total/52)

#load player data
player_data = load_player_data()
if player_data is None:
    player_data = {'name': 'Player', 'balance': 1000, 'wins': 0, 'games_played': 0, 'highest_balance': 0, 'biggest_win': 0, 'biggest_loss': 0, 'times_bankrupt': 0, 'num_decks': 1}

quitgame = False #used for menu option 4 to quit game
card_count_mode = 2 #used to switch on and off mode
debug_mode = 2 #used to switch on and off debug mode
value = 0

# Logic
while quitgame == False:
    #initializing variables
    current_win = 0
    current_loss = 0
    play_again = 'y'
    round_count = 0
    exit_settings = False #used for settings menu navigation
    save_player_data(player_data) #save player data when you go back to the menu
    menu_option = main_menu()

    if menu_option == 1:
        #used for calculating true_count
        value = 0
        true_count = 0
        cards_played = 0 
        num_decks_left = 0
        playedcards = []

        #deck created/reset after selecting menu option 1
        num_decks = int(player_data['num_decks'])
        play_deck = []

        for _ in range(num_decks):
            deck = create_deck()
            play_deck += deck

        print(f"Your balance is: €{player_data['balance']}")

        while play_again.lower() == 'y':
            #betting
            while True:
                try:
                    bet = int(input("Enter your bet: "))
                    if bet > player_data['balance']:
                        print("You do not have enough money!")
                    else:
                        break  #exit loop if valid
                except ValueError:
                    print("Invalid input! Please enter a valid number.")

            player_hand = [play_deck.pop(), play_deck.pop()]
            dealer_hand = [play_deck.pop(), play_deck.pop()]
            cards_played += 4

            while True:
                display_hand(player_hand, player_data['name'])
                display_hand([dealer_hand[0]], "Dealer")

                player_value = calculate_hand_value(player_hand)

                #blackjack
                if player_value == 21:
                    print("Blackjack! You win!")
                    player_data['balance'] += int(bet * 1.5)
                    player_data['wins'] += 1
                    current_win = int(bet * 1.5)
                    display_hand(player_hand, player_data['name'])
                    display_hand(dealer_hand, "Dealer")
                    break

                #bust
                elif player_value > 21:
                    print("Bust! You lose!")
                    player_data['balance'] -= bet
                    save_player_data(player_data) #stop player cheating loses
                    current_loss = bet
                    display_hand(player_hand, player_data['name'])
                    display_hand(dealer_hand, "Dealer")
                    break

                #hit or stand
                action = input("Do you want to hit or stand? ").lower()

                if action in ['hit', 'h']:
                    player_hand.append(play_deck.pop())
                    cards_played += 1

                elif action in ['stand', 's']:
                    break

            #loop used to calculate win or loss when you dont bust or blackjack
            if player_value != 21 and player_value < 21:
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(play_deck.pop())
                    cards_played += 1

                display_hand(player_hand, player_data['name'])
                display_hand(dealer_hand, "Dealer")

                player_value = calculate_hand_value(player_hand)
                dealer_value = calculate_hand_value(dealer_hand)

                if player_value <= 21:
                    if player_value > dealer_value or dealer_value > 21:
                        print("You win!")
                        player_data['balance'] += bet
                        player_data['wins'] += 1
                        current_win = bet

                    elif player_value < dealer_value:
                        print("Dealer wins!")
                        player_data['balance'] -= bet
                        save_player_data(player_data) #stop player cheating loses
                        current_loss = bet

                    else:
                        print("It's a tie!")

            #update some stats
            highest_stat_checker()

            #true count calculation
            number_decks_left()
            playedcards = player_hand + dealer_hand
            true_count = true_count_checker(playedcards)

            round_count += 1
            player_data['games_played'] += 1
            print(f"Balance: €{player_data['balance']}")

            #display true count
            if (card_count_mode %2 != 0):
                print(f"The true count is: {true_count:.2f}")
            
            #display debug stats
            if (debug_mode %2 != 0):
                    print(f"Value = {value}\nNumber of deck = {num_decks}\nNumber of decks left = {num_decks_left}\nCards played = {cards_played}")

            play_again = input("Would you like to play again? (y/n): ")

            #exit game back to main menu
            if play_again.lower() != 'y':
                print(f"\nYou played {round_count} rounds, and your final balance was €{player_data['balance']}!\n")
                break

            #add money if you run out
            if (player_data['balance'] <= 0):
                print("You have gone bankrupt! Here is another €1000!")
                player_data['balance'] += 1000
                player_data['times_bankrupt'] += 1

    #settings menu
    elif menu_option == 2:
        while exit_settings == False:
            settings_option = settings_menu()

            #change name
            if settings_option == 1:
                print(f"Your current name is: {player_data['name']}")
                player_data['name'] = input("Please enter your new name: ")
        
            #change amount of decks
            if settings_option == 2:
                print(f"Your current number of decks is {player_data['num_decks']}")
                while True:
                    deck_input = input("\nPlease select between 1-8 decks: ")

                    if deck_input.isdigit() and int(deck_input) in [1, 2, 3, 4, 5, 6, 7, 8]:
                        player_data['num_decks'] = deck_input
                        break
                    else:
                        print("Invalid option.")

            #card count mode
            if settings_option == 3:
                card_count_mode += 1
                if (card_count_mode %2 == 0):
                    print("Card count mode is: Disabled")
                if (card_count_mode %2 != 0):
                    print("Card count mode is: Enabled")

            #debug mode
            if settings_option == 4:
                debug_mode += 1
                if (debug_mode %2 == 0):
                    print("Debug mode is: Disabled")
                if (debug_mode %2 != 0):
                    print("Debug mode is: Enabled")

            #exit settings
            if settings_option == 5:
                exit_settings = True

    #stats
    elif menu_option == 3:
        print(f"Wins = {player_data['wins']}")
        print(f"Games Played = {player_data['games_played']}")
        print(f"Biggest Win = {player_data['biggest_win']}")
        print(f"Biggest Loss = {player_data['biggest_loss']}")
        print(f"Highest Balance = {player_data['highest_balance']}")
        print(f"Times Bankrupt = {player_data['times_bankrupt']}\n")

    #end program
    elif menu_option == 4:
        quitgame = True

print("\n\nThanks for playing!\n\n")