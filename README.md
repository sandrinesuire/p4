# Develop a software program in Python

## Objective of the project

Develop a tournament software that would allow managing offline events, and generating reports.

## Specifications

### Development
Swiss chess tournament system
MVC archi : 
    Models
        * tournament,
        * players,
        * round,
        * matches.
    Controllers
        * accept user data,
        * produce the results of the matches,
        * start new tournaments, etc.
    Views
        * rankings,
        * pairings,
        * other statistics.
Code will be clean and maintainable (PEP8 ...)

### Application

The application should be
    * Independent Application
    * Offline Application
    * Python console Application
    * Platform Windows, Mac, Linux
    * Virtual environment


#### Progress of the game

    1. Create a new tournament.
    2. Add eight players.
    3. Generation of pairs of players for
        the first round.
            * Sort all players according to their ranking
            * Divide players into two halves, one upper and one lower
            * The best player in the upper half is paired with the best player in the lower half
        the following rounds.
            * Sort all players according to their total number of points
            * If several players have the same number of points, sort them according to their rank
            * Match player 1 with player 2, player 3 with player 4 ...
            * If player 1 has played against player 2 before, pair them with player 3 instead.
    4. A draw of the players will determine who plays white and who plays black.
    5. When the round is finished, enter the results.
    6. Repeat steps 3 and 4 for subsequent rounds until all rounds are played, and the tournament is over.

#### Tournament

    • Last name
    • Location
    • Date (several days)
    • Number of turns (default: 4)
    • Tours: list of round bodies
    • Players: list of player indices
    • Time control: bullet, blitz or quick hit
    • Description: general remarks from the tournament director

#### Player

    • Section dedicated to adding players
    • Database :
        • Last name
        • First name
        • Date of Birth
        • Gender
        • Ranking (positive number)

    • No old data
    • Manual entry of players upon arrival
    • No removal of players

#### Round
    * list (match)
    * name (ex "Round 1")
    * Start date / time
    * End date / time

    At the end of a round:
        * Tournament manager enters the results of each match
        * Tournament manager generates the following pairs
        * if match null:
            * each player receives 1/2 point.
        * if not
            * The winner receives 1 point
            * The loser 0 point

#### Match
match = ([player.id, score], [player.id, score])

#### Pairs
Swiss system.
At the end of the tournament and at any time:
    * Tournament manager manually updates player ranking

#### Report
We would like to be able to display the following reports in the program:

    • List of all actors:
        ◦ in alphabetical order;
        ◦ by classification.
    • List of all players in a tournament:
        ◦ in alphabetical order;
        ◦ by classification.
    • List of all tournaments.
    • List of all rounds in a tournament.
    • List of all matches in a tournament.

#### Save / Load data
Save and load program at any time between two user actions.
BD or easier to see

## Deliverables

A link to a GitHub repository which includes:
    * the application code, as prescribed in the technical specification;
    * a directory containing an HTML file generated by flake8-html, showing no fluffing errors in the code;
    * a README.md file with clear instructions on how to 
        - run the program, 
        - use it, 
        - generate rapport "flake8_rapport" (max-length=119).

## Install

Virtual environment Linux/macOS
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

Virtual environment Windows
```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```

Install the libraries
```
pip install -r requirements.txt
```

## Run application
 
```
python3 main.py
```

## Flake8 html file generation
 
```

```

## Platforms

This application was testing on
* Ubuntu 20.10 + python 3.8