import os
import sys
import argparse
import networkx as nx

import torch
from torchnlp.encoders.text import pad_tensor

from Basics import *


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


def parse_args():
    parser = argparse.ArgumentParser(description='Opcode Block Summarizing Script')
    parser.add_argument('--method', type=str, required=True, metavar='[summary | opcode_blocks]',
                        help='information to obtain')
    parser.add_argument('-f', '--file-path', type=str, required=True,  metavar='<path>', 
                        help='path to the graph pickle file')
    parser.add_argument('-s', '--save-dir',  type=str, required=False, metavar='<directory>', default='extracted', 
                        help='path to the directory to put the opcode blocks')
    args = parser.parse_args()

    METHODS = ['summary', 'opcode_blocks']
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

    elif args.method == 'opcode_blocks':
        parser = GraphParser()
        opc_blocks = parser.get_opcode_blocks(args.file_path)
        write_pickle(opc_blocks, save_path)


if __name__=='__main__':
    main()
