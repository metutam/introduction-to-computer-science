# World Cup
In soccer’s World Cup, the knockout round consists of 16 teams. In each round, each team plays another team and the losing teams are eliminated. When only two teams remain, the winner of the final match is the champion.

In soccer, teams are given FIFA Ratings, which are numerical values representing each team’s relative skill level. Higher FIFA ratings indicate better previous game results, and given two teams’ FIFA ratings, it’s possible to estimate the probability that either team wins a game based on their current ratings. The FIFA Ratings from two previous World Cups are available as the May 2018 Men’s FIFA Ratings and March 2019 Women’s FIFA Ratings.

Using this information, we can simulate the entire tournament by repeatedly simulating rounds until we’re left with just one team. And if we want to estimate how likely it is that any given team wins the tournament, we might simulate the tournament many times (e.g. 1000 simulations) and count how many times each team wins a simulated tournament.

Your task in this lab is to do just that using Python!

Start by taking a look at the 2018m.csv file. This file contains the 16 teams in the knockout round of the 2018 Men’s World Cup and the ratings for each team. Notice that the CSV file has two columns, one called team (representing the team’s country name) and one called rating (representing the team’s rating).

The order in which the teams are listed determines which teams will play each other in each round (in the first round, for example, Uruguay will play Portugal and France will play Argentina; in the next round, the winner of the Uruguay-Portugal match will play the winner of the France-Argentina match). So be sure not to edit the order in which teams appear in this file!

Ultimately, in Python, we can represent each team as a dictionary that contains two values: the team name and the rating. Uruguay, for example, we would want to represent in Python as {"team": "Uruguay", "rating": 976}.

Next, take a look at 2019w.csv, which contains data formatted the same way for the 2019 Women’s World Cup.

Now, open tournament.py and see that we’ve already written some code for you. The variable N at the top represents how many World Cup simulations to run: in this case, 1000.

The simulate_game function accepts two teams as inputs (recall that each team is a dictionary containing the team name and the team’s rating), and simulates a game between them. If the first team wins, the function returns True; otherwise, the function returns False.

The simulate_round function accepts a list of teams (in a variable called teams) as input, and simulates games between each pair of teams. The function then returns a list of all of the teams that won the round.

In the main function, notice that we first ensure that len(sys.argv) (the number of command-line arguments) is 2. We’ll use command-line arguments to tell Python which team CSV file to use to run the tournament simulation. We’ve then defined a list called teams (which will eventually be a list of teams) and a dictionary called counts (which will associate team names with the number of times that team won a simulated tournament). Right now they’re both empty, so populating them is left up to you!

Finally, at the end of main, we sort the teams in descending order of how many times they won simulations (according to counts) and print the estimated probability that each team wins the World Cup.

Populating teams and counts and writing the simulate_tournament function are left up to you!
