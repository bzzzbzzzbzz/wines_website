import datetime, pandas, pprint, collections
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def grammar_func(year):
    danger_years = [111, 112, 113, 114]
    if year in danger_years:
        return 'лет'
    elif year % 10 == 0:
        return 'лет'
    elif year % 10 == 1:
        return 'год'
    elif year % 10 >= 5:
        return 'лет'
    else:
        return 'года'


excel_data = pandas.read_excel('wine3.xlsx',
                               na_filter=False
                               )
data_dict = excel_data.to_dict()

white_wine = []
red_wine = []
drinks = []

types = []
for key in data_dict:
    types.append(key)

i = 0
for inside_key in data_dict[types[i]]:
    new_dict = {}
    for key in data_dict:
        if not data_dict[key][inside_key]:
            data_dict[key][inside_key] = ''
        new_dict[key] = data_dict[key][inside_key]
    if new_dict[types[0]] == data_dict[types[0]][0]:
        white_wine.append(new_dict)
    elif new_dict[types[0]] == data_dict[types[0]][3]:
        red_wine.append(new_dict)
    else:
        drinks.append(new_dict)

final_dictionary = {}
final_dictionary.update({data_dict[types[0]][0]: white_wine})
final_dictionary.update({data_dict[types[0]][3]: red_wine})
final_dictionary.update({data_dict[types[0]][1]: drinks})

alcohol = collections.defaultdict(str, final_dictionary)




env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

difference = datetime.datetime.today() - datetime.datetime(year=1920, month=1, day=1)
year_var = difference.days // 365

rendered_page = template.render(
    product_year=year_var,
    correct_year=grammar_func(year_var),
    alcohol=alcohol,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
