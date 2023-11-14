import bin.Core as C
import bin.Hex as H

#TODO - Zmodyfikować grida aby był tablica dwuwymiarowa, ulatwi to pozniejsze wplywanie komorek na siebie wzajemnie i umozliwi dzialanie klasy automatu

def genGrid(nHeight, nWidth): # 8 /12
    arrGrid = []
    nModifier = 0
    for nRow in range(nHeight):
        row = []
        for nCell in range(nWidth):
            if nRow % 2 == 0:
                row.append(H.Hex(20 + nCell*88, 20 + nRow*26))
            else:
                row.append(H.Hex(64 + nCell*88, 20 + nRow*26))
        arrGrid.append(row)
        nModifier = 1 - nModifier
    return arrGrid