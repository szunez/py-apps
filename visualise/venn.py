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
    venn3(subsets = (n100, n010, n110, n001, n101, n011, n111), set_labels = (strA, strB, strC))
    plt.title(strTitle)
    plt.show()
mkplot('Canada', 'Scratch', 'RBG', 'Mix', 2563, 1018, 676, 418, 692, 380, 287)
mkplot('USA', 'Scratch', 'RBG', 'Mix', 1685, 1826, 1105, 642, 990, 935, 538)