import pandas as pd
import csv


data = pd.read_csv(input("Wprowadź nazwę pliku w formacie .csv, który zawiera dane z pomiaru batymetrycznego: \n"))
print(data.head())
depth = data['Depth'].to_list()
time = data['TimeOffset[ms]'].to_list()

datagps = pd.read_csv(input("Wprowadź nazwę pliku w formacie .csv, który zawiera dane z pomiaru GPS: \n"))
print(datagps.head())
X = datagps['X'].to_list()
Y = datagps['Y'].to_list()
H = datagps['H'].to_list()
czas = datagps['czas'].to_list()
tryb = datagps['tryb'].to_list()

XY_GPS = []
N_GPS = 0
for i in X:
    XY_GPS.append([i, Y[N_GPS]])
    N_GPS = N_GPS + 1

dlugosc_tyczki = float(input("Wprowadź długość tyczki anteny GPS w metrach: \n"))
undulacja = 39.934

d = []
for i in depth:
    d.append(i*0.3048)


podany_czas = int(input("Wprowadź numer soundingu o znanej godzinie: \n"))
godzina = str(input("Wprowadź godzinę pomiaru (gg:mm:ss): \n"))
g = 10*float(godzina[0]) + float(godzina[1])
m = 10*float(godzina[3]) + float(godzina[4])
s = 10*float(godzina[6]) + float(godzina[7])
cz = (g*3600)+(m*60)+s

time0 = []
for i in time:
    time0.append(i/1000)

czas_wprowadzony = time0[podany_czas - 1]
czas_poczatku_pomiaru = cz - czas_wprowadzony

sdeptx = []
for i in time0:
    sdeptx.append(czas_poczatku_pomiaru + i)

gl_czdict = {}
n=0
for i in sdeptx:
    gl_czdict[i] = d[n]
    n = n + 1

S_GPS = []
for i in czas:
    g0 = float(i[11])
    g1 = float(i[12])
    m3 = float(i[14])
    m4 = float(i[15])
    s6 = float(i[17])
    s7 = float(i[18])
    S_GPS.append(((10*g0+g1)*3600)+((10*m3+m4)*60)+(10*s6+s7))

tryb_dict = {}
t = 0
for i in S_GPS:
    tryb_dict[i] = tryb[t]
    t = t + 1


ns = 0
XY_czdict = {}
for i in S_GPS:
    XY_czdict[i] = XY_GPS[ns]
    ns = ns + 1

NSH = 0
H_czdict = {}
for i in S_GPS:
    H_czdict[i] = H[NSH]
    NSH = NSH + 1

S_DEPT = []
for i in sdeptx:
    if i >= min(S_GPS) and i <= max(S_GPS) + 1:
        S_DEPT.append(i)

SGP = []
for i in S_GPS:
    if i >= min(sdeptx) and i <= max(sdeptx):
        SGP.append(i)

TIME_DICT = {}
GPS_ID = 1
for gle in S_DEPT:
    key = None
    if GPS_ID >= len(SGP) or gle <= SGP[GPS_ID]:
        key = SGP[GPS_ID - 1]
    else:
        key = SGP[GPS_ID]
        GPS_ID = GPS_ID + 1

    if not key in TIME_DICT:
        TIME_DICT[key] = []
    TIME_DICT[key].append(gle)

lista_b = []
for i in TIME_DICT:
    lista_b.append(TIME_DICT[i])

S_DEPT_0 = []
for linia in lista_b:
    S_DEPT_0.append(min(linia))

tyczka_undulacja = []
for i in S_DEPT_0:
    tyczka_undulacja.append(gl_czdict[i] + dlugosc_tyczki + undulacja)

DT = 0
glebokosci_bezwgledne = []
for i in SGP:
    glebokosci_bezwgledne.append(H_czdict[i] - tyczka_undulacja[DT])
    DT = DT + 1

WYNIK = []
IDW = 0
for i in SGP:
    if tryb_dict[i] == "Pomierzony" or tryb_dict[i] == "Measured":
        WYNIK.append([XY_czdict[i], glebokosci_bezwgledne[IDW]])
        IDW = IDW + 1

with open(input("Podaj nazwe pliku .csv, do ktorego zapisac wynik: \n"), 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for i in WYNIK:
        csvwriter.writerow(i)

with open('Wszystkie.csv', 'a', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for i in WYNIK:
        csvwriter.writerow(i)

print (f'zestawienie: {WYNIK}')
print (f'Głebokości bezwzględne wynoszą: {glebokosci_bezwgledne}')