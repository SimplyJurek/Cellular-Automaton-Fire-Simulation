import bin.Core as C
import bin.Hex as H

windowOffset = 20 # odleglosć od ramki okna

def genGrid(nHeight, nWidth):
    arrGrid = []

    for nColumn in range(nWidth):
        column = []
        voffset = windowOffset if nColumn % 2 == 0 else C.HEXH / 2 + windowOffset
        for nCell in range(nHeight):
            column.append(H.Hex(windowOffset + nColumn * (C.HEXW * 3/4), voffset + nCell * C.HEXH))
        arrGrid.append(column)

    for col_index, column in enumerate(arrGrid):
        for hex_index, hex_obj in enumerate(column):
            hex_obj.findNeighbors(arrGrid, [col_index, hex_index])
                

    return arrGrid