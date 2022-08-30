import sys
import os
from pathlib import Path
def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))
def convertToSec(s) :
    l = list(map(float, s.split(':')))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600)))
def getProfileSections(elevationProfile) :
    d = 0
    dd = 0
    olgaGeometry = '        '
    for g in elevationProfile :
        if dd <= 4 :
            olgaGeometry = olgaGeometry + g + ' ' * (13-len(g))
        else :
            olgaGeometry = olgaGeometry + '\n        ' + g + ' ' * (13-len(g))
            dd = 0
        d = d + 1
        dd = dd + 1
    return olgaGeometry
def alignProfileDataWithSemicolon(profile) :
    i = 0
    j = 0
    repeatData = 0
    skipped = 0
    for d in profile :
        for g in geometry[i] :
            while float(g) > float(geometry[geomIndex][j+repeatData+skipped]) :
                repeatData = repeatData + 1
            if repeatData > 0 :
                profile[i][j] = str(1 + repeatData) + ':' + profile[i][j]
            skipped = skipped + repeatData
            repeatData = 0
            j = j + 1
        skipped = 0
        j = 0
        i = i + 1
def alignProfileData(profile) :
    i = 0
    j = 0
    repeatData = 0
    skipped = 0
    for d in profile :
        for g in geometry[i] :
            while float(g) > float(geometry[geomIndex][j+repeatData+skipped]) :
                repeatData = repeatData + 1
            if repeatData > 0 :
                profile[i][j] = str(profile[i][j] + ' ') * int(repeatData + 1)
                profile[i][j] = str(1 + repeatData) + ':' + profile[i][j]
            skipped = skipped + repeatData
            repeatData = 0
            j = j + 1
        skipped = 0
        j = 0
        i = i + 1
def writeDebugFile() :
    debugFolder = Path(os.path.expanduser('~')+'/src/py-apps/olgapy/') #this needs to be generalised and tested on Windows OS
    #os.remove(reportFolder / str(simCase + '.ppl'))
    debugFile = open(debugFolder / 'debug.log','w')
    for dataline in geometry :
        debugFile.write(str(dataline)+'\n')
    debugFile.close()
def writeOlgaProfile() :
    dataline = ''
    #reportFolder = Path(os.path.expanduser('~')+'/src/py-apps/olgapy/') #this needs to be generalised and tested on Windows OS
    reportFolder = Path(os.path.expanduser('.'))
    reportFile = open(reportFolder / str(simCase + '.ppl'),'w')
    reportFile.write('\'OLGA 7.3.0.110137\'\nPROFILE PLOT\nINPUT FILE\n\''+simCase+'.key\'\nPVT FILE\n\'../'+simCase+'.tab\'\nDATE\n\'2000-10-16 12:34:56\'\nPROJECT\n\''+simCase+'\'\nTITLE\n\'Base Case\'\nAUTHOR\n\'evoleap\'\nNETWORK\n1\nGEOMETRY \' ('+x_unit+')  \'\nBRANCH\n\''+simBranch+'\'\n'+str(mostSections-1)+'\n')
    reportFile.write(x_positons + '\n' + y_positons + '\n')
    reportFile.write('CATALOG \n1\nPT \'SECTION:\' \'BRANCH:\' \''+simBranch+'\' \'('+y_unit+')\' \'Pressure\'\n')
    reportFile.write('TIME SERIES  \' (S)  \'\n')
    tthreshold = 0.1 #seconds
    tsimbefore = -1 *  tthreshold
    for k in range(j) :
        tthreshold = 0.1 #seconds
        y = 0
        tsim = eformat(convertToSec([s for s in data[k] if 'time' in s][0][4:]),6,3)
        print(float(tsim)-tsimbefore)
        for x in data[k] :
            if y == 0 :
                dataline = str(tsim) + '\n' + x
            elif x[:4] == 'time':
                datline = dataline
            elif x[:2] == 'dt':
                datline = dataline
            elif x[:4] == 'step':
                datline = dataline
            else :
                dataline = dataline.strip() + str(' ') + x
            y = y + 1
        if float(tsim) - tsimbefore >= tthreshold :
            reportFile.write(dataline+'\n')
            tsimbefore = float(tsim)
        if float(tsim) - tsimbefore < tthreshold :
            reportFile.write(dataline+'\n')
        tsimbefore = float(tsim)
    reportFile.close()
