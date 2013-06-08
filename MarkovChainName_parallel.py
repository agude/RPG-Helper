#!/usr/bin/python3
#  Copyright (C) 2013  Alexander Gude -
#  alex.public.account+pathfinderhelper@gmail.com
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 3 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc., 59 Temple
#  Place - Suite 330, Boston, MA  02111-1307, USA.

from random import choice
import multiprocessing


class MarkovChain:
    """ Class to store weighted Markov Chain data """
    def __init__(self):
        self.d = {}
        self.s = []

    def __getitem__(self, prefix):
        """ Return a suffix for a given input prefix """
        return choice(self.d[prefix])

    def add(self, prefix, suffix):
        """ Add a prefix, and the suffix that follows it """
        if prefix in self.d.keys():
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]

    def addStart(self, prefix, suffix):
        """ Add a prefix, and the suffix, to both the normal list and starts
        list """
        self.s.append(prefix)
        self.add(prefix, suffix)

    def keys(self):
        """ Return keys """
        return self.d.keys()

    def __repr__(self):
        """ Used for interactive display and printing """
        return self.d.__repr__()


class NameGenerator:
    """ Use a Markov Chain and a list of input names to generate
    random names """
    def __init__(self, inputFile, chainLength, maxLength, minLength, noDupes, useStarts, nJobs):
        self.inputFile = inputFile
        self.chainLength = chainLength
        self.maxLength = maxLength
        self.minLength = minLength
        self.noDupes = noDupes
        self.useStarts = useStarts
        self.nJobs = nJobs
        self.mc = MarkovChain()
        self.__loadFile()
        self.__parseData()

    def __loadFile(self):
        """ Load names from input file into a set """
        f = open(self.inputFile)
        self.data = f.readlines()
        f.close()
        #Clean up lines
        for i in range(len(self.data)):
            self.data[i] = self.data[i].strip().lower()
        self.data = frozenset(self.data)

    def __parseData(self):
        """ Run through self.data, parse it, and store the results into
        MarkovChain object """
        for word in self.data:
            firstRun = True
            while len(word) >= self.chainLength:
                prefix = word[0:self.chainLength]
                word = word[self.chainLength:]
                # First run
                # Check to see if we're at the end of our word
                if len(word) == self.chainLength:
                    suffix = word[0:self.chainLength]
                    if firstRun:
                        self.mc.addStart(prefix, suffix)
                    else:
                        self.mc.add(prefix, suffix)
                    self.mc.add(suffix, '\n')
                    break
                # Check to see if we are at the end, and need to pad
                elif len(word) < self.chainLength:
                    suffix = word[0:self.chainLength] + '\n'
                    if firstRun:
                        self.mc.addStart(prefix, suffix)
                    else:
                        self.mc.add(prefix, suffix)
                    break
                # Otherwise keep running
                else:
                    suffix = word[0:self.chainLength]
                    if firstRun:
                        self.mc.addStart(prefix, suffix)
                    else:
                        self.mc.add(prefix, suffix)
                firstRun = False

    def makeNames(self, nNames):
        """ Make a list of names by spawning subprocesses to run through the
        Markov Chain """
        # Variables to share between threads
        self.nameQueue = multiprocessing.Queue()

        # Make processes
        jobs = []
        for i in range(self.nJobs):
            p = NameShover(self.mc, self.maxLength, self.minLength, self.useStarts, self.nameQueue)
            p.daemon = True
            jobs.append(p)
            p.start()

        # Keep track of how many tries we have made
        checkedNames = 0
        self.finalNames = set()
        runCheck = True
        while len(self.finalNames) < nNames and checkedNames < nNames * 100:
            name = self.nameQueue.get(block=True)
            self.__checkName(name)
            checkedNames += 1
            # Shut down the Shovers if we have more names than we could need.
            # We have a safety factor of nNames (hence 101) because qsize() is
            # somewhat inaccurate.
            if runCheck and self.nameQueue.qsize() + checkedNames >= nNames * 101:
                runCheck = False
                for p in jobs:
                    if p.is_alive():
                        p.shutdown()

        # Shutdown Shovers
        for p in jobs:
            if p.is_alive():
                p.shutdown()

        # print names
        for name in self.finalNames:
            print(name)

    def __checkName(self, name):
        """ Check if we should add a name to the final list or not """
        name = name.lower().strip()
        if self.noDupes and name not in self.data:
            self.finalNames.add(name.title())
        elif not self.noDupes:
            self.finalNames.add(name.title())


class NameShover(multiprocessing.Process):
    """ Takes a Markcov Chain and a queue, and shoves names onto the queue
    until told to stop. """
    def __init__(self, markovchain, maxLength, minLength, useStarts, resultQueue):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.mc = markovchain
        self.maxLength = maxLength
        self.minLength = minLength
        self.useStarts = useStarts
        self.resultQueue = resultQueue

    def shutdown(self):
        """ Stop the process """
        self.exit.set()

    def run(self):
        """ The function called by multiprocessing to do work """
        while not self.exit.is_set():
            # Generate first part of name, use only the start list in mc class
            # if useStart is set
            if self.useStarts:
                prefix = choice(tuple(self.mc.s))
            else:
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
        # Done, return exit code
        return 0

    def __checkName(self, name):
        """ Check if we should add a name to the queue or not """
        if self.minLength <= len(name.strip()) <= self.maxLength:
            name = name.lower().strip()
            self.resultQueue.put(name.title())

##### START OF CODE
if __name__ == '__main__':

    from optparse import OptionParser  # Command line parsing
    from math import floor

    NJOBS = int(floor(multiprocessing.cpu_count() * 1.5))  # Default job number

    # Allows command line options to be parsed. Called first to in order to let
    # functions use them.

    usage = "usage: %prog [Options]"
    version = "%prog Version 0.2\n\nCopyright (C) 2013 Alexander Gude - alex.public.account+pathfinderhelper@gmail.com\nThis is free software.  You may redistribute copies of it under the terms of\nthe GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Alexander Gude."
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-f", "--input-file", action="store", type="str", dest="inputFile", help="input file containing a list of names, one per line")
    parser.add_option("-c", "--chain-length", action="store", type="int", dest="chainLength", default=2, help="length of fragments [default 2]")
    parser.add_option("-m", "--max-length", action="store", type="int", dest="maxLength", default=30, help="maximum length of a name [default 30]")
    parser.add_option("-u", "--min-length", action="store", type="int", dest="minLength", default=2, help="minimum length of a name [default 2]")
    parser.add_option("-n", "--n-names", action="store", type="int", dest="nNames", default=5, help="create this many names [default 5]")
    parser.add_option("-j", "--jobs", action="store", type="int", dest="nJobs", default=NJOBS, help="use this many subprocess [default cpu_count]")
    parser.add_option("-i", "--not-in-input", action="store_true", dest="noDupes", default=False, help="prevent generating names found in the input file [default false]")
    parser.add_option("-s", "--use-starts", action="store_true", dest="useStarts", default=False, help="start names only with combinations that also start names in the input file [default false]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout [default false]")
    parser.add_option("-q", "--quite", action="store_false", dest="verbose", default=False, help="do not print status messages to stdout")

    (options, args) = parser.parse_args()

    ng = NameGenerator(options.inputFile, options.chainLength, options.maxLength, options.minLength, options.noDupes, options.useStarts, options.nJobs)
    ng.makeNames(options.nNames)
