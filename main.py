from config import collection

from page_class.betwarrior import BetWarrior

place = BetWarrior()

games = place.get_basketaball_games_info(spe="Spain")

collection.insert_many(games)
