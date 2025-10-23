# TODO create a number guessing game that runs through the main() function
import random, time, math, msvcrt, sys
from contextlib import nullcontext

print("Welcome to Number Guesser")
print("\n Made by, Rivith Uyangoda")

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f"Time left: {timer}", end="\r")
        time.sleep(1)
        t -= 1
    print("\n⏰ *Alarm Noises* Time’s up!")
    return False


def save_round_data(name, difficulty, result, number, elapsed_time, guesses_used, total_guesses):
    try:
        with open("data.txt", "a") as file:
            file.write(f"{name},{difficulty},{result},{number},{elapsed_time:.2f},{guesses_used}/{total_guesses}\n")
    except Exception as e:
        print(f"⚠️ Error saving data: {e}")


def get_name():
    name = input("\nWhat is your name? ")
    while not name.isalpha():
        name = input("\nInvalid name. Try again: ")
    try:
        with open('names.txt', 'r+') as file:
            names = [line.strip() for line in file.readlines()]
            if name not in names:
                file.write(name + '\n')
                print(f"\nNew name '{name}' saved.")
            if name == "Rivith":
                print("\nRivith's name is too long. Try again.")
                print("\nJk, all system's are up and running (definitely not a print statement).")
            elif name == "Jonathan" or "Derpak":
                print("\nAccess Denied. Please give student A to continue")
                print("\nJK (but please do)")
            else:
                print(f"\nWelcome back, {name}!")
    except FileNotFoundError:
        with open('names.txt', 'w') as file:
            file.write(name + '\n')
            print(f"\nNew name '{name}' saved.")
    return name


