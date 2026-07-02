def get_milk_face(player):
    hp_ratio = player.hp / max(1, player.max_hp)

    if hp_ratio <= 0:
        return "×"

    if hp_ratio <= 0.2:
        return "><"

    if hp_ratio <= 0.4:
        return ";_;"

    if hp_ratio <= 0.7:
        return "o_o"

    return "^_^"