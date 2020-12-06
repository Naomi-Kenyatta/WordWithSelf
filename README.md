# WordWithSelf
cs50 final project - Eric and Naomi


We created a flask web app game. To play cs50 first you must unzip the folder. Then in the terminal navigate to inside the app folder. Then you are going to need to run “export API_KEY=pk_baf5acf8b82149dc9fb5e3aece72ca78” in the terminal. This will allow the register/login process to work.

Once that runs input “flask run” into the terminal and a web browser should pop up. First You will need to register and create an account and password. 

Then by navigating to the log in you will be able to log in as the user you just created. It will showcase the home page that will display your current stats aka total games, wins, losses and ties. On the top left corner you can click the rules of the game, but we will explain them here so they are there as a refresher. 

Now if you want to play a game of words with self you can click the start game button on the navigation bar. This will redirect you to a new page, click play there to confirm that you want to start the game. Now you will see a scrabble board that has 15 rows and columns. They are indexed from 0 to 14. Blew the board your hand will be displayed. These are the 7 tiles that you get to use during your turn in the game. You start the game by making a word with your hand and putting the starting letter on the 7,7 spot that is marked *.  
There should be a play button where you will type in your play. To play a tile it needs to be listed in a specific way. The tile that will be placed on the board is written and then the location written as a tuple in the form (r,c). Each tile should be separated by an &. For example if you wanted to play the word AA starting at (7,7) going to the right it would be entered as A:(7,7)&A:(7,8). 

If your word is not in the scrabble dictionary or the play was entered incorrectly, the game will reject your play and wait for a new one.
If your play is valid you will be sent to a new page that showcases your move and asks if this is what you intended. If you want to go back you can press the back button or you can confirm and move forward. You will be back to the home screen and your word will have been placed along with the computer’s word. In the bottom of the screen you will see the new updated scores. 

If you can't make a move you can type pass into the play and it will ask you to confirm and then the computer will make a move. 

There are some special rules in scrabble. After the first turn you must play a word that connects with something that is already on the board. The game has randomly spread out special board spots. There are 2 types that are labeled DL which doubles the amount the points the letter plays on top of it or TL which triples it. There is also DW and TW which respectively double the word and triple the point value of the whole word played.

The game can end in 2 different ways: it can end once all 100 tiles in the virtual bag have been used up or if you type end in the play. Once the game is over the game will tell you if you lost or won. The game will then be added to your stats which you can see be accessing the homepage. 

