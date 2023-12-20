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
            print("Invalid option. Please enter 1, 2, or 3.")

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

def highest_stat_checker():
    global player_data, current_win, current_loss
    # Check and update the stats
    if current_win > player_data['biggest_win']:
        player_data['biggest_win'] = current_win

    if current_loss > player_data['biggest_loss']:
        player_data['biggest_loss'] = current_loss

    if player_data['balance'] > player_data['highest_balance']:
        player_data['highest_balance'] = player_data['balance']


#load player data
player_data = load_player_data()
if player_data is None:
    player_data = {'name': 'Player', 'balance': 1000, 'wins': 0, 'games_played': 0, 'highest_balance': 0, 'biggest_win': 0, 'biggest_loss': 0}

quitgame = False #used for menu option 4 to quit game
# Logic
while quitgame == False:
    #initializing variables
    current_win = 0
    current_loss = 0
    play_again = 'y'
    round_count = 0
    save_player_data(player_data) #save player data when you go back to the menu
    menu_option = main_menu()

    if menu_option == 1:
        print(f"Your balance is: €{player_data['balance']}")
        while play_again.lower() == 'y':
            bet = int(input("Please input your bet: "))
            deck = create_deck()
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            while True:
                display_hand(player_hand, player_data['name'])
                display_hand([dealer_hand[0]], "Dealer")

                player_value = calculate_hand_value(player_hand)

                if player_value == 21:
                    print("Blackjack! You win!")
                    player_data['balance'] += int(bet * 1.5)
                    player_data['wins'] += 1
                    current_win = int(bet * 1.5)
                    break

                elif player_value > 21:
                    print("Bust! You lose!")
                    player_data['balance'] -= bet
                    current_loss = bet
                    break

                action = input("Do you want to hit or stand? ").lower()

                if action in ['hit', 'h']:
                    player_hand.append(deck.pop())

                elif action in ['stand', 's']:
                    break

            if player_value != 21 and player_value < 21:
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())

                display_hand(player_hand, "Player")
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
                        current_loss = bet

                    else:
                        print("It's a tie!")

            highest_stat_checker()
            round_count += 1
            player_data['games_played'] += 1
            print(f"Balance: €{player_data['balance']}")

            play_again = input("Would you like to play again? (y/n): ")

            if play_again.lower() != 'y':
                print(f"\nYou played {round_count} rounds, and your final balance was €{player_data['balance']}!\n")
                break

    elif menu_option == 2:
        print(f"Your current name is: {player_data['name']}")
        player_data['name'] = input("Please enter your new name: ")

    elif menu_option == 3:
        print(f"Wins = {player_data['wins']}")
        print(f"Games played = {player_data['games_played']}")
        print(f"Biggest Win = {player_data['biggest_win']}")
        print(f"Biggest Loss = {player_data['biggest_loss']}")
        print(f"Highest Balance = {player_data['highest_balance']}\n")

    elif menu_option == 4:
        quitgame = True

print("\n\nThanks for playing!")