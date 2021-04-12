#Helper Functions which help in formatting and sorting data
from datetime import date


def getISODate(dateData:date):
    """
    INFO:
        Returns the ISO Format of a given date Object
    PARAM:
        A date Object
    """
    return dateData.isoformat()


def getMonth(dateData:date):
    """
    INFO:
        Returns the Month of a given date Object
    PARAM:
        A date Object
    """
    Months={
        1:"JANUARY",
        2:"FEBRUARY",
        3:"MARCH",
        4:"APRIL",
        5:"MAY",
        6:"JUNE",
        7:"JULY",
        8:"AUGUST",
        9:"SEPTEMBER",
        10:"OCTOBER",
        11:"NOVEMBER",
        12:"DECEMBER"
    }

    return Months[dateData.month]

def getYear(dateData:date):
    """
    INFO:
        Returns the Year of a given date Object
    PARAM:
        A date Object
    """
    return str(dateData.year)