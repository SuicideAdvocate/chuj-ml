import random
cards = ["7h", "8h", "9h", "10h", "Uh", "Oh", "Kh", "Ah",
         "7a", "8a", "9a", "10a", "Ua", "Oa", "Ka", "Aa",
         "7b", "8b", "9b", "10b", "Ub", "Ob", "Kb", "Ab",
         "7l", "8l", "9l", "10l", "Ul", "Ol", "Kl", "Al",]

random.shuffle(cards)
play = cards[0:3]
print(play)