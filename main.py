import datetime, pandas, collections, argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape




parsed_xlsx = argparse.ArgumentParser()
parsed_xlsx.add_argument('xlsx', help='enter your xlsx')
args = parsed_xlsx.parse_args()

excel_data = pandas.read_excel(args.xlsx, na_filter=False)


wines_data = excel_data.to_dict()

white_wines = []
red_wines = []
drinks = []

types = []
for key in wines_data:
    types.append(key)

i = 0
for inside_key in wines_data[types[i]]:
    new_dict = {}
    for key in wines_data:
        new_dict[key] = wines_data[key][inside_key]
    if new_dict[types[0]] == wines_data[types[0]][0]:
        white_wines.append(new_dict)
    elif new_dict[types[0]] == wines_data[types[0]][3]:
        red_wines.append(new_dict)
    else:
        drinks.append(new_dict)

final_dictionary = {}
final_dictionary.update({wines_data[types[0]][0]: white_wines})
final_dictionary.update({wines_data[types[0]][3]: red_wines})
final_dictionary.update({wines_data[types[0]][1]: drinks})

alcohols = collections.defaultdict(str, final_dictionary)

difference = datetime.datetime.today() - datetime.datetime(year=1920, month=1, day=1)
product_year = difference.days // 365

def is_year(year):
    year = str(year)
    if year[-1] in '0':
        return 'лет'
    elif year[-1] in '1':
        return 'год'
    elif year[-1] in '234':
        return 'года'
    else:
        return 'лет'


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        product_year=product_year,
        correct_year=is_year(product_year),
        alcohols=alcohols,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
