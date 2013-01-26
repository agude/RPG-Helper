#!/usr/bin/python3
#  Copyright (C) 2013  Alexander Gude - alex.public.account+pathfinderhelper@gmail.com
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

class conversionTable:
    """ Class to convert from CR to EXP and back """
    def __init__(self):
        self.EXP = ( 
                50, 65, 100, 135, 200, 400, 600, 800, 1200, 1600,
                2400, 3200, 4800, 6400, 9600, 12800, 19200, 25600, 38400, 51200,
                76800, 102400, 153600, 204800, 307200, 409600, 614400, 819200, 1228800, 1638400
                )
        self.CR = (
                "1/8", "1/6", "1/4", "1/3", "1/2", "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"
                )
        self.CRtoEXP = {
                "1/8": 50, "1/6": 65, "1/4": 100,
                "1/3": 135, "1/2": 200, "1": 400,
                "2": 600, "3": 800, "4": 1200,
                "5": 1600, "6": 2400, "7": 3200,
                "8": 4800, "9": 6400, "10": 9600,
                "11": 12800, "12": 19200, "13": 25600,
                "14": 38400, "15": 51200, "16": 76800,
                "17": 102400, "18": 153600, "19": 204800,
                "20": 307200, "21": 409600, "22": 614400,
                "23": 819200, "24": 1228800, "25": 1638400
                }
        self.EXPtoCR = {
                50: "1/8",
                65: "1/6",
                100: "1/4",
                135: "1/3",
                200: "1/2",
                400: "1",
                600: "2",
                800: "3",
                1200: "4",
                1600: "5",
                2400: "6",
                3200: "7",
                4800: "8",
                6400: "9",
                9600: "10",
                12800: "11",
                19200: "12",
                25600: "13",
                38400: "14",
                51200: "15",
                76800: "16",
                102400: "17",
                153600: "18",
                204800: "19",
                307200: "20",
                409600: "21",
                614400: "22",
                819200: "23",
                1228800: "24",
                1638400: "25"
                }

    def isCR(self,CR):
        """ Check if the CR value is legal """
        if CR in self.CR:
            return True
        else:
            return False

    def isEXP(self,EXP):
        """ Check if the EXP value is legal """
        if EXP in self.EXP:
            return True
        else:
            return False

    def __getitem__(self,item):
        """ Allow conversion via array access """
        if self.isCR(item):
            return self.CRtoEXP[item]
        elif self.isEXP(item):
            return self.EXPtoCR[item]
        else:
            raise KeyError

##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser # Command line parsing

    """ Allows command line options to be parsed. Called first to in order to
    let functions use them.  """

    usage = "usage: %prog [Options]"
    version = "%prog Version 1.0.0\n\nCopyright (C) 2013 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage,version=version)
    parser.add_option("-c", "--cr", action="store", type="int", dest="crTotal", default=1, help="target this CR rating for an encounter [defualt 1]")
    parser.add_option("-x", "--max", action="store", type="int", dest="crMax", default=25, help="do not use CR ratings larger than CRMAX to fill in the encounter [defualt 25]")
    parser.add_option("-n", "--min", action="store", type="int", dest="crMin", default=0, help="do not use CR ratings smaller than CRMIN to fill in the encounter [defualt 0]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    ## Code to brute force
    ct = conversionTable()
