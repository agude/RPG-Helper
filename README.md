RPG Helper
=========

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
in Pathfinder such that the combined total is a specificed challenge rating.

This script is **still under developement** and as such does not work yet.

## DateHandler.py

This script handles dates in my custom campaign setting. It allows the
conversion of dates and the generation of random dates.

### Usage

If the program is called as follows:

    ./DateHandler.py -h

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

    ./DateHandler.py --random

Which produces results like:

    Random Date: It is Summer 46, which is the 136 day of the year, and the 1st day of the week.

The script can also be used to convert date formats using the season and day as
input:

    ./DateHandler.py -d "Summer 85"

Which returns:

    It is Summer 85, which is the 175 day of the year, and also the Day of Rest.

Finally, the script can be used to convert date formats using the day of the year as input:

    ./DateHandler.py -d "354"

Which returns:

    It is Winter 84, which is the 354 day of the year, and the 4th day of the week.


