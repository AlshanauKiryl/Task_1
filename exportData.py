import json
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import date, datetime
import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")


def dump_data(data, format: str, filename: str):
    '''Вызывает определенную функцию сохранения в файл для разных форматов данных'''
    serializers = {
        "json": dump_json,
        "xml": dump_xml
    }

    if format not in serializers:
        raise ValueError(f"Unsupported format: {format}")

    serializers[format](data, filename)


def dump_json(data, filename: str):
    '''Сохраняет переданные данные в json файл с переданным названием'''
    with open(f"{filename}.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=serialize_data)
    logging.info(f'Query result saved in {filename}.json')


def dump_xml(data, filename: str):
    '''Сохраняет переданные данные в xml файл с переданным названием'''
    root = ET.Element("result")

    def create_item_element(parent, item):
        item_el = ET.SubElement(parent, "item")
        if isinstance(item, dict):
            for k, v in item.items():
                ET.SubElement(item_el, k).text = str(v)
        else:
            ET.SubElement(item_el, "value").text = str(item)

    if isinstance(data, dict):
        for key, items in data.items():
            section = ET.SubElement(root, key)
            for item in items:
                create_item_element(section, item)
    elif isinstance(data, list):
        section = ET.SubElement(root, "items")
        for item in data:
            create_item_element(section, item)
    else:
        raise TypeError("Data must be a dict or list")

    tree = ET.ElementTree(root)
    tree.write(f"{filename}.xml", encoding="utf-8", xml_declaration=True)
    logging.info(f'Query result saved in {filename}.xml')


def serialize_data(obj):
    '''адаптирует данные для сохранения их в json файл'''
    if isinstance(obj, (Decimal, date, datetime)):
        return str(obj)