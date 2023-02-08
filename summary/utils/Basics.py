import pickle

def read_pickle(path):
    with open(path, 'rb') as f:
        output = pickle.load(f)
    return output


def write_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)