#!/usr/bin/env python3
"""example usage:
python get_synth_subtree.py --input-file ../../../LizardData/output/main.csv 
"""

import argparse
import sys
from opentree import OT

parser = argparse.ArgumentParser(description='Get a synthetic subtree for a set of OTT ids')
parser.add_argument("--ott-ids", help="The list of ott ids")
parser.add_argument("--input-file", 
                    help="A file containing the ids. Either a single column or comma delimited")
parser.add_argument("--ott-id-header",default="OTT TAXON ID",
                    help="Header for column containing the ids")
parser.add_argument("--label-format",  default="name_and_id",
                    help='The label format for the output tree')
parser.add_argument("--file-format", default="newick",
                    help='The file format for the output tree')
parser.add_argument("--output-tree", default="output.tre",
                    help='The file name for the output tree')
parser.add_argument("--output-info", default="citations.txt",
                    help='The file name for the citations')
#parser.print_help()

args = parser.parse_args()

ott_ids = set()

assert(args.input_file or args.ott_ids), "Either an ott-ids argument or a file containing ids is required"
if args.input_file:
    with open(args.input_file) as csvfile:
        header = csvfile.readline().split(',')
        column = header.index(args.ott_id_header)
        for line in csvfile:
            row = line.split(',')
            ott_id = row[column]
            if ott_id:
                ott_ids.add(int(ott_id))
else:
    for ott_id in args.ott_ids:
        try:
            ott_ids.add(int(ott_id))
        except ValueError:
            sys.stderr.write("{o} not an integer".format(ott_id))


output = OT.synth_induced_tree(ott_ids = ott_ids,
                               label_format = args.label_format)

print("Newick tree saved to {of}".format(of = args.output_tree))
of = open(args.output_tree, 'w')
of.write(output.response_dict['newick'])

print("Citation info saved to {cf}".format(cf = args.output_info))
cf = open(args.output_info, 'w')

for study in output.response_dict['supporting_studies']:
    study_id, tree_id = study.split('@')
    url = 'https://tree.opentreeoflife.org/curator/study/view/{s}/?tab=home&tree={t}'.format(s=study_id,
                                                                                             t=tree_id)
    cite = OT.get_citations([study_id])
    cf.write(cite)
    cf.write("Link to tree: " + url)
    cf.write("\n"+"-----------------------------------------------------------------------------"+"\n")

cf.close()