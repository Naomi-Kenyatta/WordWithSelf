from random import shuffle
from helpers import random_tuples
from operator import itemgetter
from cs50 import SQL

Points = {"A": 1,"B": 3,"C": 3,"D": 2,"E": 1,"F": 4,"G": 2,"H": 4,"I": 1,"J": 1,"K": 5,
                 "L": 1,"M": 3,"N": 1,"O": 1,"P": 3,"Q": 10,"R": 1,"S": 1,"T": 1,
                 "U": 1,"V": 4,"W": 4,"X": 8,"Y": 4,"Z": 10}


db = SQL("sqlite:///words.db")

class Tile:
    def __init__(self, char, points):
        # Initialize tile
        self.letter = char.upper()
        if self.letter in points:
            self.value = points[self.letter]
        else:
            self.value = 0

    def get_letter(self):
        return self.letter

    def get_value(self):
        return self.value

class Bag:
    def __init__(self):
        # Makes initial bag of tiles
        # Add function defined below
        self.bag = []
        self.add(Tile("A", Points), 9)
        self.add(Tile("B", Points), 2)
        self.add(Tile("C", Points), 2)
        self.add(Tile("D", Points), 4)
        self.add(Tile("E", Points), 12)
        self.add(Tile("F", Points), 2)
        self.add(Tile("G", Points), 3)
        self.add(Tile("H", Points), 2)
        self.add(Tile("I", Points), 9)
        self.add(Tile("J", Points), 9)
        self.add(Tile("K", Points), 1)
        self.add(Tile("L", Points), 4)
        self.add(Tile("M", Points), 2)
        self.add(Tile("N", Points), 6)
        self.add(Tile("O", Points), 8)
        self.add(Tile("P", Points), 2)
        self.add(Tile("Q", Points), 1)
        self.add(Tile("R", Points), 6)
        self.add(Tile("S", Points), 4)
        self.add(Tile("T", Points), 6)
        self.add(Tile("U", Points), 4)
        self.add(Tile("V", Points), 2)
        self.add(Tile("W", Points), 2)
        self.add(Tile("X", Points), 1)
        self.add(Tile("Y", Points), 2)
        self.add(Tile("Z", Points), 1)
        shuffle(self.bag)

    def add(self, tile, num):
        for i in range(num):
            self.bag.append(tile)

    def draw(self):
        # draw from bag
        return self.bag.pop()

    def num_remaining(self):
        # get number of remaining tiles
        return len(self.bag)


class Hand:
    def __init__(self, bag):
        # Initialize hand
        # add function defined below
        self.hand = []
        self.bag = bag
        for i in range(7):
            self.add()

    def get_hand(self):
        return self.hand

    def getHandArr(self):
        a = []
        for tile in self.hand:
            a.append(tile.get_letter())
        return a

    def get_length(self):
        return len(self.hand)

    def add(self):
        self.hand.append(self.bag.draw())

    def remove(self, tile):
        for i in self.hand:
            if i.letter == tile.letter:
                self.hand.remove(i)
                break

    def refill(self):
        while self.bag.num_remaining() > 0 and self.get_length() < 7:
            self.add()

    def find(self, letter):
        for tile in self.hand:
            if tile.get_letter() == letter:
                return True
        return False


class Player:
    def __init__(self, bag):
        # Initialize player hand and score
        self.hand = Hand(bag)
        self.score = 0

    def get_hand(self):
        return self.hand.get_hand()

    def get_score(self):
        return self.score

    def add_points(self, points):
        self.score += points


