from wizardlang.houses.gryffindor import error as gryffindor_error
from wizardlang.houses.ravenclaw import error as ravenclaw_error
from wizardlang.houses.hufflepuff import error as hufflepuff_error
from wizardlang.houses.slytherin import error as slytherin_error


def handle_error(env, message):

    house = env.house

    if house == "Gryffindor":
        gryffindor_error(message)

    elif house == "Ravenclaw":
        ravenclaw_error(message)

    elif house == "Hufflepuff":
        hufflepuff_error(message)

    elif house == "Slytherin":
        slytherin_error(message)

    else:
        print("⚠ Wizard Error:", message)