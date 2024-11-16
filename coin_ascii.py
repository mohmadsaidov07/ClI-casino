def coin_ascii(coin_side) -> str:
    if coin_side == "heads":
        return r"""
                  _________
                 /           \
                |   _______   |
                |  /       \  |
                | |  HEADS  | |
                |  \_______/  |
                |             |
                 \___________/
    """
    elif coin_side == "tails":
        return r"""
                  _________
                 /           \
                |   _______   |
                |  /       \  |
                | |  TAILS  | |
                |  \_______/  |
                |             |
                 \___________/
    """
    else:
        return "There is no such side on a coin"


if __name__ == "__main__":
    print(coin_ascii("heads"))
