"""Implementation of the Hogwarts house-selection spell."""


def hogwarts(line, env):
    """Switch runtime house mode if a valid house is provided."""
    house = line.replace("Hogwarts", "", 1).strip()
    houses = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]

    if house not in houses:
        print("⚠ Unknown house. Defaulting to Hogwarts.")
        env.set_house("Hogwarts")
        return

    env.set_house(house)
    print(f"🏰 Welcome to {house} House!")