class Board:
    def __init__(self):
        # Creates a 2-dimensional array that will serve as the board, as well as adds in the premium squares.
        self.board = [["" for i in range(15)] for j in range(15)]
        self.words = []
        self.add_multipliers()
        self.board[7][7] = "*"

    def get_board(self):
       return self.board

    def get_words(self):
        return self.words

    def add_multipliers(self):
        TW = []
        DW = []
        TL = []
        DL = []
        random_tuples(TW, 8)
        random_tuples(DW, 17)
        random_tuples(TL, 12)
        random_tuples(DL, 24)
        for tup in TW:
            self.board[tup[0]][tup[1]] = "TW"
        for tup in DW:
            self.board[tup[0]][tup[1]] = "DW"
        for tup in TL:
            self.board[tup[0]][tup[1]] = "TL"
        for tup in DL:
            self.board[tup[0]][tup[1]] = "DL"

    def place_word(self, info, player):
        info = parse(info,player)
        if info == [0]:
            return False
        if(not Playerlegal(player.hand, self, info)): # adjustment HERE
            return False
        real = word(self, info)
        print(real)
        if not real:
            return False
        for i in info:
            self.board[i[1][0]][i[1][1]] = i[0]
        print(player.hand.getHandArr())
        return True

    def placeword(self, info, player):
        info = parse(info,player)
        if info == [0]:
            return False
        if(not Playerlegal(player.hand, self, info)): # adjustment HERE
            return False
        real = word(self, info)
        if not real:
            return False
        else:
            player.score += real #points
        for i in info:
            self.board[i[1][0]][i[1][1]] = i[0]
            player.hand.remove(Tile(i[0], Points))
        player.hand.refill()
        print(player.hand.getHandArr())
        return True

    def place_word_comp(self, move, computer):
        if move == (0,0):
            return False
        points = 0
        multiplier = 1
        loc = move[1]
        direction = mT(move[2], -1)
        for i in range(len(move[0])):
            if len(self.board[loc[0]][loc[1]]) != 1:
                letter = move[0][i]
                if self.board[loc[0]][loc[1]] == "DW":
                    multiplier *= 2
                    points += calculate(letter)
                    computer.hand.remove(Tile(letter, Points))
                elif self.board[loc[0]][loc[1]] == "TW":
                    multiplier *= 3
                    points += calculate(letter)
                    computer.hand.remove(Tile(letter, Points))
                elif self.board[loc[0]][loc[1]] == "TL":
                    points += 3 * calculate(letter)
                    computer.hand.remove(Tile(letter, Points))
                elif self.board[loc[0]][loc[1]] == "DL":
                    points += 2 * calculate(letter)
                    computer.hand.remove(Tile(letter, Points))
                else:
                    points += calculate(letter)
                    computer.hand.remove(Tile(letter, Points))
                self.board[loc[0]][loc[1]] = letter
            else:
                points += calculate(self.board[loc[0]][loc[1]])
            loc = addT(loc, direction)
            computer.hand.refill()
        computer.score += points * multiplier
        return True

class Computer:
    def __init__(self, bag):
        # Initialize player hand and score
        self.hand = Hand(bag)
        self.score = 0

    def get_hand(self):
        return self.hand.get_hand()

    def get_score(self):
        return self.score

    def add_points(self, points):
        self.score += points

    def move(self,board):
        possible = []
        for i in range(15):
            for j in range(15):
                if len(board.board[i][j]) != 1:
                    continue
                start_letter = board.board[i][j] + "%"
                end_letter = "%" + board.board[i][j]
                start = db.execute("SELECT word FROM dictionary WHERE word LIKE ? AND LENGTH(word) < 13 ORDER BY value DESC", start_letter)
                end = db.execute("SELECT word FROM dictionary WHERE word LIKE ? AND LENGTH(word) < 13 ORDER BY value DESC", end_letter)
                for word in start:
                    term = word["word"]
                    if legal(self.hand, board, term, (i,j), (0,-1)):
                        if j == 0 or len(board.board[i][j-1]) != 1:
                            possible.append((term, (i,j), (0,-1), calculate(term)))
                            break
                    if legal(self.hand, board, term, (i,j), (-1,0)):
                        if i == 0 or len(board.board[i-1][j]) != 1:
                            possible.append((term, (i,j), (-1,0), calculate(term)))
                            break
                for word in end:
                    term = word["word"]
                    termlen = len(term)
                    if legal(self.hand, board, term, (i,j - termlen), (0,-1)):
                        if j == 14 or len(board.board[i][j+1]) != 1:
                            possible.append((term, (i,j - termlen), (0,-1), calculate(term)))
                            break
                    if legal(self.hand, board, term, (i - termlen,j), (-1,0)):
                        if i == 14 or len(board.board[i+1][j]) != 1:
                            possible.append((term, (i - termlen, j), (-1,0), calculate(term)))
                            break
        if not possible:
            return (0,0)
        print(possible)
        return max(possible, key=itemgetter(3))


def parse(info, player):
    if info.find(":") == -1:
        return [0]
    parsed = []
    a = info.split("&")
    for item in a:
        item = item.split(":")
        if len(item) != 2 or not item[0].isalpha() or not player.hand.find(item[0]): #the letter is not a letter WRITE THE FUNCTION
            return [0]
        t = item[1] # thing to be turned into a tuple
        #check the intergets are in the range and that they are ints
        try:
            tup = eval(t)
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            return [0]
        if not isinstance(tup, tuple) or len(tup) != 2 or not isinstance(tup[0], int) or not isinstance(tup[1], int) or (not (tup[0] in range(0,15))) or (not (tup[1] in range(0,15))):
            return [0]
        pair = []
        pair.append(item[0])
        pair.append(tup)
        parsed.append(pair)
    parsed = sorted(parsed, key=itemgetter(1)) #sorts the array
    return parsed
    #First Determine if it goes left and right or up and down
    #Check up and down

