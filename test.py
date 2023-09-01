import pandas, pprint

excel_data = pandas.read_excel('wine2.xlsx', na_values='', keep_default_na=False)
datadict = excel_data.to_dict()
data_dict = datadict

white_wine = []
red_wine = []
drinks = []


types = []
for key in data_dict:
    types.append(key)

i = 0
for key2 in data_dict[types[i]]:
    new_dict = {}
    for key in data_dict:
        new_dict[key] = data_dict[key][key2]
    if new_dict[types[0]] == data_dict[types[0]][0]:
        white_wine.append(new_dict)
    elif new_dict[types[0]] == data_dict[types[0]][3]:
        red_wine.append(new_dict)
    else:
        drinks.append(new_dict)

final_dictionary = {}
final_dictionary.update({datadict[types[0]][0]:white_wine})
final_dictionary.update({data_dict[types[0]][3]:red_wine})
final_dictionary.update({data_dict[types[0]][1]:drinks})

pprint.pprint(final_dictionary)
