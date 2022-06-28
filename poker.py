import random
import time

#ΣΗΜΑΝΤΙΚΗ ΣΗΜΕΙΩΣΗ!!! READ ME!!!
"""1. Η εύρεση του νικητή γίνεται με χρήση σκορ. Το σκορ του κάθε παίκτη
αποθηκεύεται σε λίστα με όνομα FinalScoreList[Αριθμός Παίκτη]."""
"""2. Η εύρεση του συνδιασμού φύλλων του κάθε παίκτη γίνεται με τη βοήθεια
δισδιάστατης λίστας με όνομα ScoreList[Αριθμός Παίκτη][0-6]. Οι εκχωρήσεις
στη συγκεκριμένη λίστα θα χρησιμοποιηθούν ως flags από τις συναρτήσεις του
προγράμματος. Παρακάτω φαίνεται η κωδικοποίηση τους με βάση το δεύτερο δείκτη
ο οποίος παίρνει τιμές από 0 έως και 6 με σειρά από το πιο δυνατό συνδιασμό
που έχει δείκτη 0 προς τον πιο αδύναμο με δείκτη 6 :
#######################################################################################################
#Δείκτες|Ρόλος δείκτη                                                                                 #
#   0   :Παίρνει την τιμή 4* σε περίπτωση που ο παίκτης έχει 'StraightFlush'.                         #
#   1   :Παίρνει την τιμή του δείκτη της κάρτας όταν ο παίκτης έχει 'Four of a kind'.                 #
#   2   :Παίρνει την τιμή 4* σε περίπτωση που ο παίκτης έχει 'Flush'.                                 #
#   3   :Παίρνει την τιμή 4* σε περίπτωση που ο παίκτης έχει 'Straight'.                              #
#   4   :Παίρνει την τιμή του δείκτη της κάρτας όταν ο παίκτης έχει 'Three of a kind'.                #
#   5   :Παίρνει την τιμή του δείκτη της κάρτας του δέυτερου ζεύγους, όταν ο παίκτης έχει 'Two pairs'.#
#   6   :Παίρνει την τιμή του δείκτη της κάρτας του ζεύγους, όταν ο παίκτης έχει 'OnePair' ή          #
#       |του πρώτου ζεύγους όταν έχει 'Two pairs'.                                                    #
#######################################################################################################
* Η τιμή 4 είναι η τιμή του φύλλου με τη μεγαλύτερη αξία στο χέρι του παίκτη καθώς οι κάρτες στο χέρι
ταξινομούνται με αύξουσα σειρά αξίας μέσω της συνάρτησης BubbleSortHand()."""
"""3. Ο υπολογισμός του σκορ εξηγείται αναλυτικά στα σχόλια της σειράς 217."""

    #---------ΣΥΝΑΡΤΗΣΕΙΣ-ΠΑΙΧΝΙΔΙΟΥ---------------------
"""Δημιουργούμε μία τράπουλα με τους αριθμούς και
τις φιγούρες από τη λίστα Axia και τα χρώματα από
τη λίστα Color. Η τράπουλα αποθηκεύεται στη λίστα
Deck."""
def CreateDeck(Deck, Axia, Color):
    for i in Axia:
        for j in Color:
            Deck.append([i,j])
    #----------------------------------------------------
"""Αρχικοποιούμε τη λίστα Player η οποία θα περιέχει
το χέρι του κάθε παίχτη. Τη λίστα ScoreList η οποία
θα μας δείχνει το συνδιασμό του κάθε παίχτη. Συνολικά,
μας ενδιαφέρουν 9 συνδιασμοί καρτών με βάση τους
οποίους θα υπολογιστεί το FinalScore το οποίο αποθηκεύεται
στην λίστα FinalScoreList, και θα αποφασιστεί ο νικητής."""
def GameSetup(NumberOfPlayers, Player, ScoreList, FinalScoreList, Deck):
    for PlayerNumber in range (NumberOfPlayers):
        Player.append([])
        ScoreList.append([])
        FinalScoreList.append(0)
    #----------------------------------------------------
