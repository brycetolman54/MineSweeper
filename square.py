# This class holds the information for the squares on the board

class Square():
    
    def __init__(self):
        self.val = 0
        self.revealed = False
        self.bomb = False
        self.flagged = False

    # to send the board the appropriate value to display
    def Print(self):

        # send our number if we are revealed
        if self.revealed:
           
            # if we are a bomb, say it
            if self.bomb:
                return " \u001b[38;5;160mB\u001b[38;5;15m "

            # we want to know if we are actually a number or an empty box
            if self.val == 0:
                return " - "
            else:
                color = ""
                if self.val == 1:
                    color = "12m"
                elif self.val == 2:
                    color = "226m"
                elif self.val == 3:
                    color = "22m"
                elif self.val == 4:
                    color = "5m"
                elif self.val == 5:
                    color = "46m"
                elif self.val == 6:
                    color = "56m"
                elif self.val == 7:
                    color = "242m"
                elif self.val == 8:
                    color = "56m"
                return " \u001b[38;5;{}{}\u001b[38;5;15m ".format(color, self.val)
        else:
            
            # check if we are flagged
            if self.flagged:
                return "[F]"
            else:

                # send back an empty square
                return "[ ]"
