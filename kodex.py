import os
import sys
import threading
import pyfiglet
import time
import itertools

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from collections import Counter
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def print_title():
    title = pyfiglet.figlet_format("    K o d e x    ", font="slant")
    print(Fore.MAGENTA + Style.BRIGHT + title)


def loading_animation(stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    print(Fore.YELLOW + "Analyzing project", end="")

    while not stop_event.is_set():
        print(f"\r{Fore.YELLOW}Analyzing project {next(spinner)}", end="")
        time.sleep(0.2)

    print("\r" + " " * 40, end="") # clear the line after the animation

def detect_language(file_path):
    try:
        lexer = get_lexer_for_filename(file_path)
        return lexer.name
    except ClassNotFound:
        return "Other"

def get_language_statistics(directory):
    language_counts = Counter()
    total_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            lang = detect_language(file_path)
            language_counts[lang] += 1
            total_files +=1

    return language_counts, total_files


def calculate_percentage(language_counts, total_files):
    percentages = {}

    if total_files > 0:
        for lang, count in language_counts.items():
            percentages[lang] = (count / total_files) * 100
    return percentages


def print_language_bars(percentages):
    max_length = 50 # Max length of the bar
    print(Fore.GREEN + "\nLanguage Usage Percentage:\n")

    for lang, percentage in percentages.items():
        bar_length = int((percentage / 100) * max_length)
        bar = '█' * bar_length
        print(f"\n{Fore.CYAN + lang.ljust(20)} {bar} {percentage: .2f}%")

def main():
    print_title()
    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python language_percentage.py <direcory_path>")
        return

    directory_path = sys.argv[1]

    if os.path.isdir(directory_path):
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()

        language_counts, total_files = get_language_statistics(directory_path)

        # Stop the loading animation
        stop_event.set()
        loading_thread.join()

        percentages = calculate_percentage(language_counts, total_files)

        print_language_bars(percentages)
    
    else:
        print(Fore.RED + "The provided path is not a valid directory.")

if __name__ == "__main__":
    main()
