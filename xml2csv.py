import os
from csv import DictWriter, QUOTE_ALL
from lxml import etree


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
    for event, elem in context:
        attribute = elem.attrib
        chunked_rows.append(attribute)
        if len(chunked_rows) == chunk_size:
            with open(f'{filename_csv}.csv', 'a', newline='') as f_object:
                dictwriter_object = DictWriter(f_object,
                                               fieldnames=list(dict(chunked_rows[0])),
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
                f_object.close()
            chunked_rows = []
            elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]


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
    while True:
        a = list(input('1 параметр - размер чанка (число должно делиться на количество строк)\n'
                       '2 параметр - сепаратор в csv (по умол. ";")\n'
                       '3 параметр - символ цитаты в csv (по умол. "#")\n'
                       '4 параметр - относительный путь к директории с .xml файлами (по умол. текущая)\n').split())
        if len(a) == 1:
            chunk_size = int(a[0])
            for file in find_all_xmls():
                print(f'Работа с файлом "{file}"')
                convert_xml2csv(file_xml=file, chunk_size=chunk_size)
        elif len(a) == 2:
            chunk_size = int(a[0])
            csv_sep = a[1]
            for file in find_all_xmls():
                print(f'Работа с файлом "{file}"')
                convert_xml2csv(file_xml=file, chunk_size=chunk_size, csv_sep=csv_sep)
        elif len(a) == 3:
            chunk_size = int(a[0])
            csv_sep = a[1]
            quotechar = a[2]
            for file in find_all_xmls():
                print(f'Работа с файлом "{file}"')
                convert_xml2csv(file_xml=file, chunk_size=chunk_size, csv_sep=csv_sep, quotechar=quotechar)
        elif len(a) == 4:
            chunk_size = int(a[0])
            csv_sep = a[1]
            quotechar = a[2]
            file_path = a[3]
            find = find_all_xmls(file_path)
            if find:
                for file in find:
                    print(f'Работа с файлом "{file}"')
                    convert_xml2csv(file_xml=f'{os.path.abspath(os.getcwd())}{file_path}\{file}', chunk_size=chunk_size, csv_sep=csv_sep, quotechar=quotechar)
        else:
            print('Incorrect arguments')

        print('Процесс завершен')
