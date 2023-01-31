import matplotlib.pyplot as plt
from matplotlib_venn import venn3
def mkplot(strTitle, strA, strB, strC, nA, nB, nC, nac, nab, nbc, nabc) :
    n111 = nabc
    n110 = abs(nabc - nab)
    n011 = abs(nabc - nbc)
    n101 = abs(nabc - nac)
    n100 = nA - n110 - n111 - n101
    n010 = nB - n110 - n111 - n011
    n001 = nC - n101 - n111 - n011
    nT = nA + nB + nC
    p111 = int(n111/nT*1000)/10
    p110 = int(n110/nT*1000)/10
    p011 = int(n011/nT*1000)/10
    p101 = int(n101/nT*1000)/10
    p100 = int(n100/nT*1000)/10
    p010 = int(n010/nT*1000)/10
    p001 = int(n001/nT*1000)/10
    labelA = strA+' = '+str(nA)
    labelB = strB+' = '+str(nB)
    labelC = strC+' = '+str(nC)
    labelAp = strA+' = '+str(int(nA/nT*1000)/10)
    labelBp = strB+' = '+str(int(nB/nT*1000)/10)
    labelCp = strC+' = '+str(int(nC/nT*1000)/10)
    venn3(subsets = (n100, n010, n110, n001, n101, n011, n111), set_labels = (labelA,labelB,labelC))
    plt.title(strTitle+' values')
    plt.show()
    venn3(subsets = (p100, p010, p110, p001, p101, p011, p111), set_labels = (labelAp,labelBp,labelCp))
    plt.title(strTitle+' per cent of total')
    plt.show()
mkplot('Canada', 'Scratch', 'RBG', 'Mix', 2563, 1018, 676, 418, 692, 380, 287)
mkplot('USA', 'Scratch', 'RBG', 'Mix', 1685, 1826, 1105, 642, 990, 935, 538)