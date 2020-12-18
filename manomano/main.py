from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('manomano')
process.start() # the script will block here until the crawling is finished

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/paula.romero.lopes/Projects/credencials/manomano-8f87406ceb33.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('manomano')
worksheet = spreadsheet.get_worksheet(0)

file_list = ["cuadros.csv", "diferenciales.csv", "disjuntores_modulares.csv"]

df = pandas.read_csv(file_list[0], delimiter=";", decimal=".", encoding="latin-1")
df = df.append(pandas.read_csv(file_list[1], delimiter=";", decimal=".", encoding="latin-1"))
df = df.append(pandas.read_csv(file_list[2], delimiter=";", decimal=".", encoding="latin-1"))
df.precio = df.precio.astype(float)
df = df.drop_duplicates()

worksheet.update([df.columns.values.tolist()] + df.fillna(' ').values.tolist())