def show_past_games(player):
    try:
        with open("data.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                print("\n📭 No past games found.")
                return
            print("\n📜 Game History:")
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue
                name, diff, result, num, time_used, guesses = parts
                if name == player:
                    print(
                    f"Name - {name} | Difficulty - {diff} | Win/Lose - {result} | Number - {num} | Time - {time_used}s | Guesses - {guesses}")
    except FileNotFoundError:
        print("\n No past games found.")


def readline(player):
    best_scores = {}  # {name: {difficulty: (percent_used, time_used, line)}}

    try:
        with open("data.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue

                name, diff, result, num, time_used, guesses = parts
                if name != player:
                    continue
                try:
                    used, total = guesses.split("/")
                    used, total = int(used), int(total)
                except (ValueError, IndexError):
                    continue

                try:
                    time_used = float(time_used)
                except ValueError:
                    continue

                percent_used = (used / total) * 100 if total > 0 else 100

                if name not in best_scores:
                    best_scores[name] = {}

                if diff not in best_scores[name]:
                    best_scores[name][diff] = (percent_used, time_used, line.strip())
                else:
                    best_p, best_t, _ = best_scores[name][diff]
                    if percent_used < best_p or (percent_used == best_p and time_used < best_t):
                        best_scores[name][diff] = (percent_used, time_used, line.strip())

        if not best_scores:
            print("⚠️ No valid scores found.")
            return {}

        for name, diffs in best_scores.items():
            print(f"\n{name}'s Personal Bests:")
            for diff, (p, t, record) in diffs.items():
                print(f"  {diff}: {record} | Percent of guesses used: {p:.1f}% | Time: {t:.2f}s")

        return best_scores

    except FileNotFoundError:
        print("⚠️ No past games found.")
        return {}

def num_creator(g_min, g_max, range_min, range_max):
    guesses = random.randint(g_min, g_max)
    first_num = second_num =  0
    while abs(second_num - first_num) < range_min:
        first_num = random.randint(1, range_max)
        second_num = random.randint(1, range_max)
    if first_num > second_num:
        first_num, second_num = second_num, first_num
    print(f"\nYour random number range is: {first_num} - {second_num}")
    print(f"\nYou have {guesses} guesses.")
    return guesses, first_num, second_num
def singleplayer(player):
    difficulty = input("\nPick a difficulty \nE=Easy \nM=Medium \nH=Hard \nI=Insane \n\n").strip().capitalize()
    if difficulty in ["E", "Easy", "1", "e",'easy']:
        guesses, first_num, second_num = num_creator(13, 17, 100, 1000)
        t = 60
    elif difficulty in ["M", "Medium", "2", 'm', 'medium']:
        guesses, first_num, second_num = num_creator(8, 12, 500, 10000)
        t = 70
    elif difficulty in ["H", "Hard", "3", 'h', "hard"]:
        guesses, first_num, second_num = num_creator(5, 9, 1500, 100000)
        t = 90
    elif difficulty in ["I", "Insane", "4", 'i', "insane"]:
        guesses, first_num, second_num = num_creator(3, 5, 10000, 10 ** 18)
        t = 40
    else:
        print("\nInvalid difficulty")
        return
    number = random.randint(first_num, second_num)
    start_time = time.perf_counter()
    print(f"\nAlright {player}, start guessing!")
    total_guesses = guesses
    while guesses > 0:
        elapsed = time.perf_counter() - start_time
        remaining = int(t - elapsed)
        if remaining <= 0:
            print("\n⏰ Time’s up! You ran out of time!")
            break
        print(f"\nGuesses left: {guesses} | Time left: {remaining}s | Range {first_num} - {second_num}")
        guess = input("\nGuess a number: ")
        elapsed = time.perf_counter() - start_time
        if elapsed >= t:
            print("\n⏰ Time’s up! You ran out of time!")
            print(f"\nYou lost! The number was {number}.")
            break
        if guess == '2010':
            print(f"\nThe number was {number}.")
        if not guess.isdigit() or not (first_num <= int(guess) <= second_num):
            print("\nPlease enter a valid number.")
            continue
        guess = int(guess)
        guesses -= 1
        if guess == number:
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            save_round_data(player, difficulty, "Win", number, elapsed_time, total_guesses - guesses, total_guesses)
            print(f"\n✅ Correct! You got it in {elapsed_time:.2f} seconds.")
            break
        elif guess > number:
            print(f"\nToo high!")
        elif guess < number:
            print(f"\nToo low!")
    else:
        print(f"\nYou lost! The number was {number}.")
    end_time = time.perf_counter()
    print(f"\nElapsed time: {end_time - start_time:.2f} seconds")
    elapsed_time = end_time - start_time
    save_round_data(player, difficulty, "Lose", number, elapsed_time, total_guesses, total_guesses)
    readline(player)
    time.sleep(1.5)
def multiplayer(player):
    players = {}
    while True:
        player_count = input("\nHow many players do you have? ")

        if not player_count.isdigit() or int(player_count) <= 0:
            print("\n❌ Please enter a valid positive number.")
            continue

        player_count = int(player_count)
        print(f"\n👥 Setting up {player_count} players...")

        for i in range(player_count):
            while True:
                name = get_name()
                if name in players:
                    print(f"\n⚠️ The name '{name}' is already used. Please enter a different name.")
                    continue
                players[name] = i + 1
                print(f"✅ Player {i + 1} registered: {name}")
                break
        break

    # --- Select difficulty ONCE for all players ---
    while True:
        difficulty = input("\nPick a difficulty for everyone \nE=Easy \nM=Medium \nH=Hard \nI=Insane \n\n").strip().capitalize()
        if difficulty in ["E", "Easy", "1", "e", "easy"]:
            guesses, first_num, second_num = num_creator(13, 17, 100, 1000)
            t = 60
        elif difficulty in ["M", "Medium", "2", "m", "medium"]:
            guesses, first_num, second_num = num_creator(8, 12, 500, 10000)
            t = 70
        elif difficulty in ["H", "Hard", "3", "h", "hard"]:
            guesses, first_num, second_num = num_creator(5, 9, 1500, 100000)
            t = 90
        elif difficulty in ["I", "Insane", "4", "i", "insane"]:
            guesses, first_num, second_num = num_creator(3, 5, 10000, 10 ** 18)
            t = 40
        else:
            print("\nInvalid difficulty")
            continue
        break

    print("\n🎮 Let’s begin the multiplayer match!\n")

    # --- Each player takes a turn ---
    for player in players:
        print(f"\n▶️ {player}'s turn begins!")
        number = random.randint(first_num, second_num)
        total_guesses = guesses
        start_time = time.perf_counter()
        remaining = t

        while guesses > 0:
            elapsed = time.perf_counter() - start_time
            remaining = int(t - elapsed)
            if remaining <= 0:
                print("\n⏰ Time’s up! You ran out of time!")
                break

            print(f"\n{player} → Guesses left: {guesses} | Time left: {remaining}s | Range: {first_num} - {second_num}")
            guess = input(f"{player}, enter your guess: ")

            if elapsed >= t:
                print("\n⏰ Time’s up! You ran out of time!")
                print(f"You lost! The number was {number}.")
                break

            if not guess.isdigit() or not (first_num <= int(guess) <= second_num):
                print("\n❌ Please enter a valid number.")
                continue

            guess = int(guess)
            guesses -= 1

            if guess == number:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                save_round_data(player, difficulty, "Win", number, elapsed_time, total_guesses - guesses, total_guesses)
                print(f"\n✅ {player} guessed correctly in {elapsed_time:.2f}s!")
                break
            elif guess > number:
                print("Too high!")
            else:
                print("Too low!")
        else:
            print(f"\n{player} lost! The number was {number}.")
            elapsed_time = time.perf_counter() - start_time
            save_round_data(player, difficulty, "Lose", number, elapsed_time, total_guesses, total_guesses)

        guesses, _, _ = num_creator(13, 17, 100, 1000)  # reset guesses for next player (can vary by diff)
        print(f"\n🔹 {player}'s turn is over.")
        readline(player)
        time.sleep(1.5)

    print("\n🏁 All players have finished their rounds!")







def main():
    player = get_name()
    play_again = "null"
    callback = False
    while True:
        choice = input("\nType '1' to Play, '2' to View Past Games, or anything else to Quit: ").strip()
        if choice == "2":
            show_past_games(player)
            continue
        elif choice != "1":
            print("\nGoodbye!")
            return
        play_mode = input("1. Singleplayer (S) \n2. Multiplayer (M): ").strip()
        if play_mode in ["S", "1" , "s","single", "singleplayer", "Singleplayer", "Single", "single player", "Single player"]:
            singleplayer(player)
        elif play_mode in ["M", "m", "2"]:
            multiplayer(player)
        play_again = input("\nPress Enter to play again or type anything else (and enter) to quit: ")
        if play_again == "":
            continue
        else:
            sys.exit("\nTerminating")
            break


if __name__ == "__main__":
    main()
