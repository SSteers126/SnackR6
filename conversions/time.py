from math import floor


def ordinal_to_hours(ordinal):
    hours = floor(ordinal/3600)
    minsandseconds = ordinal-(hours*3600)
    mins = minsandseconds // 60
    seconds = floor(minsandseconds - (60 * mins))
    # print(mintime)
    # minutes = floor(ordinal-(hours*3600)/60)
    # # minutes = floor((ordinal-(hours*3600))/60)
    # seconds = floor((ordinal-(minutes*60))/60)
    return [hours, mins, seconds]