"""Η συνάρτηση GameStart() καλείται στην αρχή κάθε γύρου και ανακατεύει
την τράπουλα (Deck), καλεί τη συνάρτηση CardDraw() και αρχικοποιεί με
την τιμή μηδέν τη ScoreList και FinalScoreList του κάθε παίκτη."""
def GameStart(NumberOfPlayers, Player, Deck, FinalScoreList):
    random.shuffle(Deck)
    CardDraw(NumberOfPlayers, Player, Deck)
    #MHDENISMOS SCORE
    for pl_numb in range (NumberOfPlayers):    
        ScoreList[pl_numb] = [0 for i in range(7)]
        FinalScoreList[pl_numb] = 0
    #----------------------------------------------------
"""Η συνάρτηση CardDraw() παίρνει κάρτες απο την τράπουλα (Deck) και
τις προσθέτει στα χέρια των παικτών."""
def CardDraw(NumberOfPlayers, Player, Deck):
    for pl_numb in range (NumberOfPlayers):
        for i in range (5):
            Player[pl_numb].append(Deck.pop(-1))
    #----------------------------------------------------
"""Η συνάρτηση EmptyHands() αδειάζει τις λίστες που βρίσκονται μέσα στη λίστα
Player. Πρακτικά, αδειάζει τα χέρια των παικτών και επιτστρέφει τις κάρτες στην
τράπουλα (Deck)."""
def EmptyHands(NumberOfPlayers, Player):
    for pl_numb in range (NumberOfPlayers):
        for i in range(5):
            Deck.append(Player[pl_numb].pop())
    #----------------------------------------------------
"""Η συνάρτηση CardValue() δέχεται τον αριθμό του παίκτη καθώς και τον
αριθμό της κάρτας και επιστρέφει τον αριθμό ή την φιγούρα της συγκεκριμένης
κάρτας. Η παρακάτω συνάρτηση μου είναι ιδιαίτερα χρήσιμη κατά τις εκτυπώσεις
καθώς οι κάρτες έχουν αξία 2-14 και δεν υπάρχουν φιγούρες για λειτουργικούς
λόγους.""" 
def CardValue(PlayerNumber, CardNumber):
    if Player[PlayerNumber][CardNumber][0] > 10:
        return Figures[Player[PlayerNumber][CardNumber][0] - 11]
    return Player[PlayerNumber][CardNumber][0]
    #----------------------------------------------------
"""Η συνάρτηση BubbleSortPlayerHand() ταξινομεί τα φύλλα του κάθε παίκτη κατά
αύξουσα αξία. Παράλληλα ελέγχει και την ύπαρξη ζεύγους έτσι ώστε να μας βοηθήσει
έπειτα στους ελέγχους συνδιασμών."""
def BubbleSortPlayerHand(PlayerNumber, Player, ScoreList):
    for i in range(5):
        for j in range(1, 5-i):
            if  Player[PlayerNumber][j-1][0] > Player[PlayerNumber][j][0]:
                temp=Player[PlayerNumber][j]
                Player[PlayerNumber][j] = Player[PlayerNumber][j-1]
                Player[PlayerNumber][j-1] = temp
            elif Player[PlayerNumber][j-1][0] == Player[PlayerNumber][j][0]:
                ScoreList[PlayerNumber][6] = 1
    #----------------------------------------------------
"""Η συνάρτηση FlushCheck() ελέγχει εάν όλα τα φύλλα του παίκτη έχουν το ίδιο
χρώμα. Εάν ισχύει το παραπάνω τότε το αντιστοιχο flag στην ScoreList παίρνει
τιμή και δηλώνεται η ύπαρξη χρώματος (Flush). Ο κώδικας της παρακάτω συνάρτησης
'τρέχει' μόνο εάν δεν έχει εντοπιστεί ζεύγος κατά την BubbleSortPlayerHand()."""
def FlushCheck(PlayerNumber, Player, ScoreList):
    if ScoreList[PlayerNumber][6] == 0:
        for i in range(4):
            ScoreList[PlayerNumber][2] = 4
            if  Player[PlayerNumber][i][1] != Player[PlayerNumber][i+1][1] and ScoreList[PlayerNumber][2] != 0:
                ScoreList[PlayerNumber][2] = 0
                break
    #----------------------------------------------------
