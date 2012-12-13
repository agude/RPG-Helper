#!/usr/bin/python3
#  Copyright (C) 2012  Alexander Gude - alex.public.account+pathfinderhelper@gmail.com
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

from random import choice

class MarkovChain:
    """ Class to store weighted Markov Chain data """
    def __init__(self):
        self.d = {}
    def __getitem__(self, prefix):
        """ Return a suffix for a given input prefix """
        return choice(self.d[prefix])
    def add_key(self, prefix, suffix):
        """ Add a prefix, and the suffix that follows it """
        if prefix in self.d.keys():
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]

class NameGenerator:
    """ Use a Markov Chain and a list of input names to generate random names """
    def __init__(self, inputFile, chainLength, maxLength):
        self.inputFile = inputFile
        self.chainLength = chainLength
        self.maxLength = maxLength

##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser # Command line parsing

    """ Allows command line options to be parsed. Called first to in order to
    let functions use them.  """

    usage = "usage: %prog [Options]"
    version = "%prog Version 1.0.0\n\nCopyright (C) 2012 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage,version=version)
    parser.add_option("-c", "--chain-length", action="store", type="int", dest="chainLength", default=2, help="length of fragments [default 2]")
    parser.add_option("-m", "--max-length", action="store", type="int", dest="maxLength", default=9, help="maximum length of a name [default 9]")
    parser.add_option("-f", "--input-file", action="store", type="str", dest="inputFile", default=9, help="maximum length of a name [default 9]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    ng = NameGenerator(options.inputFile, options.chainLength, options.maxLength)
