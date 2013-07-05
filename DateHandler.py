#!/usr/bin/python3
#  Copyright (C) 2013  Alexander Gude -
#  alex.public.account+pathfinderhelper@gmail.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  The most recent version of this program is avaible at:
#  https://github.com/agude/RPG-Helper

from math import floor


class Date:
    """ Given a date, calculates all relevant information. """
    def __init__(self, inDate):
        """ Take a date and parse it. Dates are over the form 0 <= x <= 360, or
        "Season Day" """
        self.date = None
        self.season = None
        self.sday = None
        try:
            self.date = int(inDate)
        except ValueError:
            tmpseason = inDate.split(' ')[0]
            if tmpseason.lower() in ['spring', 'summer', 'fall', 'winter']:
                self.season = tmpseason.capitalize()
                self.sday = int(inDate.split(' ')[1])

        if self.date:
            self.__parseDate()
        elif self.season and self.sday:
            self.__parseSDay()

        self.__extractDOW()

    def __parseSDay(self):
        """ Parse self.sday and self.season and extract all information """
        # Extract date
        seasondic = {
                "Summer": 90,
                "Spring": 0,
                "Fall": 180,
                "Winter": 270
                }
        mod = seasondic[self.season]
        self.date = self.sday + mod

    def __parseDate(self):
        """ Parse self.date and extract all information """
        # Extract Season and sday
        if self.date <= 90:
            self.season = "Spring"
            self.sday = self.date
        elif self.date <= 180:
            self.season = "Summer"
            self.sday = self.date - 90
        elif self.date <= 270:
            self.season = "Fall"
            self.sday = self.date - 180
        elif self.date > 270:
            self.season = "Winter"
            self.sday = self.date - 270

    def __extractDOW(self):
        """ Calculate the day of the week """
        if self.date % 5 == 1:
            self.dow = "1st"
        elif self.date % 5 == 2:
            self.dow = "2nd"
        elif self.date % 5 == 3:
            self.dow = "3rd"
        elif self.date % 5 == 4:
            self.dow = "4th"
        else:
            self.dow = "Day of Rest"

    def __repr__(self):
        """ Used for interactive display and printing """
        if self.dow != "Day of Rest":
            return "It is {0} {1}, which is the {2} day of the year, and the {3} day of the week.".format(
                    self.season,
                    self.sday,
                    self.date,
                    self.dow
                    )
        else:
            return "It is {0} {1}, which is the {2} day of the year, and also the {3}.".format(
                    self.season,
                    self.sday,
                    self.date,
                    self.dow
                    )

##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser  # Command line parsing

    """ Allows command line options to be parsed. Called first to in order to
    let functions use them.  """

    usage = "usage: %prog [Options]"
    version = "%prog Version 1.0.0\n\nCopyright (C) 2013 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-d", "--date", action="store", type="str", dest="date", default=None, help="input date in the form '0 <= date <= 360' or 'Season Day'")
    parser.add_option("-r", "--random", action="store_true", dest="doRandom", default=False, help="generate a random date and ignore any --date input [default False]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    if options.doRandom:
        from random import randrange
        d = Date(randrange(1, 361, 1))
        print("Random Date:", d)
    else:
        d = Date(options.date)
        print(d)