"""Η συνάρτηση StraightCheck() ελέγχει εάν το κάθε φύλλο του παίκτη έχει αξία
κατά 1 μεγαλύτερη από το προηγούμενο. Εάν ισχύει το παραπάνω τότε το αντιστοιχο
flag στην ScoreList παίρνει τιμή και δηλώνεται η ύπαρξη κέντας (Straight).
Ο κώδικας της παρακάτω συνάρτησης 'τρέχει' μόνο εάν δεν έχει εντοπιστεί ζεύγος
κατά την BubbleSortPlayerHand()."""
def StraightCheck(PlayerNumber, Player, ScoreList):
    ScoreList[PlayerNumber][3] = 4
    for i in range(4):
        if  Player[PlayerNumber][i][0] + 1 != Player[PlayerNumber][i+1][0]:
            ScoreList[PlayerNumber][3] = 0
            break
    #----------------------------------------------------
"""Η συνάρτηση StraightFlush() ελέγχει εάν το flag στη θέση 3 της ScoreList
έχει τιμή. Εάν έχει τιμή αυτό σημαίνει πως ο παίκτης έχει χρώμα (Flush).
Οπότε η συνάρτηση ελέγχει εάν το φύλλο του είναι και κέντα (Straight).
Σε περίπτωση που είναι τότε ο παίκτης έχει κέντα χρώμα (StraightFlush)
το οποίο δηλώνεται όταν βάζουμε τιμή στη θέση 0 του ScoreList."""
def StraightFlush(PlayerNumber, Player, ScoreList):
    if ScoreList[PlayerNumber][2] != 0:
        StraightCheck(PlayerNumber, Player, ScoreList)
        if ScoreList[PlayerNumber][3] != 0:
            ScoreList[PlayerNumber][0] = 4
    #----------------------------------------------------
"""Η συνάρτηση PairCount() υπολογίζει τον αριθμό των ζευγών που
υπάρχουν στο χέρι ενός παίχτη εφόσον η συνάρτηση BubbleSortHand()
έχει βρει τουλάχιστον ένα ζευγάρι και έχει θέσει τιμή != 0 στη
θέση 7 της λίστας ScoreList για τον συγκεκριμένο παίχτη. Στην
περίπτωση όπου δεν είχε βρεθεί ζεύγος στον έλεγχο της
BubbleSortHand(), τότε η συνάρτηση καλεί τον έλεγχο για Κέντα
μέσω της Straight()."""
def PairCount(PlayerNumber, Player, ScoreList):
    if ScoreList[PlayerNumber][6] != 0:
        ScoreList[PlayerNumber][6] = 0
        PairCount = 0
        for i in range(1, 5):
 
            if Player[PlayerNumber][i-1][0] == Player[PlayerNumber][i][0] and i < 4:
                PairCount = PairCount + 1
                
            elif PairCount != 0 or i == 4:
                if Player[PlayerNumber][i-1][0] == Player[PlayerNumber][i][0] and i == 4:
                    PairCount = PairCount + 1
                    
                #4 OF A KIND
                if PairCount == 3:
                    ScoreList[PlayerNumber][1] = i - 1
                    break
            
                #3 OF A KIND
                elif PairCount == 2:
                    ScoreList[PlayerNumber][4] = i - 1

                #TWO PAIR
                elif PairCount == 1 and ScoreList[PlayerNumber][6] != 0:
                    ScoreList[PlayerNumber][5] = i - 1
                    break
                    
                #PAIR
                elif PairCount == 1:
                    ScoreList[PlayerNumber][6] = i - 1

                PairCount = 0
    else:
        StraightCheck(PlayerNumber, Player, ScoreList)
    #----------------------------------------------------
