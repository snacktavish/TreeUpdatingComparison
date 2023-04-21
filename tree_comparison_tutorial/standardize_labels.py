#!/usr/bin/env python3
"""example usage:
python standardize_labels.py --input-tree  
"""
import os
import argparse
import sys
import dendropy
from opentree.taxonomy_helpers import standardize_labels

parser = argparse.ArgumentParser(description='Remove problematic characters form taxon labels')
parser.add_argument("--input-tree", required=True, help="input newick tree file")
parser.add_argument("--output-tree", required=True, help='The file name for the output tree')
parser.add_argument("--problem-chars", default='():#',
                    help='characters to remove from labels')
parser.add_argument("--replacement-char", default='_',
                    help='Character replace problematic characters with')

## this reads in the command line arguments
args = parser.parse_args()

assert os.path.exists(args.input_tree), "{a} not found".format(a=args.input_tree)


tree = dendropy.Tree.get(path=args.input_tree, schema='newick')

outtree = standardize_labels(tree, prob_char=args.problem_chars, replace_w=args.replacement_char)

outtree.write(path=args.output_tree, schema='newick')