def direction(a):
    #First Determine if it goes left and right or up and down
    #Check up and down
    Vdir = True
    for i in range(1, len(a)):
        if(a[i][1][1]!=a[i-1][1][1]):
            Vdir = False;

    #Check right and left
    Hdir = True
    for i in range(1, len(a)):
        if(a[i][1][0]!=a[i-1][1][0]):
            Hdir = False;

    if(not(Vdir or Hdir)):
        return (0,0) #gotta be in a straight line this is the false return
    elif (Vdir):
        return (-1,0)
    else:
        return (0,-1)

# checks if word is valid and returns points
def word(board,a): #points
    points = 0
    specialEnd = []
    word = a[0][0]
    d = direction(a)
    start = a[0][1]
    connected = False
    if(len(a)==1):
        return oneLetter(board,a)
    if(board.board[start[0]][start[1]] == "*"):
        connected = True
    #add things for first turn
    start = addT(a[0][1],d)

    while(start[0] >= 0 and start[1] >= 0):
        letter = board.board[start[0]][start[1]]
        if(len(letter) == 1):
            connected = True
            word = ""+letter+word
        else:
            break
        start = addT(start,d)
    #rstart = start
    start = a[0][1]
    # now go to the right

    if(len(board.board[start[0]][start[1]]) == 2):
        print(len(board.board[start[0]][start[1]]))
        if(board.board[start[0]][start[1]][1] == "W"): #checks if DW or TW
            specialEnd.append(board.board[start[0]][start[1]])
        else:
            if(board.board[start[0]][start[1]] == "TL"):
                points += 2*Points[a[0][0]]
            else:
                points += Points[a[0][0]]
    start = addT(a[0][1],mT(d,-1))
    i = 1
    while start[0] < 15 and  start[1] < 15:
        if(len(board.board[start[0]][start[1]])!=1):
            if i >= len(a):
                break
            if(start == a[i][1]):
                print(len(board.board[start[0]][start[1]]))
                if(len(board.board[start[0]][start[1]]) == 2):
                    print(len(board.board[start[0]][start[1]]))
                    if(board.board[start[0]][start[1]][1] == "W"): #checks if DW or TW
                        specialEnd.append(board.board[start[0]][start[1]])
                    else:
                        if(board.board[start[0]][start[1]] == "TL"):
                            points += 2*Points[a[i][0]]
                        else:
                            points += Points[a[i][0]]
                word = word + a[i][0]
                i += 1
            else:
                return False
        else:
            connected = True
            if(board.board[start[0]][start[1]] == "*"):
                word = word + a[i][0]
            else:
                word = word + board.board[start[0]][start[1]]
        start = addT(start,mT(d,-1))
    board.words.append(word)

    points += calculate(word)
    print(specialEnd)
    print(points)
    for i in specialEnd:
        if i == "TW":
            points = points*3
        if i == "DW":
            points = points*2
    print(points)

    return points*indic(word)*connected*nextl(a,d, board)


def indic(word):
    #now check if the word formed is in the dic
    dic = open("scrabble.txt","r").read()
    word = word.upper()

    if(dic.find(word) == -1):
        #not a valid word
        return False
    return True


