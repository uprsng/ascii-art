#!/usr/bin/env python3
"""Interactive ASCII Art Generator — type words, pick fonts & colors."""

import pyfiglet
import colorama
from colorama import Fore, Style
import random

colorama.init()

COLORS = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
}

FEATURED_FONTS = [
    "banner3-D", "block", "bulbhead", "colossal", "doom",
    "epic", "isometric1", "larry3d", "puffy", "slant",
    "speed", "starwars", "stop", "univers",
]


def list_fonts():
    fonts = pyfiglet.FigletFont.getFonts()
    print(f"\n{Fore.CYAN}Featured fonts:{Style.RESET_ALL}")
    cols = 4
    for i in range(0, len(FEATURED_FONTS), cols):
        row = FEATURED_FONTS[i:i+cols]
        print("  " + "  ".join(f"{f:<20}" for f in row))
    print(f"\n{Fore.CYAN}All available fonts ({len(fonts)} total):{Style.RESET_ALL}")
    for i in range(0, min(len(fonts), 80), cols):
        row = fonts[i:i+cols]
        print("  " + "  ".join(f"{f:<20}" for f in row))
    if len(fonts) > 80:
        print(f"  ... and {len(fonts) - 80} more. See pyfiglet docs for full list.")


def rainbow(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    result = []
    color_idx = 0
    for ch in text:
        if ch != " ":
            result.append(colors[color_idx % len(colors)] + ch)
            color_idx += 1
        else:
            result.append(ch)
    return "".join(result) + Style.RESET_ALL


def render(text, font, color):
    try:
        art = pyfiglet.figlet_format(text, font=font)
    except pyfiglet.FontNotFound:
        print(f"{Fore.RED}Font '{font}' not found. Try 'fonts' to see options.{Style.RESET_ALL}")
        return

    if color == "rainbow":
        for line in art.splitlines():
            print(rainbow(line))
    else:
        c = COLORS.get(color, Fore.WHITE)
        print(c + art + Style.RESET_ALL)


def print_help():
    print(f"""
{Fore.CYAN}Commands:{Style.RESET_ALL}
  <text>                render with current font & color
  font <name>           switch font  (e.g. {Fore.YELLOW}font doom{Style.RESET_ALL})
  color <name>          switch color (e.g. {Fore.YELLOW}color cyan{Style.RESET_ALL})
  random                render last text with a random font & color
  fonts                 list available fonts
  colors                list available colors
  help                  show this message
  quit / exit           exit

{Fore.CYAN}Colors:{Style.RESET_ALL}  {" ".join(COLORS.keys())}  rainbow
""")


def main():
    print(f"\n{Fore.MAGENTA}{pyfiglet.figlet_format('ASCII Art', font='slant')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Welcome! Type a word to render it. Type 'help' for commands.{Style.RESET_ALL}\n")

    current_font = "doom"
    current_color = "cyan"
    last_text = "Hello"

    render(last_text, current_font, current_color)

    while True:
        try:
            raw = input(f"{Fore.YELLOW}[{current_font} / {current_color}]>{Style.RESET_ALL} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}Bye!{Style.RESET_ALL}")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()

        if cmd in ("quit", "exit"):
            print(f"{Fore.CYAN}Bye!{Style.RESET_ALL}")
            break
        elif cmd == "help":
            print_help()
        elif cmd == "fonts":
            list_fonts()
        elif cmd == "colors":
            print(f"\n{Fore.CYAN}Colors:{Style.RESET_ALL}  {' '.join(COLORS.keys())}  rainbow\n")
        elif cmd == "font" and len(parts) == 2:
            current_font = parts[1].strip()
            print(f"{Fore.GREEN}Font set to '{current_font}'{Style.RESET_ALL}")
            render(last_text, current_font, current_color)
        elif cmd == "color" and len(parts) == 2:
            c = parts[1].strip().lower()
            if c in COLORS or c == "rainbow":
                current_color = c
                print(f"{Fore.GREEN}Color set to '{current_color}'{Style.RESET_ALL}")
                render(last_text, current_font, current_color)
            else:
                print(f"{Fore.RED}Unknown color. Options: {' '.join(COLORS.keys())} rainbow{Style.RESET_ALL}")
        elif cmd == "random":
            current_font = random.choice(FEATURED_FONTS)
            current_color = random.choice(list(COLORS.keys()) + ["rainbow"])
            print(f"{Fore.GREEN}Random: font={current_font}, color={current_color}{Style.RESET_ALL}")
            render(last_text, current_font, current_color)
        else:
            last_text = raw
            render(last_text, current_font, current_color)


if __name__ == "__main__":
    main()
