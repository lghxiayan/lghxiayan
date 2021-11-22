import yaml

with open('items.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data['raincoat'])
    #
    # sorted = yaml.dump(data, sort_keys=True)
    # print(sorted)

    # for token in data:
    #     print(token)
