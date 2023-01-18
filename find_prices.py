import requests
from bs4 import BeautifulSoup


#   Accepts a user-specified game name
def find_game_prices(user_game_name):

    #   This is the name of the game in the format game+name for the request url
    combine_name = create_game_combine(user_game_name)

    #   The function returns the name of the game, the names of the stores, and the prices of the game.
    return {
            "Game Name": f"{user_game_name}",
            "Gamers Gate": g_gate_find_price(combine_name.lower(), user_game_name),
            "Games Planet": g_planet_find_price(combine_name.lower(), user_game_name),
            "Win Game Store": win_g_find_price(combine_name.lower(), user_game_name),
            "MMOGA": mmoga_find_price(combine_name.lower()),
            "YU PLAY": yu_play_find_price(combine_name.lower()),
            "Punktid": punktid_find_price(combine_name.lower(), user_game_name),
            "Games for play": g_for_play(combine_name.lower())
            }


#   The function creates the name of the game in the format game+name for the request url
def create_game_combine(game_name):
    combine_name = game_name.replace(" ", "+").replace(":", "").replace("'", "").replace(",", "").replace("&", "")

    return combine_name


#   The function looks up the price of a game in the Gamers Gate store
def g_gate_find_price(game, final_game_name):
    try:
        url = f"https://www.gamersgate.com/games/?query={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        games = soup.findAll("div", class_="column catalog-item product--item")

        point = 0

        for game in games:
            game_name = game.get("data-name")
            if game_name == final_game_name:
                price = f"{game.get('data-price')}$"
                point += 1
                return price
        if point == 0:
            price = "Game not found."

            return price

    except Exception:
        return "Something went wrong."


#   The function looks up the price of a game in the Games Planet store
def g_planet_find_price(game, final_game_name):
    try:
        url = f"https://us.gamesplanet.com/search?query={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        games = soup.findAll("a", class_="d-block text-decoration-none stretched-link")

        point = 0
        for i in games:
            if i.text == final_game_name:
                prices = soup.find("span", class_="price_current")
                point += 1
                price = f"{prices.text.split('$')[1]}$"
                return price

        if point == 0:
            return "Game not found."

    except Exception:
        return "Something went wrong."


#   The function looks up the price of a game in the Win Game Store
def win_g_find_price(game, final_game_name):
    try:
        url = f"https://www.wingamestore.com/search/?SearchWord={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        price_c = soup.find("span", class_="price").text

        try:
            gn_link = soup.find("a", class_="atitle").text

            if gn_link[0] == final_game_name[0]:
                price = f"{price_c.split('$')[1]}$"
            else:
                price = "Game not found."

            return price

        except AttributeError:
            gn_link = soup.find("div", class_="boxhole img16x9").get("title")

            if gn_link[0] == final_game_name[0]:
                price = f"{price_c.split('$')[1]}$"
            else:
                price = "Game not found."

            return price

    except Exception:
        return "Something went wrong."


#   The function looks up the price of a game in the Games For Play store
def g_for_play(game):
    try:
        url = f"https://gamesforplay.com/index.php?route=product/search&search={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        try:
            games = soup.find("span", class_="price-tax").text

            split_price = games.split("€")

            return f"{split_price[1]}€"

        except AttributeError:
            return "Game not found"

    except Exception:
        return "Something went wrong."


#   The function looks up the price of a game in the MMOGA store
def mmoga_find_price(game):
    try:
        url = f"https://www.mmoga.com/advanced_search.php?keywords={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        try:
            games = soup.find("span", class_="smallBoldText").text

            split_price = games.split("$")

            return f"{split_price[1].replace(',', '.')}$".replace("\xa0", '')
        except AttributeError:
            return "Game not found"

    except Exception:
        return "Something went wrong."


#   The function looks up the price of a game in the YU PLAY store
def yu_play_find_price(game):
    try:
        url = f"https://www.yuplay.com/products/?search={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        try:
            games = soup.find("span", class_="catalog-item-sale-price").text

            return f"{games}"
        except AttributeError:
            return "Game not found"

    except Exception:
        return "Something went wrong."


#   The function looks up the price of a game in the Punktid store
def punktid_find_price(game, final_game_name):
    try:
        url = f"https://punktid.com/search?se={game}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        try:
            games_names = soup.find("div", class_="field field-name-title").text.split(" ")
            split_final_name = final_game_name.split(" ")

            if games_names[0] == split_final_name[0]:
                price = soup.find("span", class_="price-amount").text
                split_price = price.split("\xa0")
                return f"{split_price[0].replace(',', '.')}€"

            elif games_names[0] != split_final_name[0]:
                return "Game not found"

        except AttributeError:
            return "Game not found"

    except Exception:
        return "Something went wrong."
