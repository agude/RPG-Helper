# RPG Helper


RPG Helper is a collection of python scripts designed to aid a game master in
running a pen and paper role playing game.

## AbilityScoreCombinations.py

This script generates a list of all possible ability score combinations for a
set point value in a Pathfinder point buy.

### Usage

If the program is called as follows:

    AbilityScoreCombinations.py -h

It will provide the following usage guide:

    Usage: AbilityScoreCombinations.py [Options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -p POINTSTOTAL, --points=POINTSTOTAL
                            use this many points as the total budget [defualt 15]
      -v, --verbose         print status messages to stdout [default false]
      -q, --quite           do not print status messages to stdout


The simplest usage case is:

    AbilityScoreCombinations.py

This will print the possible combination of ability scores for a 15 point buy.

One can change the number of points used in the point buy with the `-p` option:

    AbilityScoreCombinations.py -p 20

This will print the possible combination of ability scores for a 20 point buy.

## CRCombinations.py

This script generates a list of all possible combinations of challenge rating
in Pathfinder such that the combined total is a specified challenge rating.

This script is **still under developement** and as such does not work yet.

## DateHandler.py

This script handles dates in my custom campaign setting. It allows the
conversion of dates and the generation of random dates.

### Usage

If the program is called as follows:

    DateHandler.py -h

It will provide the following usage guide:

    Usage: DateHandler.py [Options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -d DATE, --date=DATE  input date in the form '0 <= date <= 360' or 'Season
                            Day'
      -r, --random          generate a random date and ignore any --date input
                            [default False]
      -v, --verbose         print status messages to stdout [default false]
      -q, --quite           do not print status messages to stdout

To generate random dates it can be used as follows:

    DateHandler.py --random

Which produces results like:

    Random Date: It is Summer 46, which is the 136 day of the year, and the 1st day of the week.

The script can also be used to convert date formats using the season and day as
input:

    DateHandler.py -d "Summer 85"

Which returns:

    It is Summer 85, which is the 175 day of the year, and also the Day of Rest.

Finally, the script can be used to convert date formats using the day of the
year as input:

    DateHandler.py -d "354"

Which returns:

    It is Winter 84, which is the 354 day of the year, and the 4th day of the week.

## MarkovChainName.py

This script parses an list of input words, and generates a new set of words
using a [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo).
It is useful for generating a list names that look and sound similar to a set
of input names.

### Algorithm

Input words are broken down into *fragments* of characters, which are then used
to form a Markov chain. For example, the input word `Alexander` would be mapped
to a chain of the following form (using the default fragment size of 2):

    "al" -> "ex" -> "an" -> "de" -> "r\n"

Which each link in the chain having a probability of 1 of moving to the next
link.

If we used to the names `Alexander` and `Andrew` we would form the following
structure:

    "al" -> "ex" -> "an" 0.5|-> "de" -> "r\n"
                         0.5|-> "dr" -> "ew" -> "\n"

The chain now has a branch point at "an" giving a probability of 0.5 of moving
to each of "de" or "dr". 


The results of parsing the input list are stored as a dictionary and a list.
The dictionary stores the chain, which for the above case looks like:

    {'de': ['r\n'], 'al': ['ex'], 'an': ['dr', 'de'], 'ex': ['an'], 'ew': ['\n'], 'dr': ['ew']}

The list stores a set of starting values, which for the above case would look like:

    ['an', 'al']

The starting values list allows the code to—if the user so desires—only start
from fragments that also start words in the input list. This behavior is
toggled with the `-s` flag.

Frequency information is automatically stored by the use of a dictionary. If
the input values were `Alexander`, `Andrew`, and `Andrew` (yes, using the same
name twice), we would generate the following chain:

    "al" -> "ex" -> "an" 1/3|-> "de" -> "r\n"
                         2/3|-> "dr" -> "ew" -> "\n"

Which has the following dictionary representation:

    {'de': ['r\n'], 'al': ['ex'], 'an': ['de', 'dr', 'dr'], 'ex': ['an'], 'ew': ['\n', '\n'], 'dr': ['ew', 'ew']}

And the following start list:

    ['al', 'an', 'an']

### Usage

If the program is called as follows:

    MarkovChainName.py -h

It will provide the following usage guide:

    Usage: MarkovChainName.py [Options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -f INPUTFILE, --input-file=INPUTFILE
                            input file containing a list of names, one per line
      -c CHAINLENGTH, --chain-length=CHAINLENGTH
                            length of fragments [default 2]
      -m MAXLENGTH, --max-length=MAXLENGTH
                            maximum length of a name [default 30]
      -u MINLENGTH, --min-length=MINLENGTH
                            minimum length of a name [default 2]
      -n NNAMES, --n-names=NNAMES
                            create this many names [default 5]
      -i, --not-in-input    prevent generating names found in the input file
                            [default false]
      -s, --use-starts      start names only with combinations that also start
                            names in the input file [default false]
      -v, --verbose         print status messages to stdout [default false]
      -q, --quite           do not print status messages to stdout

The simplest usage case is:

    MarkovChainName.py -f $FILE

Which will output a 5 randomly generated names. One can increase the number of
generated names using `-n`. To generate 25 random names, one would run:

    MarkovChainName.py -f $FILE -n 25

The default configuration breaks the names in the input list into fragments of
2 characters. This can be changed with `-c`. Larger numbers will generate names
that more closely match the input names, but at the cost of the total number of
unique names possible. To break the input names into fragments of 3 characters,
one would run:

    MarkovChainName.py -f $FILE -c 3

One can change the length of the output names using `-u` and `-m`. By default
names at least 2 characters long and no more than 30 are generated. To generate
names between 6 and 12 characters one would run:

    MarkovChainName.py -f $FILE -u 6 -m 12

The default configuration allows names in that are in the input list to be
generated as output. One can prevent names already in the input list from being
generated by using `-i`.

The default configuration allows any set of letters to be used to start a name.
Using `-s` forces the script to only start names with letter combinations that
also start names in the input list. This is useful to avoid odd consonant
combinations that rarely start names, but often appear in the middle of names.

One can, of course, combine all these options at once. For example:

    MarkovChainName.py -f $FILE -u 3 -m 13 -i -s -n 100 -c 3

This would generate 100 names that are not in the input list while using only
letter combinations that are used to start names in the input list. These names
would be constrained to contain no fewer than 3, but no more than 13
characters. Finally, the script would form chains with fragments of 3
characters, instead of the default 2.

## MarkovChainName_parallel.py

A multiprocess version of MarkovChainName.py. It uses the same algorithm, and
has the same flags as MarkovChainName.py.

### Performance

This script currently under performs MarkovChainName.py in all cases. It was
mainly written to gain experience with python mutilprocessing.

### Usage

If the program is called as follows:

    MarkovChainName.py -h

It will provide the following usage guide:

    Usage: MarkovChainName_parallel.py [Options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -f INPUTFILE, --input-file=INPUTFILE
                            input file containing a list of names, one per line
      -c CHAINLENGTH, --chain-length=CHAINLENGTH
                            length of fragments [default 2]
      -m MAXLENGTH, --max-length=MAXLENGTH
                            maximum length of a name [default 30]
      -u MINLENGTH, --min-length=MINLENGTH
                            minimum length of a name [default 2]
      -n NNAMES, --n-names=NNAMES
                            create this many names [default 5]
      -j NJOBS, --jobs=NJOBS
                            use this many subprocess [default cpu_count]
      -i, --not-in-input    prevent generating names found in the input file
                            [default false]
      -s, --use-starts      start names only with combinations that also start
                            names in the input file [default false]
      -v, --verbose         print status messages to stdout [default false]
      -q, --quite           do not print status messages to stdout

All the flags operate identically to those used in MarkovChainName.py. The one
new flag is `-j`, which sets the number of new processes to use. The default is
the number of cores times 1.5 (floored). 

## RandomName.py

This script generates a list of names by randomly selecting from a list of
input names. Unlike MarkovChainName.py, this does not change the names.

### Usage

If the program is called as follows:

    RandomName.py -h

It will provide the following usage guide:

    Usage: RandomName.py [Options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -f FNLIST, --first-name-list=FNLIST
                            input file containing a list of first names
      -l LNLIST, --last-name-list=LNLIST
                            input file containing a list of last names
      -p HYPHENP, --hyphen-probability=HYPHENP
                            number in [0.,1.] giving the probability of
                            hyphenating a last name [default 0.05]
      -n NNAMES, --n-names=NNAMES
                            print this number of names [default 5]
      -v, --verbose         print status messages to stdout [default false]
      -q, --quite           do not print status messages to stdout

The simplest usage case is:

    MarkovChainName.py -f $FILE

This produces a list of 5 names randomly selected from the input file, with a
5% chance of creating a hyphenated name that is a combination of two of the
names on the input list.  One can randomly generate full names (first and last)
with the following command:

    MarkovChainName.py -f $FILE1 -l $FILE2

This produces a list of 5 full names, with a 5% chance of a last name being a
hyphenated combination of two of the names in `$FILE2`.

One can change the probability of having a hyphenated name by using `-p`.  To
change from a 5% chance to 10%, one would call the script as follows:

    MarkovChainName.py -f $FILE1 -p .1

One can generate more random names by using `-n`. To generate 10 names instead
of 5, one would use:

    MarkovChainName.py -f $FILE1 -n 10
