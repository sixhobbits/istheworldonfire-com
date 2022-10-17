import os 
import sys
import urllib.parse

START_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.xz.style/serve/inter.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css">
    <title>Is the world on fire? | {}</title>
</head>
<body>
    <h1>Yes {} is on fire</h1>
"""

def create_page(country, fires):
    page = START_TEMPLATE.format(country, country)
    for fire_name, fire_url in fires:
        page += f"\n<p><a href={fire_url}>{fire_name}</a></p>"
    page += "</body></html>"
    return page

def process_country(country_block):
    i = 0
    lines = country_block.strip().split("\n")
    country = lines[0]
    fires = []
    while True:
        try:
            i += 1
            fire_name = lines[i]
            i += 1
            fire_url = lines[i]
            fires.append((fire_name, fire_url))
        except IndexError:
            break
    return country, fires

def save_country(country, page):
    if not os.path.exists(country):
        os.mkdir(country)
        with open(f"{country}/index.html", "w") as f:
            f.write(page)

def generate_and_save_index(countries):
    page = START_TEMPLATE.format("the World", "the World")
    page += "\n <p>🔥🔥🔥🔥</p>"
    page += '\n<p><a href="https://en.wikipedia.org/wiki/2022_food_crises">2022 food crises</a>'
    page += '\n<p><a href="https://en.wikipedia.org/wiki/2022_Russian_invasion_of_Ukraine">Ukraine war</a>'

    page += "\n<h3>Or check if individual countries are burning by clicking on the links below</h3>"
    page += f'\n<p>Want to add to the list? Contribute <a href="https://github.com/sixhobbits/istheworldonfire-com">on GitHub</a>.</p>'
    for country in countries:
        country_quoted = urllib.parse.quote(country)
        page += f"\n<p><a href={country_quoted}>{country}</a></p>"
    page += "</body></html>"
    with open("index.html", "w") as f:
        f.write(page)


def run():
    with open("fires.itwof") as f:
        s = f.read().strip()
    blocks = s.split("\n\n")
    countries = []
    for block in blocks:
        country, fires = process_country(block)
        countries.append(country)
        page = create_page(country, fires)
        save_country(country, page)
    generate_and_save_index(countries)


def run_tests():
    print("testing create_page")
    page = create_page("Ukraine", [("Fire1", "https://example.com"), ("Fire 2", "https://example.com")])
    print(page)

    print("testing process_coutry")
    russia = """Russia
Mobilization
https://en.wikipedia.org/wiki/2022_Russian_mobilization
International Sanctions
https://en.wikipedia.org/wiki/International_sanctions_during_the_Russo-Ukrainian_War"""
    country, fires = process_country(russia)
    print(country, fires)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run()
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        run_tests()