"""Η συνάρτηση PrintHand() εκτυπώνει το χέρι του κάθε παίχτη.
Χρησιμοποιώ την ιδιότητα της λίστας να μπορώ προσθέσω strings
κειμένου. Τέλος εκτυπώνω με σειρά τα περιεχόμενα των λιστών."""
def PrintHand(PlayerNumber, Player):
    print("Player ", PlayerNumber + 1, "'s hand")
    
    List1 = []
    List2 = []
    List3 = []
    List4 = []
    List5 = []
    List6 = []
    Card = [[], []]
    
    for i in range(len(Player[PlayerNumber])):
        Card[0] = CardValue(PlayerNumber,i)
        Card[1] = Player[PlayerNumber][i][1]
        if Card[0] == 10:
            List1 += ('┌────┐')
            List2 += ('│',Card[0],'     │')
            List3 += ('│    │')
            List4 += ('│   ',Card[1],'   │')
            List5 += ('│     ',Card[0],'│')
            List6 += ('└────┘')
        else: 
            List1 += ('┌────┐')
            List2 += ('│',Card[0],'      │')
            List3 += ('│    │')
            List4 += ('│   ',Card[1],'   │')
            List5 += ('│     ',Card[0],' │')
            List6 += ('└────┘')

    print(*List1)
    print(*List2)
    print(*List3)
    print(*List3)
    print(*List4)
    print(*List3)
    print(*List3)
    print(*List5)
    print(*List6)
    #----------------------------------------------------
