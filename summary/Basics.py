import pickle
import networkx as nx


def read_pickle(path):
    with open(path, 'rb') as f:
        output = pickle.load(f)
    return output

def write_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

class GraphParser:
    def __init__(self):
        pass
    
    def split_disasm(self, disasm):
        """For x86 Only"""
        _asm = disasm.split(', ')
        _opc = _asm[0].split(' ', 1)
        _ret = _opc + [_asm[1]] if len(_asm)==2 else _opc
        return _ret

    def get_opcode_blocks(self, fpath, concat=None, return_graph=False):
        G = read_pickle(fpath)

        blocks = []
        for opcodes in nx.get_node_attributes(G, 'x').values():
            asm = [self.split_disasm(disasm)[0] for _, disasm in opcodes]
            if concat is not None:
                asm = concat.join(asm)
            blocks.append(asm)

        if return_graph:
            return blocks, G
        else:
            return blocks

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