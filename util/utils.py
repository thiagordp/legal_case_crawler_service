"""

"""
from util.path_constants import TRIBUNALS_PATH


def get_date_formatted(d1, separator="-", reverse=True):
    day = d1.day
    month = d1.month
    year = d1.year

    if reverse:
        return str(year).zfill(4) + separator + str(month).zfill(2) + separator + str(day).zfill(2)

    return str(day).zfill(2) + separator + str(month).zfill(2) + separator + str(year).zfill(4)


def check_court(court_name):
    court_name = court_name.lower()

    for court in TRIBUNALS_PATH:

        if court.lower().find(court_name) != -1:
            return True

    return False
