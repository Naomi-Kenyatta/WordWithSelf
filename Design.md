Design 

Flask 
We choose to implement the game in flask so that we could render the board 

We use sql to keep track of each user’s stats so that it can be displayed.  

Class organization:
In scrabble there are 3 physical components to the game: tiles, bag, board. 
Scrabble is played with tiles that have a letter that represents a certain point value. The tile has 2 attributes, it’s letter and its point value. A tile is created given the letter and the dictionary that determines the point value of every character. Another important part of the game is that every game there is a bag that holds all the available tiles. We created classes for all these objects so that we could create instances similarly to the way the game is in real life. 

There is a board that holds all the words that the player has played to translate this into code. The board class has one attribute that is a 2-dimensional array that holds the tile placements and an array that holds all the played words which is useful for the computer when deciding what it’s possible moves are. The board has a method that adds all the special tiles onto the board. It also has 2 methods for placing words. One for before the user confirms if that's the move they want and one that will actually change the board attribute and remove the tiles from the player’s hand. The place word functions are given the player and their input. 

The first thing a place word does is determine if the play is valid. First it deciphers the player’s input through a function called parse. This function checks if the player entered anything wrong and returns [0] if the input was wrong. Then it turns the input into a 2 dimensional array. Where the every row holds an individual move, the first entry on the row is the letter and the second one is a tuple with the location of where the letter should be placed on the board. The parse function also checks if all the letters are available in the player’s hand and when done it returns the 2-dimensional array. 

Next we have a function called word that checks if the player’s input makes a word that is connected to the rest of the screen. The first thing that needs to be determined is the direction of the word. This function returns the direction as a tuple. Then the function searches for the word by going to the left of the word to see if the player’s word 
Then it goes the normal way and adds all the player’s plays and the letters that aren't already on the board. 
It also checks if the player played any letters that are next to something that currently isn't part of the word as this is an illegal move in our scrabble.  
While iterating through the board it checks if any of the new letter’s being placed are on a special tile and it correctly adjusts the point value to take into account the special tiles. Once the word has been determined, we check if it is in the dictionary throughout the function indic. 

Our direction function does not handle one letter words correctly so we created a new function that separately handles one letter plays. 

We utilized the fact that in python a 0 equals false, a true equals 1 and all positive numbers represent true. So instead of returning true and false word returns an integer value. It returns 0 if all the conditions aren’t meant but it returns the point value of the word if it is a legal play. 

Now because it is an online game we have to create a way to hold all the player’s information in one spot so we created a player class that keeps track of their current hand and total score.



Helper functions to assist with game logic (error checking and parsing input)

Computer algorithm
In making the computer player, we had to find a way to have the program generate legal moves in a timely manner. To accomplish this, we first simplified the problem for the computer. First, the dictionary that the computer has access to is considerably smaller than the Scrabble Dictionary (about 10k words vs 280k words). This reduces the number of possibilities the computer has to search through. Next, the computer dictionary was loaded into a SQL table via the program “dicadd.py”. The table “dictionary” has two columns: one for the word and the other for the score of the word according to the dictionary “Points.” SQL allows us to efficiently select words, in descending order by point value, from the dictionary that have the potential to be a legal play given the current information on the board. Specifically, when making a play, the computer searches through the tiles on the current board and only considers possibilities where the tile is at the beginning of the word or the end of the word. For each tile on the board, the computer will execute a SQL command, loop through the list of possibilities the command returns, choose the first possibility that is legal, and add it to a list of possible plays. Note that the SQL command sorts the possible words by descending point value, so the computer can stop searching after finding the first legal play in the returned list. Finally, the computer selects the highest scoring play out of the list of possible plays. Because the word scores are pre-loaded into the SQL tables based only on the “Points” dictionary, the computer does not consider the special tiles on the board when choosing a play. The information returned in the “move” method of the computer is given to the board for execution.

A critical function for the computer is the function “legal.” Given a current hand, board, word, starting location for the word, and the direction of the word, this function determines if the potential play is legal. This is very helpful for the move method of the computer as when looping through the words returned by the SQL command, the computer can easily determine the information of the above arguments and call the legal function to see if it is a valid play or not.
