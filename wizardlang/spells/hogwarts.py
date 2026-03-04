def hogwarts(line, env):

    house = line.replace("Hogwarts", "", 1).strip()

    houses = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]

    if house not in houses:
        print("⚠ Unknown house. Defaulting to Hogwarts.")
        env.set_house("Hogwarts")
        return

    env.set_house(house)

    print(f"🏰 Welcome to {house} House!")