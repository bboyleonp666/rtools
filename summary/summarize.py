import os
import argparse
import networkx as nx

from utils.Basics import *
from utils.Tools import *


class GraphParser:
    def __init__(self):
        pass
    
    
    def split_disasm(self, disasm):
        """For x86 Only"""
        _asm = disasm.split(', ')
        _opc = _asm[0].split(' ', 1)
        _ret = _opc + [_asm[1]] if len(_asm)==2 else _opc
        return _ret
    

    def get_opcode_blocks(self, fpath, concat=None):
        G = read_pickle(fpath)

        blocks = []
        for opcodes in nx.get_node_attributes(G, 'x').values():
            asm = [self.split_disasm(disasm)[0] for _, disasm in opcodes]
            if concat is not None:
                asm = concat.join(asm)
            blocks.append(asm)
        return blocks


def summarize(path):
    # file name
    name = os.path.splitext(os.path.basename(path))[0]
    
    # opcode block list
    parser = GraphParser()
    opc_blocks = parser.get_opcode_blocks(path)

    # number of nodes
    num_nodes = len(opc_blocks)

    # block lengths dictionary
    block_lengths_list = [len(opcs) for opcs in opc_blocks]
    block_lengths = compute_frequency(block_lengths_list)

    # ngram info
    unigram = dict()
    bigram  = dict()
    trigram = dict()
    for opcs in opc_blocks:
        # uni-gram counts
        _uni = ngram_iterator(opcs, concat='-', ngram=1)
        unigram = merge_dict(unigram, compute_frequency(obj=_uni))

        # bi-gram counts
        _bi  = ngram_iterator(opcs, concat='-', ngram=2)
        bigram = merge_dict(bigram, compute_frequency(obj=_bi))

        # tri-gram counts
        _tri = ngram_iterator(opcs, concat='-', ngram=3)
        trigram = merge_dict(trigram, compute_frequency(obj=_tri))

    summary = {'name': name, 
               'num_nodes': num_nodes, 
               'block_lengths': block_lengths, 
               'unigram': unigram, 
               'bigram': bigram, 
               'trigram': trigram}
    
    return summary


def generate_sequences(path, ngram=10):
    parser = GraphParser()
    opc_blocks = parser.get_opcode_blocks(path)

    sequences = []
    for blk in opc_blocks:
        if len(blk) == 1:
            continue
            
        elif len(blk) > ngram:
            ngram_seq = ngram_iterator(blk, ngram=ngram)
            for _ngram_seq in list(zip(ngram_seq[:-1], ngram_seq[1:])):
                sequences.append(_ngram_seq)
                
        else:
            sequences.append((blk[:-1], blk[1:]))
    
    return sequences


def parse_args():
    parser = argparse.ArgumentParser(description='Opcode Block Summarizing Script')
    parser.add_argument('--method', type=str, required=True, metavar='[summary | sequences | opcode_blocks]',
                        help='information to obtain')
    parser.add_argument('-f', '--file-path', type=str, required=True,  metavar='<path>', 
                        help='path to the graph pickle file')
    parser.add_argument('-s', '--save-dir',  type=str, required=False, metavar='<directory>', default='extracted', 
                        help='path to the directory to put the opcode blocks')
    args = parser.parse_args()

    METHODS = ['summary', 'sequences', 'opcode_blocks']
    assert args.method in METHODS, 'Method not support'

    return args


def main():
    args = parse_args()
    args.file_name = os.path.basename(args.file_path)
    os.makedirs(args.save_dir, exist_ok=True)
    
    save_path = os.path.join(args.save_dir, args.file_name)
    if args.method == 'summary':
        summary = summarize(args.file_path)
        write_pickle(summary, save_path)
    
    elif args.method == 'sequences':
        sequences = generate_sequences(args.file_path)
        write_pickle(sequences, save_path)

    elif args.method == 'opcode_blocks':
        parser = GraphParser()
        opc_blocks = parser.get_opcode_blocks(args.file_path)
        write_pickle(opc_blocks, save_path)
        

if __name__=='__main__':
    main()
