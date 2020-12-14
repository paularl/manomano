# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class ManomanoPipeline:
#     def process_item(self, item, spider):
#         return item

from scrapy.exporters import CsvItemExporter
from scrapy import signals
from pydispatch import dispatcher

# items.py

from scrapy.exporters import CsvItemExporter


class SeminarPipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        self.files = {}

    def close_spider(self, spider):
        for exporter in self.files.values():
            exporter.finish_exporting()

    def file_name(self, item):

        title = item["categoria"]

        if title == "cuadros":
            exporter = CsvItemExporter(open('cuadros.csv', 'ab'), include_headers_line=False, encoding='latin-1',
                                       delimiter=';')
            exporter.start_exporting()
            self.files['cuadros'] = exporter
            return self.files['cuadros']

        elif title == 'diferenciales':
            exporter = CsvItemExporter(open('diferenciales.csv', 'ab'), include_headers_line=False, encoding='latin-1', delimiter=';')
            exporter.start_exporting()
            self.files['diferenciales'] = exporter
            return self.files['diferenciales']

        elif title == 'disjuntores_modulares':
            exporter = CsvItemExporter(open('disjuntores_modulares.csv', 'ab'), include_headers_line=False, encoding='latin-1', delimiter=';')
            exporter.start_exporting()
            self.files['disjuntores_modulares'] = exporter
            return self.files['disjuntores_modulares']

    def process_item(self, item, spider):
        exporter = self.file_name(item)
        exporter.export_item(item)
        return item
