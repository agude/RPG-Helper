#!/usr/bin/python3
#  Copyright (C) 2012  Alexander Gude -
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


##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser  # Command line parsing

    """ Allows command line options to be parsed. Called first to in order to
    let functions use them.  """

    usage = "usage: %prog [Options]"
    version = "%prog Version 1.0.0\n\nCopyright (C) 2012 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-p", "--points", action="store", type="int", dest="pointsTotal", default=15, help="use this many points as the total budget [defualt 15]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    ## Code to brute force
    costs = {
            7: -4,
            8: -2,
            9: -1,
            10: 0,
            11: 1,
            12: 2,
            13: 3,
            14: 5,
            15: 7,
            16: 10,
            17: 13,
            18: 17,
            }

    found = {}

    for i in range(7, 19):
        for j in range(7, 19):
            for k in range(7, 19):
                for l in range(7, 19):
                    for m in range(7, 19):
                        for n in range(7, 19):
                            abilities = [i, j, k, l, m, n]
                            costCurrent = 0
                            for z in abilities:
                                costCurrent += costs[z]
                            if costCurrent == options.pointsTotal:
                                abilities.sort()
                                abilities.reverse()
                                found[tuple(abilities)] = costCurrent

    keys = list(found.keys())
    keys.sort()

    for statline in keys:
        print(statline)
