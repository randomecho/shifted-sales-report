import csv
import operator
import os
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_file",
    default='/tmp/activity.csv',
    help="CSV input file with transactions (default: %(default)s)")
parser.add_argument("-o", "--output", dest="output_file",
    default='/tmp/sales_order_columns_extracted.csv',
    help="Output location of reformatted CSV (default: %(default)s)")
parser.add_argument("-d", "--delimit", dest="delimiter",
    default="\t",
    help="Delimiter character (default: %(default)s)")
args = parser.parse_args()

wanted_columns = []


def extract_columns(row):
    if len(row) < 26 or not row[23] or not str.isdigit(row[26]):
        return False

    columns = {
        'item': row[23],
        'cost': 0,
        'returns': 0,
        'ask': row[27],
        'sold': int(row[26]) * float(row[27].replace('$', '')),
        'tax': row[38],
        'shipping': row[28],
        'free_ship': '',
        'fvf':  '',
        'promo': '',
        'inter': '',
        'profit': '',
        'source': '',
        'buy_date': '',
        'list_date': '',
        'sold_date': row[53],
        'ship_date': row[57],
        'arrive_date': row[63],
        'weight': '?',
        'ship_state': row[19],
        'notes': row[2] +' '+ row[3] +' '+ row[24] +' '+ row[60],
    }

    if row[81] == 'Yes':
        columns['ship_state'] = row[78]+' '+row[80]

    return columns


try:
    with open(args.input_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            extracted_columns = extract_columns(row)

            if extracted_columns:
                wanted_columns.append(extracted_columns)

except FileNotFoundError:
    print("Cannot open transactions file: " + args.input_file)


if wanted_columns:
    wanted_columns.sort(key=operator.itemgetter("sold_date"))
    sales_order = ''

    if Path(args.output_file).is_file():
        os.remove(args.output_file)

    with open(args.output_file, "w") as output_file_location:
        csv_out = csv.writer(output_file_location)

        for sales_data in wanted_columns:
            sales_order += sales_data['item']+args.delimiter\
                +str(sales_data['cost'])+args.delimiter\
                +str(sales_data['returns'])+args.delimiter\
                +sales_data['ask']+args.delimiter\
                +str(sales_data['sold'])+args.delimiter\
                +str(sales_data['tax'])+args.delimiter\
                +str(sales_data['shipping'])+args.delimiter\
                +sales_data['free_ship']+args.delimiter\
                +sales_data['fvf']+args.delimiter\
                +sales_data['promo']+args.delimiter\
                +sales_data['inter']+args.delimiter\
                +sales_data['profit']+args.delimiter\
                +sales_data['source']+args.delimiter\
                +sales_data['buy_date']+args.delimiter\
                +sales_data['list_date']+args.delimiter\
                +sales_data['sold_date']+args.delimiter\
                +sales_data['ship_date']+args.delimiter\
                +sales_data['arrive_date']+args.delimiter\
                +sales_data['weight']+args.delimiter\
                +sales_data['ship_state']+args.delimiter\
                +sales_data['notes']+args.delimiter\
                +'e'\
                +"\n"

        output_file_location.write(sales_order)

    if Path(args.output_file).is_file():
        print("CSV transformed into file: {}".format(args.output_file))
    else:
        print("No output file generated")
