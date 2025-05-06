def dictionary_output(dictionaries: dict):
    for key, value in dictionaries.items():
        if type(value) is not dict:
            print(key, value)
        else:
            print(key)
            for x, y in dictionaries[key].items():
                print(f"\t{x}: {y}")