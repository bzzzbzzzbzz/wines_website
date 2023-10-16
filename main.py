import datetime, pandas, argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

def get_year_word(year):
    if year % 10 == 1 and year % 100 != 11:
        return 'год'
    elif 2 <= year % 10 <= 4 and (year % 100 < 10 or year % 100 >= 20):
        return 'года'
    else:
        return 'лет'


if __name__ == '__main__':
    parsed_xlsx = argparse.ArgumentParser()
    parsed_xlsx.add_argument('xlsx', help='enter your xlsx')
    args = parsed_xlsx.parse_args()
    excel_data = pandas.read_excel(args.xlsx, na_filter=False)

    categories = defaultdict(list)
    for record in excel_data.to_dict(orient="records"):
        categories[record['Категория']].append(record)

    difference = datetime.datetime.today() - datetime.datetime(year=1920, month=1, day=1)
    product_year = difference.days // 365
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        product_year=product_year,
        correct_year=get_year_word(product_year),
        categories=categories
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()