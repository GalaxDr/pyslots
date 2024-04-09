import os
import numpy as np
import json
from cryptography.fernet import Fernet
import time


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def auth_user():
    # Ask for username and password
    username = input("Username:")
    password = input("Password:")

    # Load the users
    users = load_users()

    # Check if username and password are correct
    if username in users:
        if password == users[username]["password"]:
            print("Login successful!")
            return username
        else:
            print("Password incorrect!")
            return auth_user()
    else:
        print("Username not found!")
        return auth_user()


def load_users():
    encryption_key = os.getenv("KEY")
    with open("users_encrypted.json", "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = decrypt_data(encrypted_data, encryption_key)
    json_data = json.loads(decrypted_data)
    return json_data


def decrypt_data(cipher_text, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text


def check_balance(username):
    # Check the balance
    users = load_users()
    balance = users[username]["balance"]
    return balance


def update_balance(username, balance):
    # Update the balance
    users = load_users()
    users[username]["balance"] = balance
    print(f"Your new balance is {balance}")
    # Write the updated user data back to the file
    encryption_key = os.getenv("KEY")
    with open("users_encrypted.json", "wb") as encrypted_file:
        encrypted_data = encrypt_data(json.dumps(users), encryption_key)
        encrypted_file.write(encrypted_data)


def print_symbol(symbol):
    if symbol in ["Cherry", "Lemon", "Orange", "Plum", "Bell", "Bar", "Seven"]:
        print(symbol, end="")
    else:
        print("Invalid symbol")


def print_symbols_3x3(reel):
    for i in range(3):
        for j in range(3):
            print_symbol(reel[i][j])  # Corrigindo a chamada da função
            if j < 2:
                print(" | ", end="")  # Adicionando a barra vertical entre os símbolos e espaçamento
        print()  # Quebra de linha após cada linha de símbolos
        if i < 2:
            print(" --- " * 3)


def play_slot_machine(authenticated_user, balance):
    users = load_users()
    # Define bet
    bet = input("Bet amount:")
    # Check if bet is valid
    if int(bet) > balance:
        print("Bet is higher than balance!")
        return play_slot_machine(authenticated_user, balance)
    elif int(bet) <= 0:
        print("Bet is lower than 0!")
        return play_slot_machine(authenticated_user, balance)

    # Define the symbols
    symbols = ['Cherry', 'Lemon', 'Orange', 'Plum', 'Bell', 'Bar', 'Seven']

    # Spin the reels
    reel = np.random.choice(symbols, size=9, replace=True)

    # Reshape the array to 3x3
    reel = reel.reshape(3, 3)

    # Print the result
    # print(reel)

    # Select method of winning
    win_method = select_win_method()

    print_symbols_3x3(reel)

    final_bet = check_win(reel, win_method, bet)
    # Update the balance
    balance = balance + final_bet

    update_balance(authenticated_user, balance)

    choice = input("Play again? (y/n)")
    if choice == "y":
        play_slot_machine(authenticated_user, balance)
    else:
        print("Thanks for playing!")


def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text


def select_win_method():
    # Select method of winning
    # 1. Horizontal line
    # 2. Diagonal line
    # 3. Vertical line
    print("1 - Horizontal line")
    print("2 - Diagonal line")
    print("3 - Vertical line")
    win_method = input("Select a method of winning:")
    match win_method:
        case "1":
            print("Horizontal line")
            return win_method
        case "2":
            print("Diagonal line")
            return win_method
        case "3":
            print("Vertical line")
            return win_method
        case _:
            print("Invalid input")
            return select_win_method()


def check_win(reel, win_method, bet):
    # Check for win
    won = 0
    payout_multiplier = 0

    for i in range(3):
        if win_method == "3":
            if reel[0, i] == reel[1, i] == reel[2, i]:
                won += 1
                payout_multiplier = 2
        elif win_method == "2":
            if reel[0, 0] == reel[1, 1] == reel[2, 2] or reel[0, 2] == reel[1, 1] == reel[2, 0]:
                won += 1
                payout_multiplier = 3
        elif win_method == "1":
            if reel[i, 0] == reel[i, 1] == reel[i, 2]:
                won += 1
                payout_multiplier = 4

    if won == 0:
        print("You lose!")
        return -int(bet)
    else:
        print(f"You win {won} times!")
        return int(bet) * payout_multiplier * won


def pick_card(deck):
    # Pick a card
    card = np.random.choice(list(deck.keys()))
    # Return the card
    return card


def print_card(deck, card):
    print(deck[card])


def play_again(authenticated_user, balance):
    input1 = input("Play again? (y/n)")
    if input1 == "y":
        play_blackjack(authenticated_user, balance)
    else:
        print("Thanks for playing!")
        exit()


def hit_or_stand():
    response = input("Would you like to hit or stand?")
    while response not in ["hit", "stand", "h", "s"]:
        print("Invalid input!")
        response = input("Would you like to hit or stand?")
    return response


def play_blackjack(authenticated_user, balance):
    # Define bet
    bet = input("Bet amount:")
    if int(bet) > balance:
        print("Bet is higher than balance!")
        return play_blackjack(authenticated_user, balance)
    elif int(bet) <= 0:
        print("Bet is lower than 0!")
        return play_blackjack(authenticated_user, balance)
    # Define the deck
    deck = {1:
                "   _____\n" +
                "  |A _  |\n" +
                "  | ( ) |\n" +
                "  |(_'_)|\n" +
                "  |  |  |\n" +
                "  |____V|\n",

            2:

                "   _____\n" +
                "  |2    |\n" +
                "  |  o  |\n" +
                "  |     |\n" +
                "  |  o  |\n" +
                "  |____Z|\n",

            3:
                "   _____\n" +
                "  |3    |\n" +
                "  | o o |\n" +
                "  |     |\n" +
                "  |  o  |\n" +
                "  |____E|\n",

            4:
                "   _____\n" +
                "  |4    |\n" +
                "  | o o |\n" +
                "  |     |\n" +
                "  | o o |\n" +
                "  |____h|\n",

            5:
                "   _____ \n" +
                "  |5    |\n" +
                "  | o o |\n" +
                "  |  o  |\n" +
                "  | o o |\n" +
                "  |____S|\n",

            6:
                "   _____ \n" +
                "  |6    |\n" +
                "  | o o |\n" +
                "  | o o |\n" +
                "  | o o |\n" +
                "  |____6|\n",

            7:

                "   _____ \n" +
                "  |7    |\n" +
                "  | o o |\n" +
                "  |o o o|\n" +
                "  | o o |\n" +
                "  |____7|\n",

            8:

                "   _____ \n" +
                "  |8    |\n" +
                "  |o o o|\n" +
                "  | o o |\n" +
                "  |o o o|\n" +
                "  |____8|\n",

            9:
                "   _____ \n" +
                "  |9    |\n" +
                "  |o o o|\n" +
                "  |o o o|\n" +
                "  |o o o|\n" +
                "  |____9|\n",

            10:
                "   _____ \n" +
                "  |10  o|\n" +
                "  |o o o|\n" +
                "  |o o o|\n" +
                "  |o o o|\n" +
                "  |___10|\n",

            11:

                "   _____\n" +
                "  |J  ww|\n" +
                "  | o {)|\n" +
                "  |o o% |\n" +
                "  | | % |\n" +
                "  |__%%[|\n",

            12:

                "   _____\n" +
                "  |Q  ww|\n" +
                "  | o {(|\n" +
                "  |o o%%|\n" +
                "  | |%%%|\n" +
                "  |_%%%O|\n",

            13:
                "   _____\n" +
                "  |K  WW|\n" +
                "  | o {)|\n" +
                "  |o o%%|\n" +
                "  | |%%%|\n" +
                "  |_%%%>|\n"
            }

    # Deal the cards
    user_card1 = pick_card(deck)
    user_card2 = pick_card(deck)
    total = sum_cards([min(user_card1, 10), min(user_card2, 10)])
    print_card(deck, user_card1)
    time.sleep(2)
    print_card(deck, user_card2)
    print(f"You get a {min(user_card1, 10)} and a {min(user_card2, 10)}")
    print(f"Your total is {total}")
    time.sleep(2)
    dealer_card1 = pick_card(deck)
    time.sleep(2)
    dealer_card2 = pick_card(deck)
    print_card(deck, dealer_card1)
    print(f"The dealer gets a {min(dealer_card1, 10)} and a has a hidden card {card_face_down()}")
    print(f"The dealer's total is hidden")

    # Ask for hit or stand
    time.sleep(1)
    response = hit_or_stand()
    while response in ["hit", "h"]:
        card = pick_card(deck)
        print(f"You choose to hit and get a {min(card, 10)}")
        time.sleep(1)
        print_card(deck, card)
        total += sum_cards([card])
        print(f"Your total is {total}")
        if total > 21:
            print("You busted!")
            balance = balance - int(bet)
            update_balance(authenticated_user, balance)
            play_again(authenticated_user, balance)
        response = hit_or_stand()

    print("Okay, dealer's turn.")
    print(f"The dealer's hidden card was")
    time.sleep(2)
    print_card(deck, dealer_card2)
    dealer_total = sum_cards([dealer_card1, dealer_card2])
    print(f"The dealer's total is {dealer_total}")
    while dealer_total < 17 and dealer_total < total:
        card = pick_card(deck)
        print(f"The dealer choose to hit and gets a {card}")
        dealer_total += sum_cards([card])
        print(f"The dealer's total is {dealer_total}")
        input("Press enter to continue")
        if dealer_total > 21:
            print("The dealer busted!")
            balance = balance + int(bet)
            update_balance(authenticated_user, balance)
            play_again(authenticated_user, balance)
    if total < dealer_total <= 21:
        print("The dealer wins!")
        balance = balance - int(bet)
        update_balance(authenticated_user, balance)
        play_again(authenticated_user, balance)
    elif dealer_total < total:
        print("You win!")
        balance = balance + int(bet)
        update_balance(authenticated_user, balance)
        play_again(authenticated_user, balance)
    else:
        print("It's a tie!")
        play_again(authenticated_user, balance)


def card_face_down():
    return "\n   _____\n" + \
        "  |/////|\n" + \
        "  |/////|\n" + \
        "  |/////|\n" + \
        "  |/////|\n" + \
        "  |/////|\n"


def sum_cards(cards):
    # Sum the cards
    total = 0
    for card in cards:
        if card in [11, 12, 13]:
            total += 10
        else:
            total += int(card)
    return total


def play_roulette(authenticated_user, balance):
    # Define the wheel
    wheel = np.arange(0, 37)
    # Shuffle the wheel
    np.random.shuffle(wheel)
    # Deal the ball
    ball = wheel[0]
    # Print the ball
    print(f"The ball is {ball}")
    # Ask for bet
    bet = input("Bet on a number (0-36), even (e), odd (o), red (r), black (b), low (l), high (h):")
    # Check if bet is valid
    if bet not in ["0", "00", "e", "o", "r", "b", "l", "h"] and int(bet) not in wheel:
        print("Invalid bet!")
        return play_roulette()
    # Check if bet is a number
    if bet in ["0", "00", "e", "o", "r", "b", "l", "h"]:
        # Check if player has won
        if bet == "e" and ball % 2 == 0 or bet == "o" and ball % 2 == 1:
            print("You win!")
            return 2
        elif bet == "r" and ball in [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34,
                                     36] or bet == "b" and ball in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 29,
                                                                    31, 33, 35]:
            print("You win!")
            return 2
        elif bet == "l" and ball in range(1, 19) or bet == "h" and ball in range(19, 37):
            print("You win!")
            return 2
        else:
            print("You lose!")
            return 0
    else:
        # Check if player has won
        if int(bet) == ball:
            print("You win!")
            return 36
        else:
            print("You lose!")
            return 0


def main():
    authenticated_user = auth_user()
    balance = check_balance(authenticated_user)
    time.sleep(2)
    cls()
    print(f"Welcome {authenticated_user}!")
    print(f"Your balance is {balance}")
    print("What game do you want to play?")
    print("1 - Slot machine")
    print("2 - Blackjack")
    print("3 - Roulette")
    game = input("Select a game:")
    cls()
    if game == "1":
        play_slot_machine(authenticated_user, balance)
    elif game == "2":
        play_blackjack(authenticated_user, balance)
    elif game == "3":
        play_roulette(authenticated_user, balance)
    else:
        print("Invalid input")


# Run the game
if __name__ == "__main__":
    main()
