# This class holds the information for the squares on the board

class Square():
    
    def __init__(self, val, bomb):
        self.val = val
        self.revealed = False
        self.bomb = bomb
        self.flagged = False

    # to send the board the appropriate value to display
    def Print(self):

        # send our number if we are revealed
        if self.revealed:
            
            # we want to know if we are actually a number or an empty box
            if self.val == 0:
                return " - "
            else:
                return " {} ".format(self.val)
        else:
            
            # check if we are flagged
            if self.flagged:
                return "[F]"
            else:

                # send back an empty square
                return "[ ]"
