import csv
import os
import sys


def check_arg():
    conc = sys.argv[1:]
    if len(conc) == 0:
        print(
            'GndHCl calculation script. Use it like this: \n\ncalculate_gua.py -z 1.3333 -g 1.46\n\n-z zero gnd refracting index\n-g measured gnd refracting index\n-f use single column csv file with refracting indexes')
        exit(0)
    zero = 1.3333
    if '-z' in conc:
        z = conc.index('-z')
        try:
            zero = conc[z + 1]
        except IndexError:
            print('\nUsing ddH2O refracting index for 0M [GndHCl]: 1.3333, if different use -z "RefIndex"')
    elif '-z' not in conc:
        print('\nUsing ddH2O refracting index for 0M [GndHCl]: 1.3333, if different use -z "RefIndex"')
    if '-g' in conc:
        g = conc.index('-g')
        try:
            gnd = conc[g + 1]
            is_file = False
        except IndexError:
            print('argument missing!')
            exit(0)
        return is_file, gnd, zero
    if '-f' in conc:
        f = conc.index('-f')
        try:
            file = conc[f + 1]
            print('Using csv file, ', file)
            is_file = True
        except IndexError:
            print('argument missing!')
            exit(0)
        return is_file, file, zero


def calc_conc(zero, ref_index):
    diff = float(ref_index) - float(zero)
    conc = (57.147 * (diff) + 38.68 * (diff) ** 2 - 91.6 * (diff) ** 3)
    return round(conc, 4)


def check_file(file, zero):
    with open(file, 'r') as fh:
        if os.path.isfile(str(file).replace('.csv', '-calculated.csv')):
            os.remove(str(file).replace('.csv', '-calculated.csv'))
        with open(str(file).replace('.csv', '-calculated.csv'), 'a', newline='') as fr:
            reader = csv.reader(fh)
            writer = csv.writer(fr)
            writer.writerow(['Refracting index', 'Calculated [GndHCl]'])
            writer.writerow([zero, 0])
            for row in reader:
                row.append(calc_conc(zero, float(row[0])))
                writer.writerow(row)


def file_not_present(is_file, gnd, zero):
    if is_file:
        print('\nWriting the file with result...')
        check_file(gnd, zero)
    if not is_file:
        print('\nMeasured [GndHCl] is:  ', calc_conc(zero, gnd),'\n')


is_file, gnd, zero = check_arg()
file_not_present(is_file, gnd, zero)
