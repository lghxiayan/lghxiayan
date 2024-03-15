import csv


def reader():
    with open('test.csv', mode='rt', encoding='utf-8') as f_in:
        reader = csv.reader(f_in, delimiter=',')
        print(reader)  # <_csv.reader object at 0x000001F4D63C6040>

        # print(reader.__next__())
        print(reader.dialect)
        print(reader.line_num)

        # header[0] = 'name'
        # header[1] = 'sex'
        # header[2] = 'age'
        # header[3] = 'score'
        header = next(reader)

        print(header)  # ['name', 'sex', 'age', 'score']

        for line in reader:
            print(type(line), line)  # <class 'list'> ['agua', 'm', '20', '80']


def dict_reader():
    with open('test.csv', 'rt', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)

        print(reader)  # <csv.DictReader object at 0x00000296B2013EE0>
        for line in reader:
            print(type(line), line)  # <class 'dict'> {'name': 'agua', 'sex': 'm', 'age': '20', 'score': '80'}


def writer():
    # 创建列表，保存header内容
    header_list = ['name', 'sex', 'age', 'score']
    data_list = [
        ['agua', 'm', '20', '80'],
        ['ahua', 'fm', '19', '90'],
        ['adai', 'm', '21', '95']
    ]

    with open('new_data.csv', 'w', encoding='utf-8', newline='') as f_out:
        new_writer = csv.writer(f_out)
        new_writer.writerow(header_list)
        new_writer.writerows(data_list)


def dict_writer():
    header_list = ['name', 'sex', 'age', 'score']
    data_list = [
        {"name": "a", "sex": "m", "age": 20, "score": 80},
        {"name": "bb", "sex": "fm", "age": 19, "score": 90},
        {"name": "ccc", "sex": "fm", "age": 21, "score": 95}
    ]

    with open('dict_new_data.csv', 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, header_list)
        writer.writeheader()
        writer.writerows(data_list)


# reader()
# dict_reader()

writer()
# dict_writer()
