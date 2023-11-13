import bin.Core as C
import bin.Hex as H

#TODO - Zmodyfikować grida aby był tablica dwuwymiarowa, ulatwi to pozniejsze wplywanie komorek na siebie wzajemnie i umozliwi dzialanie klasy automatu

def genGrid(nHeight, nWidth):
    arrGrid = [H.Hex(20, 20)]
    nModifier = 0
    for nRow in range(nWidth):
        for nCell in range(nHeight):
            if not (nRow == 0 and nCell == 0):   # skip first hex as its inialized with the array
                arrGrid.append(H.Hex(20 + (nRow * (C.HEXW * 3/4)), 20 + ((C.HEXH / 2) * nModifier) + (nCell * C.HEXH)))
        if nRow % 2 == 1:
            arrGrid.pop()
            nModifier = 0
        else: 
            nModifier = 1
    print(arrGrid)
    return arrGrid