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

    def add(self, prefix, suffix):
        """ Add a prefix, and the suffix that follows it """
        if prefix in self.d.keys():
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]
            
    def keys(self):
        """ Return keys """
        return self.d.keys()

    def __repr__(self):
        """ Used for interactive display and printing """
        return self.d.__repr__()

class NameGenerator:
    """ Use a Markov Chain and a list of input names to generate random names """
    def __init__(self, inputFile, chainLength, maxLength, noDupes):
        self.inputFile = inputFile
        self.chainLength = chainLength
        self.maxLength = maxLength
        self.noDupes = noDupes
        self.mc = MarkovChain()
        self.__loadFile()
        self.__parseData()
        #print(self.mc)

    def __loadFile(self):
        """ Load names from input file into a set """
        f = open(self.inputFile)
        self.data = f.readlines()
        f.close()
        #Clean up lines
        for i in range(len(self.data)):
            self.data[i] = self.data[i].strip().lower()

    def __parseData(self):
        """ Run through self.data, parse it, and store the results into
        MarkovChain object """
        for word in self.data:
            while len(word) >= self.chainLength:
                prefix = word[0:self.chainLength]
                word = word[self.chainLength:]
                # Check to see if we're at the end of our word
                if len(word) == self.chainLength:
                    suffix = word[0:self.chainLength]
                    self.mc.add(prefix,suffix)
                    self.mc.add(suffix,'\n')
                    break
                elif len(word) < self.chainLength:
                    suffix = word[0:self.chainLength] + '\n'
                    self.mc.add(prefix,suffix)
                    break
                else:
                    suffix = word[0:self.chainLength]
                    self.mc.add(prefix,suffix)

    def makeNames(self,nnames):
        """ Generate n names """
        self.names = []
        # Loop until we have enough self.names
        i = 0
        while len(self.names) < nnames and i <= nnames * 100:
            i += 1 # Makes it so we don't run forever
            prefix = choice(tuple(self.mc.keys()))
            name = prefix
            # Walk through the chain for each name
            while True:
                try:
                    suffix = self.mc[prefix]
                except KeyError:
                    self.__checkName(name)
                    break
                else:
                    name += suffix
                    prefix = suffix
                # Name is long enough, or we hit break characters
                if len(name) >= self.maxLength or prefix == '' or prefix == '\n':
                    self.__checkName(name)
                    break

        for name in self.names:
            print(name.title())

    def __checkName(self,name):
        """ Check if we should add a name to the final list or not """
        name = name.lower().strip()
        if name.title() not in self.names:
            if self.noDupes and name not in self.data:
                self.names.append(name.title())
            elif not self.noDupes:
                self.names.append(name.title())


##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser # Command line parsing

    """ Allows command line options to be parsed. Called first to in order to
    let functions use them.  """

    usage = "usage: %prog [Options]"
    version = "%prog Version 1.0.0\n\nCopyright (C) 2012 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage,version=version)
    parser.add_option("-f", "--input-file", action="store", type="str", dest="inputFile", help="input file containing a list of names, one per line")
    parser.add_option("-c", "--chain-length", action="store", type="int", dest="chainLength", default=2, help="length of fragments [default 2]")
    parser.add_option("-m", "--max-length", action="store", type="int", dest="maxLength", default=9, help="maximum length of a name [default 9]")
    parser.add_option("-n", "--n-names", action="store", type="int", dest="nNames", default=5, help="create this many names [default 5]")
    parser.add_option("-i", "--not-in-input", action="store_true", dest="noDupes", default=False, help="prevent generating names found in the input file [default false]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    ng = NameGenerator(options.inputFile, options.chainLength, options.maxLength, options.noDupes)
    ng.makeNames(options.nNames)
