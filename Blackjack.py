import random

play_again = 'y'
balance = 100
round_count = 0

def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [[rank, suit] for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

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

def display_hand(hand, player_name):
    print(f"{player_name}'s Hand: {', '.join([f'{card[0]} of {card[1]}' for card in hand])}")

print(f"Your balance is: €{balance}")

while play_again.lower() == 'y':
    bet = int(input("Please input your bet: "))
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    while True:
        display_hand(player_hand, "Player")
        display_hand([dealer_hand[0]], "Dealer")

        player_value = calculate_hand_value(player_hand)

        if player_value == 21:
            print("Blackjack! You win!")
            balance += int(bet * 1.5)
            break

        elif player_value > 21:
            print("Bust! You lose!")
            balance -= bet
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
                balance += bet

            elif player_value < dealer_value:
                print("Dealer wins!")
                balance -= bet

            else:
                print("It's a tie!")

    round_count += 1
    print(f"Balance: €{balance}")
    play_again = input("Would you like to play again? (y/n): ")

print(f"Thanks for playing! You played {round_count} rounds, and your final balance was €{balance}!")