global data, geometry, x_positons, y_positons
global simCase, simBranch, x_unit, y_unit
debug = False
rawdata = []
datamap = []
data = []
geometry = []
getValue = False
getGeometry = False
mostSections = 0
var = ''                                              # This will be the simulated variable of interest
geom = ''                                             # This will be the pipe distance point associated with a given variable of interest
strKeep = 'time'
#dumpChars = '()[] \n'
# initialisation
#   options
if len(sys.argv) > 1 :
    if sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == '-man' :
        print('*' * 99+'\n*     Welcome to get-PPL!, a Python 3.x command-line utility for working with OLGA output data     *\n'+'*' * 99+'\nusage: python get-ppl.py sps_sim_data [--help][--debug][--case][--branch][--x_unit][--y_unit]\n	\nwhere: sps_sim_data is a path and filename of .txt output file [ ./data/P_liq.txt ] \n \noptions:\n	[--help   [-h][-man] documentation]\n	[--debug  [-d] write debug.log file]\n	[--case   [-c] define a case name, default case name is \'fake\']\n	[--branch [-b] define a branch name, default case name is \'fake\']\n	[--x_unit [-x] specify units for profile distances]\n	[--y_unit [-y] specify units for profile variable]\n	')
        quit()
    for i in range(len(sys.argv)) :
        if sys.argv[i] == '--case' or sys.argv[i] == '-c' :
            simCase = str(sys.argv[i+1])
        elif sys.argv[i] == '--branch' or sys.argv[i] == '-b' :
            simBranch = str(sys.argv[i+1])
        elif sys.argv[i] == '--x_unit' or sys.argv[i] == '-x' :
            x_unit = str(sys.argv[i+1])
        elif sys.argv[i] == '--y_unit' or sys.argv[i] == '-y' :
            y_unit = str(sys.argv[i+1])
        elif sys.argv[i] == '--debug' or sys.argv[i] == '-d' :
            debug = True
        else:
            continue
try: simCase
except NameError: simCase = None
if simCase is None :
    simCase = 'fake'
try: simBranch
except NameError: simBranch = None
if simBranch is None :
    simBranch = 'fake'
try: x_unit
except NameError: x_unit = None
if x_unit is None :
    x_unit = 'M'
try: y_unit
except NameError: y_unit = None
if y_unit is None :
    y_unit = 'PA'
# program execution
if len(sys.argv) > 1 :
    sps_sim_data=sys.argv[1]
else :
    sps_sim_data=input('Please enter a path and filename for SPS simulation data to be converted to OLGA .ppl: ')
    if len(sps_sim_data) < 1 :
        use_default_data=input('No SPS simulation data was selected, would you like to use default demo data? [y/n]: ')
        if use_default_data[0] == 'y' :
            sps_sim_data='./data/P_liq.txt'
        else :
            print('Bye for now, please come back later')
            exit
with open(sps_sim_data) as f:
    lines = f.readlines()
    i = 0
    for line in lines :
        line = line.strip()
        if line.find(strKeep) > 0 :
            datamap.append(i)
        i = i + 1
    global j
    j = 0
    for nkeep in datamap :
        jj = 0
        while not lines[nkeep - jj][0] == '[' :
            jj = jj + 1
        rawdata.append(lines[nkeep - jj:nkeep + 1])   # a list of strings containing data from first line to last line for the time step
        rawdata[j] = ''.join(rawdata[j])              # join list elements to one list
        for d in rawdata[j] :                         #get variable data, e.g. Pressure
            if d == ',' :
                getValue = True
                getGeometry = False
            if d == ')' :
                getValue = False
            if d == '(' :
                getValue = False
                getGeometry = True
            if getValue == True :
                 var = var + d
            if getGeometry == True :
                geom = geom + d
        data.append(var)                              #join profile data points into one line
        geometry.append(geom)
        #data[j] = ''.join(c for c in data[j] if not c in dumpChars)
        data[j] = data[j][2:len(data[j])-1].replace(' ', '').split(',')
        geometry[j] = geometry[j][2:len(geometry[j])-1].replace(' ', '').split('(')
        if mostSections < len(geometry[j]) :          #find the index of the timestep with the most sections
            geomIndex = j
            mostSections = len(geometry[j])
        j = j + 1
        var = ''
        geom = ''
    x_positons = getProfileSections(geometry[geomIndex])
    y_positons = getProfileSections(['0.'] * mostSections)
    #y_positons = getProfileSections(['0.'] + ['10.'] * 17 + ['0.'] * 2) # Test case for 2x90degL geometry
alignProfileData(data)
writeOlgaProfile()
if debug == True :
    writeDebugFile()