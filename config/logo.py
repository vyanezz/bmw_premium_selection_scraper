import pyfiglet

def print_bmw_ascii_with_small_by():
    bmw_lines = pyfiglet.figlet_format("BMW Scraper", font="big").splitlines()
    by_text = "by vyanezz"

    padded_bmw = bmw_lines[:-1]
    last_line = bmw_lines[-1] + " " * 4 + by_text

    for line in padded_bmw:
        print(line)
    print(last_line)
