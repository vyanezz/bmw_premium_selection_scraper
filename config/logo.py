import pyfiglet

def print_start_logo():
    bmw_lines = pyfiglet.figlet_format("BMW Scraper", font="big").splitlines()
    by_text = "by vyanezz"

    padded_bmw = bmw_lines[:-1]
    last_line = bmw_lines[-1] + " " * 4 + by_text

    for line in padded_bmw:
        print(line)
    print(last_line)