"""Η συνάρτηση FinalScoreCalculator() δέχεται ως είσοδο τον αριθμό
του παίχτη, τη λίστα όπου περιέχεται το χέρι του και τη λίστα
με τα flags συνδιασμών, ScoreList. Τέλος ανάλογα με το συνδιασμό που
έχει ο κάθε παίχτης υπολογίζεται το του τελικό Σκορ με βάση τον
παρακάτω πίνακα:
##############################################################################################################################################
#StraightFlush  :Αξία μέγιστης κάρτας * 10.000.000                                                                                           #
#Four of a Kind :Αξία κάρτας καρέ * 1.000.000                                                                                                #
#Full House     :Αξία κάρτας τριπλέτας * 100.000                                                                                             #
#Flush          :Αξία μέγιστης κάρτας * 10.000 + Αξία 2ης μέγιστης κάρτας * 1.000 + ....                                                     #
#Straight       :Αξία μέγιστης κάρτας * 1.000                                                                                                #
#Three of a kind:Αξία κάρτας τριπλέτας * 100                                                                                                 #
#Two pairs      :Αξία μεγαλύτερου ζεύγους * 10 + Αξία δεύτερου ζεύγους * 1 + Αξία φύλλου που δεν είναι ζεύγος * 0,01                         #
#One pair       :Αξία ζεύγους * 1 + Αξία μεγαλύτερου φύλλου που δεν είναι ζεύγος * 0,1 + Αξία 2ου -//- * 0,01 + ....                         #
#High Card      :Αξία καρτών από τη μεγαλύτερη προς τη μικρότερη. Κάρτα(Κ)1 * 0,01 + Κ2 * 0,001 + Κ3 * 0,0001 + Κ4 * 0,00001 + Κ5 * 0,000001 #
##############################################################################################################################################
και τέλος, το αποθηκεύει στη λίστα FinalScoreList στο index που είναι
με ίσο με τον αριθμό του παίχτη (PlayerNumber)."""
def FinalScoreCalculator(PlayerNumber, Player, ScoreList, FinalScoreList):
    if ScoreList[PlayerNumber][0] != 0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][-1][0] * 10000000
        print("Player ", PlayerNumber +1, " has a Straight Flush up to", CardValue(PlayerNumber,-1), ".")
        return
    
    if ScoreList[PlayerNumber][1] != 0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][ScoreList[PlayerNumber][1]][0] * 1000000
        print("Player ", PlayerNumber +1, " has a Four of a Kind of ", CardValue(PlayerNumber, ScoreList[PlayerNumber][1]), "s.")
        return
    
    if ScoreList[PlayerNumber][4] != 0 and ScoreList[PlayerNumber][6] !=0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][ScoreList[PlayerNumber][4]][0] * 100000
        print("Player ", PlayerNumber +1, " has ", CardValue(PlayerNumber, ScoreList[PlayerNumber][4]), "s full of ", CardValue(PlayerNumber, ScoreList[PlayerNumber][6]), "s.")
        return

    if ScoreList[PlayerNumber][2] != 0:
        FinalScoreList[PlayerNumber] = 0
        Multiplier = 10000
        for i in range(4, -1, -1):
            FinalScoreList[PlayerNumber] = FinalScoreList[PlayerNumber] + Player[PlayerNumber][i][0] * Multiplier
            Multiplier = Multiplier / 10
        print("Player ", PlayerNumber + 1, " has a Flush up to", CardValue(PlayerNumber, -1), ".")
        return
            
    if ScoreList[PlayerNumber][3] != 0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][-1][0] * 1000
        print("Player ", PlayerNumber + 1, " has a Straight up to", CardValue(PlayerNumber, -1), ".")
        return
        
    if ScoreList[PlayerNumber][4] != 0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][ScoreList[PlayerNumber][4]][0] * 100
        print("Player ", PlayerNumber + 1, " has a Three of a Kind of ", CardValue(PlayerNumber, ScoreList[PlayerNumber][4]), "s.")
        return
    
    if ScoreList[PlayerNumber][5] != 0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][ScoreList[PlayerNumber][5]][0] * 10 + Player[PlayerNumber][ScoreList[PlayerNumber][6]][0]
        if ScoreList[PlayerNumber][5] == 3:
            if ScoreList[PlayerNumber][6] == 2:
                FinalScoreList[PlayerNumber] = FinalScoreList[PlayerNumber] + Player[PlayerNumber][0][0] * 0.01
            else:
                FinalScoreList[PlayerNumber] = FinalScoreList[PlayerNumber] + Player[PlayerNumber][2][0] * 0.01
        else:
            FinalScoreList[PlayerNumber] = FinalScoreList[PlayerNumber] + Player[PlayerNumber][-1][0] * 0.01
        print("Player ", PlayerNumber + 1, " has a pair of ", CardValue(PlayerNumber, ScoreList[PlayerNumber][5]), "s and a pair of ", CardValue(PlayerNumber, ScoreList[PlayerNumber][6]), "s.")
        return
            
    if ScoreList[PlayerNumber][6] != 0:
        FinalScoreList[PlayerNumber] = Player[PlayerNumber][ScoreList[PlayerNumber][6]][0]
        Multiplier = 0.0001
        for i in range(5):
            if ScoreList[PlayerNumber][6] - 1 != i and ScoreList[PlayerNumber][6] != i:
                FinalScoreList[PlayerNumber] = FinalScoreList[PlayerNumber] + Player[PlayerNumber][i][0] * Multiplier
                Multiplier = Multiplier * 10
        
        print("Player ", PlayerNumber + 1, " has a pair of ", CardValue(PlayerNumber, ScoreList[PlayerNumber][6]), "s.")
        return    
    
    FinalScoreList[PlayerNumber] = 0
    Multiplier = 0.01
    for i in range(4,-1,-1):
        FinalScoreList[PlayerNumber] = FinalScoreList[PlayerNumber] + Player[PlayerNumber][i][0] * Multiplier
        Multiplier = Multiplier / 10
    print("Player ", PlayerNumber + 1, " has high card ", CardValue(PlayerNumber, -1), ".")
    #----------------------------------------------------
