import os
import pandas as pd

from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


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

def main():
    load_dotenv()

    file_path = os.getenv('FILEPATH', default='.')
    file_name = os.getenv('FILENAME', default='wine.xlsx')
    full_path = os.path.join(file_path, file_name)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')

    year_now = datetime.now().year
    year_of_company = 1920
    age_of_company = year_now - year_of_company

    wines_df = pd.read_excel(full_path, keep_default_na=False)
    wines_categories = wines_df['Категория'].tolist()
    wines = wines_df.to_dict('records')

    wines_by_category = defaultdict(list)
    for wine_number, category in enumerate(wines_categories):
        wines_by_category[category].append(wines[wine_number])

    rendered_page = template.render(
        wines_by_category = wines_by_category,
        year = age_of_company,
        year_word = year_comment_word(age_of_company)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
