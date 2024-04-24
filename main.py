import random

MAX_LINES = 3
MAX_BET = 200
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_values = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def check_winnings(columns, lines, bet, values): #for simplicity, betting on # of lines chooses top to bottom, so 1 line only checks top row
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_ckeck = column[line]
            if symbol != symbol_to_ckeck:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

def spin_slot_machine(rows, cols, symbols): #generates spin results
    all_symbols = []
    for symbol, symbol_count in symbols.items(): #this loop directly accesses key and value in a tuple and unpacks them directly
        for _ in range(symbol_count): # _ is an anonymous variable used to loop when you don't care about the iteration count
            all_symbols.append(symbol)

    columns = [] # 3x3 matrix, example [[A A B], [A C D], [A B D]] so 1st row A A A 2nd row A C B 3rd row B D D
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:] #slice operator, copies the list instead of refering to it, since we'll be removing selected symbols from the pool
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])): #manual transpose of the matrix (switch values in columns and rows)
        for i, column in enumerate(columns): #enumerate gives the index stored in "i" while value goes in "column"
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row])

def deposit():
    while True:
        amount = input("Deposit amount? $:")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount

def get_number_of_lines():
    while True:
        lines = input("Lines to bet (1-" + str(MAX_LINES) + "):")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Lines must be within range.")
        else:
            print("Please enter a number.")
    return lines

def get_bet():
    while True:
        amount = input("Bet amount per line? $:")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between {MIN_BET} and {MAX_BET}")
        else:
            print("Please enter a number.")
    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Insufficient balance(${balance}) to make bet(${total_bet})")
        else:
            break

    print(f"Bet is ${bet} on {lines} for a total of ${total_bet}.")

    slots = spin_slot_machine(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    print(f"You won {winnings}.")
    print(f"You won on lines: ", *winning_lines)  # * - splat / unpack operator, passes every value from list
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
        if balance <= 0:
            print("Ran out of cash! Game over.")
            break

    print(f"You left with ${balance}")

main()