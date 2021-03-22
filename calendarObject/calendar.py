"""
Classes to model Day and Pill attributes
"""

class Day():
    """
    Construct of Day Class
    :param day: day selected
    """
    def __init__(self,day):
        self.day = day
        self.pills = []

    # Add a pill to the day selected
    def add_pill(self,pillName,date,pillSelection,pillTaken,src):
        self.pills.append(Pill(pillName,date,pillSelection,pillTaken,src))
    
    # Remove pill from day selected
    def remove_pill (self,pillname):
        for pill in pills:
            if (pill.pillName == pillname):
                self.pills.remove(pill)

class Pill():
    """
    Construct of Pill Class
    :param pillName: kind of pill (metadol or metaspirin)
    :param data: date when the pill have to be taken
    :param pillSelection: pill has been selected
    :param pillTaken: pill has been taken
    :param src: pill image (red/blue)
    """
    def __init__(self,pillName,date,pillSelection,pillTaken,src):
        self.pillName = pillName
        self.date = date
        self.pillSelection = pillSelection
        self.pillTaken = pillTaken
        self.src = src

    # Set new date for the pill
    def set_date(self,date):
        self.date= date