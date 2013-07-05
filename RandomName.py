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

from random import choice, random


class NameList:
    """ A class to store a list of names """
    def __init__(self, inFile, hyphenP=0.):
        """ Construct list from a file, and set hyphenated probability """
        self.inFile = inFile
        self.hyphenP = hyphenP
        self.__loadList()

    def __loadList(self):
        """ Load the list of names """
        f = open(self.inFile, 'r')
        cont = f.read()
        f.close()
        cont = cont.splitlines()
        self.data = []
        for item in cont:
            self.data.append(item.strip())

    def returnName(self):
        """ Return a random name """
        if self.hyphenP != 0. and random() < self.hyphenP:
            return "{first}-{second}".format(first=choice(self.data),
                    second=choice(self.data))
        else:
            return choice(self.data)

##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser  # Command line parsing

    """ Allows command line options to be parsed. Called first to in order to
    let functions use them.  """

    usage = "usage: %prog [Options]"
    version = "%prog Version 1.0.0\n\nCopyright (C) 2013 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-f", "--first-name-list", action="store", type="str", dest="fnList", default=None, help="input file containing a list of first names")
    parser.add_option("-l", "--last-name-list", action="store", type="str", dest="lnList", default=None, help="input file containing a list of last names")
    parser.add_option("-p", "--hyphen-probability", action="store", type="float", dest="hyphenP", default=".05", help="number in [0.,1.] giving the probability of hyphenating a last name [default 0.05]")
    parser.add_option("-n", "--n-names", action="store", type="int", dest="nNames", default="5", help="print this number of names [default 5]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    names = []
    # First and last name
    if options.fnList != None and options.lnList != None:
        fn = NameList(options.fnList, 0.)
        ln = NameList(options.lnList, options.hyphenP)
        while len(names) < options.nNames:
            name = "{first} {last}".format(first=fn.returnName(), last=ln.returnName())
            name = name.title()
            if name not in names:
                names.append(name)
        for name in names:
            print(name)
    # One name only
    elif options.lnList == None and options.fnList != None:
        fn = NameList(options.fnList, options.hyphenP)
        while len(names) < options.nNames:
            name = fn.returnName()
            name = name.title()
            if name not in names:
                names.append(name)
        for name in names:
            print(name)
    # Missing Input
    else:
        print("Must specify at least first-name-list.")
