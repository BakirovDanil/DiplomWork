def dictionary_output(dictionaries: dict):
    """
    Функция для красивого вывода многоуровневых словарей
    :param dictionaries:
    :return:
    """
    for key, value in dictionaries.items():
        if type(value) is not dict:
            print(key, value)
        else:
            print(key)
            for x, y in dictionaries[key].items():
                if type(y) is not dict:
                    print(f"\t{x}: {y}")
                else:
                    print(x)
                    for k,l in dictionaries[key][x].items():
                        print(f"\t{k}: {l}")