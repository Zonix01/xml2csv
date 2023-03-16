import os
from csv import DictWriter, QUOTE_ALL
from lxml import etree
import sys


def convert_xml2csv(file_xml, csv_sep=';', quotechar='#', chunk_size=100):
    try:
        context = etree.iterparse(file_xml)
    except:
        print('Файлы не найдены')
        return
    filename_csv = file_xml.rstrip('.XML')
    chunked_rows = []
    header_created = False
    chunk_iterator = 0
    temp_set = set()
    amount = 0
    for event, elem in context:
        attribute = elem.attrib
        amount += 1
        for i in range(len(attribute)):
            temp_set.add(list(dict(elem.attrib).keys())[i])
        chunked_rows.append(attribute)
        if len(chunked_rows) == chunk_size:
            with open(f'{filename_csv}.csv', 'a', newline='') as f_object:
                dictwriter_object = DictWriter(f_object,
                                               fieldnames=list(temp_set),
                                               delimiter=csv_sep,
                                               quotechar=quotechar,
                                               quoting=QUOTE_ALL)
                if not header_created:
                    dictwriter_object.writeheader()
                    header_created = True
                for row in chunked_rows:
                    dictwriter_object.writerow(dict(row))
                chunk_iterator += 1
                print(f'Теущий чанк: {chunk_iterator}')
            chunked_rows = []
            elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    with open(f'{filename_csv}.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object,
                                       fieldnames=list(temp_set),
                                       delimiter=csv_sep,
                                       quotechar=quotechar,
                                       quoting=QUOTE_ALL)
        if not header_created:
            dictwriter_object.writeheader()
        for row in chunked_rows:
            dictwriter_object.writerow(dict(row))
        chunk_iterator += 1
        print(f'Теущий чанк: {chunk_iterator}')


def find_all_xmls(path=os.curdir):
    fileExt = r".XML"
    if path != os.curdir:
        path = os.curdir + path
    try:
        found = [_ for _ in os.listdir(path) if _.endswith(fileExt)]
    except FileNotFoundError:
        print(f"Директория {path} не найдена. Доступные директории: {os.listdir(os.curdir)}")
        return
    print(f'По пути: "{path}" найдены файлы: {found}')
    if found != []:
        return [_ for _ in os.listdir(path) if _.endswith(fileExt)]
    else:
        return


if __name__ == '__main__':
   # convert_xml2csv('AS_ADM_HIERARCHY_20230126_2e058bc4_5d72_4f73_804c_2d63371ed4e3.XML')
    while True:
        a = sys.argv
        print(a)
        if len(a) == 2:
            chunk_size = int(a[1])
            print(type(chunk_size))
            for file in find_all_xmls():
                print(f'Работа с файлом "{file}"')
                convert_xml2csv(file_xml=file, chunk_size=chunk_size)
                print('TEST')
        elif len(a) == 3:
            chunk_size =  int(a[1])
            csv_sep = a[2]
            for file in find_all_xmls():
                print(f'Работа с файлом "{file}"')
                convert_xml2csv(file_xml=file, chunk_size=chunk_size, csv_sep=csv_sep)
        elif len(a) == 4:
            chunk_size =  int(a[1])
            csv_sep = a[2]
            quotechar = a[3]
            for file in find_all_xmls():
                print(f'Работа с файлом "{file}"')
                convert_xml2csv(file_xml=file, chunk_size=chunk_size, csv_sep=csv_sep, quotechar=quotechar)
        elif len(a) == 5:
            chunk_size =  int(a[1])
            csv_sep = a[2]
            quotechar = a[3]
            file_path = a[4]
            find = find_all_xmls(file_path)
            if find:
                for file in find:
                    print(f'Работа с файлом "{file}"')
                    convert_xml2csv(file_xml=f'{os.path.abspath(os.getcwd())}{file_path}\{file}', chunk_size=chunk_size, csv_sep=csv_sep, quotechar=quotechar)
        else:
            print('Incorrect arguments')

        print('Процесс завершен')
        break
