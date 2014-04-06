def filter_empty_values(dict_to_clean):
    return dict((key, values) for key, values in dict_to_clean.items() if values)