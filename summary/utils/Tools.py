def compute_frequency(obj):
    return_dict = dict()
    for item in obj:
        if item in return_dict:
            return_dict[item] += 1
        else:
            return_dict[item] = 1
    return return_dict
    
    
def merge_dict(dict1, dict2):
    for key, val in dict2.items():
        if key in dict1:
            dict1[key] += val
        else:
            dict1[key] = val
    return dict1
    
    
def ngram_iterator(token_list, concat=None, ngram=2):
    """if concat is None, return the original list"""
    if concat is None:
        grams = [token_list[i:i+ngram] for i in range(len(token_list) - ngram + 1)]
    else:
        grams = [concat.join(token_list[i:i+ngram]) for i in range(len(token_list) - ngram + 1)]
    return grams


def sort_dict(obj, by_value=False, reverse=False):
    """default to sort by keys"""
    if by_value:
        return dict(sorted(obj.items(), reverse=reverse, key=lambda i: i[1]))
    else:
        return dict(sorted(obj.items(), reverse=reverse))