def oneLetter(board,a): #points
    start = a[0][1]

    if(board.board[start[0]][start[1]] == "*"):
        return indic(a[0][0])*calculate(a[0][0])

    #up?
    connected = False
    d = (-1,0)
    start = a[0][1]
    word = a[0][0]
    start = addT(start,d)

    while(start[0] >= 0 and  start[1] >= 0):
        letter = board.board[start[0]][start[1]]
        if(len(letter) == 1):
            connected = True
            word = letter+word
        else:
            break
        start = addT(start,d)
        print(word)

    d = (1,0)
    start = a[0][1]
    start = addT(a[0][1],d)

    while(start[0] < 15 and  start[1] < 15):
        letter = board.board[start[0]][start[1]]
        if(len(letter) == 1):
            connected = True
            word = letter+word
        else:
            break
        start = addT(start,d)

    start = a[0][1]
    points = calculate(word)
    if(not(len(word)==1)):
        if(board.board[start[0]][start[1]] == "DW"):
            points = points*2
        elif(board.board[start[0]][start[1]] == "TW"):
            points = points*3
        elif(board.board[start[0]][start[1]] == "TL"):
            points += Points[a[0][0]]*2
        elif(board.board[start[0]][start[1]] == "DL"):
            points += Points[a[0][0]]
        return indic(word)*points

    #left
    d = (0,-1)

    start = addT(start,d)

    while(start[0] >= 0 and  start[1] >= 0):
        letter = board.board[start[0]][start[1]]
        if(len(letter) == 1):
            connected = True
            word = letter+word
        else:
            break
        start = addT(start,d)

    d = (0,1)
    start = a[0][1]
    start = addT(a[0][1],d)
    while(start[0] < 15 and  start[1] < 15):
        letter = board.board[start[0]][start[1]]
        if(len(letter) == 1):
            connected = True
            word = ""+letter+word
        else:
            break
        start = addT(start,d)


    start = a[0][1]
    points = calculate(word)
    if(not(len(word)==1)):
        if(board.board[start[0]][start[1]] == "DW"):
            points = points*2
        elif(board.board[start[0]][start[1]] == "TW"):
            points = points*3
        elif(board.board[start[0]][start[1]] == "TL"):
            points += Points[a[0][0]]*2
        elif(board.board[start[0]][start[1]] == "DL"):
            points += Points[a[0][0]]
        return indic(word)*points

    if(len(word)!=1):
        return indic(word)*calculate(word)

    #not connected!
    return False


#adds tuples
def addT(a,b):
    return (a[0]+b[0],a[1]+b[1])

def mT(a,b):
    return (a[0]*b,a[1]*b)

def legal(hand, board, word, start, d):
    #add things for first turn
    #now go to the right
    letters_available = hand.getHandArr()
    wordlen = len(word)
    placed = False
    i = 0
    first = True
    if start[0] < 0 or start[1] < 0:
        return False
    while start[0] < 15 and start[1] < 15 and i < wordlen:
        if len(board.board[start[0]][start[1]]) == 1:
            if board.board[start[0]][start[1]] == word[i]:
                i += 1
            else:
                return False
        else:
            if word[i] not in letters_available:
                return False
            if not first:
                opposite = mT(addT(d, (1,1)), -1)
                plus = addT(start, opposite)
                if not(plus[0] > 14 or plus[1] > 14 or plus[0] < 0 or plus[1] < 0):
                    if len(board.board[plus[0]][plus[1]]) == 1:
                        return False
                minus = addT(start, mT(opposite, -1))
                if not(minus[0] > 14 or minus[1] > 14 or minus[0] < 0 or minus[1] < 0):
                    if len(board.board[minus[0]][minus[1]]) == 1:
                        return False
            placed = True
            letters_available.remove(word[i])
            i += 1
        start = addT(start, mT(d,-1))
        first = False
    if i < wordlen:
        return False
    if not placed:
        return False
    if start[0] < 15 and start[1] < 15 and len(board.board[start[0]][start[1]]) == 1:
        return False
    return True

def Playerlegal(hand, board, a):
    #check if move is legal for player
    letters_available = hand.getHandArr()
    for i in a:
        if i[0] not in letters_available:
            return False
        letters_available.remove(i[0])
    return True


def calculate(word):
    score = 0
    for letter in word:
        score += Points[letter]
    return score

def nextl(info,d, board):
    d = addT((1,1),d) #(1,1) + (0,-1) = (1,0)
    for i in info:
        m = addT(i[1],d)
        if not (m[0] > 14 or m[1] > 14 or m[0] < 0 or m[1] < 0):
            if(len(board.board[m[0]][m[1]]) == 1):
                print("hi")
                return False
        m = addT(i[1],mT(d,-1))
        if not(m[0] > 14 or m[1] > 14 or m[0] < 0 or m[1] < 0):
            if(len(board.board[m[0]][m[1]]) == 1):
                print("Hi")
                return False
    return True


"""def legal(hand, word, board, (i,j), direction):
    letters_available = hand.getHandArr()
    for letter in word:
        if letter not in letters_available:
            return False
        letters_available.remove(letter)"""

"""b= Bag()
p = Player(b)
pa=parse("A:(0,1)&A:(0,2)", p)
print(p.hand.getHandArr())
bo = Board()
print(word(bo,pa))

bo.place_word("A:(0,1)&A:(0,2)",p)
print(bo.board)"""

"""bag = Bag()
computer = Computer(bag)
board = Board()

board.board[0][0] = "A"
board.board[0][1] = "T"
board.board[1][0] = "R"
board.board[2][0] = "E"

print(computer.hand.getHandArr())
print(board.board)
print(board.place_word_comp(computer.move(board), computer))
print(computer.hand.getHandArr())
print(board.board)
print(computer.score)"""

