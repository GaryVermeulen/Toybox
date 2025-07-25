# main.py
# Main script file for Simple-Ton
# New: 7/25/25
#

from createKG import loadKG
from createKG import plotG


if __name__ == "__main__":

    LTG, nLTG = loadKG()

    plotG(LTG)
    plotG(nLTG)

    
