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

You can change the number of points used in the point buy with the `-p` option:

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

Finally, the script can be used to convert date formats using the day of the year as input:

    DateHandler.py -d "354"

Which returns:

    It is Winter 84, which is the 354 day of the year, and the 4th day of the week.

## MarkovChainName.py

This script parses an list of input words, and generates a new set of words
using a [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo).
It is useful for generating a list names that look and sound similar to a set
of input names.

### Algorithm

Input words are broken down into *chunks* of characters, which are then used to
form a Markov chain. For example, the input word `Alexander` would be mapped to
a chain of the following form (using the default chunk size of 2):

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
from chunks that also start words in the input list. This behavior is toggled
with the `-s` flag.

Frequency information is automatically stored by the use of a dictionary. If the input values were 
`Alexander`, `Andrew`, and `Andrew` (yes, using the same name twice), we would
generate the following chain:

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