"""Η συνάρτηση FindWinner() δέχεται ως είσοδο τον αριθμό των παιχτών
και τη λίστα με το τελικό σκορ τους. Με βάση το τελικό Σκορ βρίσκει
ποιος έχει το μέγιστο και άρα, είναι ο νικητής."""
def FindWinner(NumberOfPlayers, FinalScoreList):
    MaxScore = FinalScoreList[0]
    MaxPlayer = 0
    
    for i in range(1,NumberOfPlayers):
        if FinalScoreList[i] > MaxScore:
            MaxScore = FinalScoreList[i]
            MaxPlayer = i
            
    Count = FinalScoreList.count(MaxScore)
    
    if Count == 1:
        print("Player ", MaxPlayer +1, "has won!")
        return
    
    if Count == NumberOfPlayers:
        print("DRAW!")
        return
    print (Count, NumberOfPlayers)
    print("Players ", MaxPlayer + 1, end="")
    for i in range(MaxPlayer, NumberOfPlayers):
        if MaxScore == FinalScoreList[i]:
            print(" ", i + 1, end="")
    print(" have won!")
    #----------------------------------------------------

    #----ΚΥΡΙΩΣ-ΠΡΟΓΡΑΜΜΑ---------------------------------
#ΑΡΧΙΚΟΠΟΙΗΣΗ ΤΟΥ ΠΑΙΧΝΙΔΙΟΥ
NumberOfPlayers = 2
Axia = [i for i in range(2,14)]
Figures = ["J", "Q", "K", "A"]
Color = ["♠", "♦", "♥", "♣"]
Deck = []
Player = []
ScoreList = []
FinalScoreList = []

#ΔΗΜΙΟΥΡΓΙΑ ΤΡΑΠΟΥΛΑΣ
CreateDeck(Deck, Axia, Color)

#ΑΡΧΙΚΟΠΟΙΗΣΗ SCORE ΚΑΙ ΠΑΙΧΤΩΝ
GameSetup(NumberOfPlayers, Player, ScoreList, FinalScoreList, Deck)

    #----ΕΠΑΝΑΛΗΨΗ-ΠΑΙΧΝΙΔΙΟΥ-----------------------------
Continue = 'y'
while Continue == 'y' or Continue == 'Y':

    #ΑΡΧΗ ΠΑΙΧΝΙΔΙΟΥ
    GameStart(NumberOfPlayers, Player, Deck, FinalScoreList)

    #ΕΛΕΓΧΟΣ ΦΥΛΛΩΝ
    for PlayerNumber in range(NumberOfPlayers):
        
    #BUBBLESORTING ΦΥΛΛΩΝ ΚΑΙ ΕΛΕΓΧΟΣ ΓΙΑ ΖΕΥΓΗ
        BubbleSortPlayerHand(PlayerNumber, Player, ScoreList)
        
    #ΕΜΦΑΝΙΣΗ ΦΥΛΛΩΝ ΠΑΙΚΤΩΝ
        PrintHand(PlayerNumber, Player)
        
    #FLUSH CHECK
        FlushCheck(PlayerNumber, Player, ScoreList)

    #STRAIGHT FLUSH CHECK
        StraightFlush(PlayerNumber, Player, ScoreList)
    
    #STRAIGHT OR PAIRS
        PairCount(PlayerNumber, Player, ScoreList)

    #ΑΠΟΤΕΛΕΣΜΑ
    for PlayerNumber in range (NumberOfPlayers):
        FinalScoreCalculator(PlayerNumber, Player, ScoreList, FinalScoreList)

    FindWinner(NumberOfPlayers, FinalScoreList)

    #ΕΡΩΤΗΣΗ ΓΙΑ ΕΞΟΔΟ
    print("Another Round? (y/n)")
    Continue = 'p'
    while Continue != 'y' and Continue != 'Y' and Continue != 'n' and Continue != 'N':
        Continue = str(input())

    if Continue == 'y' or Continue == 'Y':
        EmptyHands(NumberOfPlayers, Player)

    #----ΤΕΛΟΣ-ΕΠΑΝΑΛΗΨΗΣ-ΠΑΙΧΝΙΔΙΟΥ--------------------
