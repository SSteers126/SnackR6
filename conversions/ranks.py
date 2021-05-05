
def rank_roman_to_int(rank_text):
    """Converts in-game rank names into a list, containing
    the rank 'league', and the position (i.e 1, 2, 3 etc) of
    the rank when applicable as a list of one when there is
    no position, and two then there is. ('league' is a string,
    position in the 'league' is an integer)"""
    rank_text = rank_text.lower()
    rank_split = rank_text.split(" ")
    listed_rank = []
    listed_rank.append(rank_split[0])
    if len(rank_split) == 2:  # TODO: check when new ranks arrive if the new algorithm will stay correct
        if (v_index := rank_split[1].find("v")) != -1:
            if v_index == 0:
                listed_rank.append(len(rank_split[1]) + 4)  # V has a value of 5, 1 in length + 4
            else:
                listed_rank.append(6 - len(rank_split[1]))  # 4 for IV, 3 for IIV (even if not possible)
        else:   # Examples such as 'IVI' would be calculated incorrectly, but are also invalid.
            listed_rank.append(len(rank_split[1]))
    return listed_rank