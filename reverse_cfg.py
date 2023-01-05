# ------ Versions ------
#  angr      |   9.2.32
#  networkx  |   2.8.8
# ----------------------

from angr import Project
import networkx as nx
import logging
import pickle

import os
import sys
from datetime import datetime
import argparse

# TIMEOUT = 180

def timer(func):
    from time import time
    
    def wrapper(*arg, **kwargs):
        start = time()
        result = func(*arg, **kwargs)
        end = time() - start
        return result, end

    return wrapper


class CFGParser:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
    
    def parse(self, mode='warning'):
        logger = logging.getLogger('angr')
        logger.setLevel(mode.upper())
        
        self.print_info('Create Project')
        self.create_project()
        self.print_info('Start Emulation')
        self.emulated()
        self.print_info('Adjust CFG')
        G = self.adjust_cfg()

        self.print_info('Completed')

        return G
    
    def print_info(self, info):
        print('[INFO] [{}] | {}'.format(datetime.now(), info), file=sys.stderr)
    
    def create_project(self):
        self.p = Project(self.path, load_options={'auto_load_libs': False})

    def emulated(self):
        cfg = self.p.analyses.CFGEmulated(keep_state=True)
        cfg.normalize()
        self.cfg = cfg.graph
        
    def adjust_cfg(self):
        for node in self.cfg.nodes(data=False):
            self.cfg.nodes[node]['bName'] = self.get_name(node)
            if node.block is None:
                self.cfg.nodes[node]['x'] = [self.get_addr(node), 'nop']
            
            else:
                try:
                    disasm = str(node.block.disassembly)
                    self.cfg.nodes[node]['x'] = self.parse_asm(node.block.disassembly) if disasm else [self.get_addr(node), 'nop']

                except KeyError:
                    # some error that I have no clue how to deal with
                    self.cfg.nodes[node]['x'] = [self.get_addr(node), 'nop']

        mapping = {node: i for i, node in enumerate(self.cfg.nodes(data=False))}
        return nx.relabel_nodes(self.cfg, mapping)

    def get_name(self, CFGNode_obj):
        string = str(CFGNode_obj)
        return string.replace('>', '').split()[1]

    def get_addr(self, CFGNode_obj):
        string = str(CFGNode_obj)
        return string.replace('>', '').split()[-1]
    
    def parse_asm(self, disasm):
        parsed = []
        disasm = str(disasm)
        for line in disasm.split('\n'):
            addr, asm = line.split(':\t')
            asm = asm.replace('\t', ' ')
            parsed.append([addr, asm])
        return parsed


def parse_args():
    parser = argparse.ArgumentParser(description='P4 Mininet Topology Generator')
    parser.add_argument('-f', '--file-path', type=str, required=True, metavar='<path>', 
                        help='path to the binary file')
    parser.add_argument('-m', '--mode', type=str, required=False, default='warning',
                        metavar='debug | info | warning | error | critical', 
                        help='path to the binary file')
    parser.add_argument('-o', '--output-dir', type=str, required=False, default='CFGs', metavar='<directory>', 
                        help='directory to save the extracted CFG files')
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    parser = CFGParser(args.file_path)
    cfg = parser.parse(args.mode)
    
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, os.path.basename(args.file_path)), 'wb') as f:
        pickle.dump(cfg, f)


if __name__=='__main__':
    main()