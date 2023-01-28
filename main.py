import pandas as pd

from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

def year_comment_word(year):
    num = year % 100
    if 4 < num < 21:
        return 'лет'

    num = num % 10
    if num == 1:
        return 'год'
    elif 1 < num < 5:
        return 'года'
    return 'лет'

year_now = datetime.now().year
year_of_company = datetime(year=1920, month=1, day=1).year
age_of_company = year_now - year_of_company

wines_df = pd.read_excel('wine.xlsx', keep_default_na=False)
wines_categories = wines_df['Категория'].tolist()
dct_wines_df = wines_df.to_dict('records')

wines_data = defaultdict(list)
for i in range(len(wines_categories)):
    wines_data[wines_categories[i]].append(dct_wines_df[i])

rendered_page = template.render(
    wines_data = wines_data,
    year = age_of_company,
    year_word = year_comment_word(age_of_company)
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
