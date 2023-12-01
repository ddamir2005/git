import csv


def read_csv(periodictable):
    data = []
    with open('periodictable.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


def get_element_info(data, element_number):
    element_data = {}
    for i, row in enumerate(data[int(element_number) - 1]):
        key = ''
        if i == 0:
            key = 'Atomic Number'
        elif i == 1:
            key = 'Symbol'
        elif i == 2:
            key = 'Element'
        elif i == 3:
            key = 'Origin of name'
        elif i == 4:
            key = 'Group'
        elif i == 5:
            key = 'Period'
        elif i == 6:
            key = 'Atomic weight'
        elif i == 7:
            key = 'Density'
        elif i == 8:
            key = 'Melting point'
        elif i == 9:
            key = 'Boiling point'
        elif i == 10:
            key = 'Specific heat capacity'
        elif i == 11:
            key = 'Electronegativity'
        elif i == 12:
            key = 'Abundance in earth\'s crust'
        element_data[key] = row
    return element_data


filename = 'periodictable.csv'  # имя вашего CSV-файла
data = read_csv(filename)
print('                            Pereodic Table of Elements')
print(' ', ' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ', ' 10 ', ' 11 ', ' 12 ', ' 13 ', ' 14 ',
      ' 15 ', ' 16 ', ' 17 ', ' 18 ')
print('1', ' H')
print('2', ' Li', ' Be', '                                           ', 'B', '   C', '   N', '   O', '   F', '   Ne')
print('3', ' Na', ' Mg', '                                           ', 'Ai', '  Si ', ' P', '   S', '   C1', '  Ar')
print('4', ' K', '  Ca', ' Sc', ' Ti', ' V', '  Cr', ' Mn', ' Fe', ' Co', ' Ni', '  Cu', '  Zn', '  Ga', '  Ge', '  As',
      '  Se', '  Br', '  Kr')
print('5', ' Rb', ' Sr', ' Y', '  Zr', ' Nb', ' Mo', ' Tc', ' Ru', ' Rh', ' Pd', '  Ag', '  Cd', '  In', '  Sn', '  Sb',
      '  Te', '  I', '   Xe')
print('6', ' Cs', ' Ba', ' La', ' Hf', ' Ta', ' W', '  Re', ' Os', ' Ir', ' Pt', '  Au', '  Hg', '  T1', '  Pb', '  Bi',
      '  Po', '  At', '  Rn')
print('7', ' Fr', ' Ra', ' Ac', ' Rf', ' Db', ' Sg', ' Bh', ' Hs', ' Mt', ' Ds', '  Rg', '  Cn', '  Nh', '  F1', '  Mc',
      '  Lv', '  Ts', '  Og')
while True:
    element_number = str(input('Enter a symbol or atomic number to examine or Quit to quit: '))
    if element_number == 'Quit':
        break
    if not element_number.isdigit():
        print("Not correct")
    if element_number.isdigit() and (1 < int(element_number) < 118):
        element_info = get_element_info(data, element_number)

        for key, value in element_info.items():
            print(f'{key}: {value}')







