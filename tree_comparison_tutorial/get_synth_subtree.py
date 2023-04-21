#!/usr/bin/env python3
"""example usage:
python get_synth_subtree.py --input-file ../../../LizardData/output/main.csv 
"""
import os
import json
import argparse
import sys
import dendropy
from opentree import OT

parser = argparse.ArgumentParser(description='Get a synthetic subtree for a set of OTT ids')
parser.add_argument("--ott-ids", nargs='+', help="The list of ott ids")
parser.add_argument("--input-file", 
                    help="A file containing the ids. Must be comma delimited, and have a header row.")
parser.add_argument("--ott-id-header",default="OTT TAXON ID",
                    help="Header for column containing the ids")
parser.add_argument("--label-format",  default="name_and_id",
                    help='The label format for the output tree')
parser.add_argument("--file-format", default="newick",
                    help='The file format for the output tree')
parser.add_argument("--output", default="synth_subtree",
                    help='The file name stub for the outputs')


## this reads in the command line arguments
args = parser.parse_args()

ott_ids = set()

assert(args.input_file or args.ott_ids), "Either an ott-ids argument or a file containing ids is required"
if args.input_file:
    assert os.path.exists(args.input_file), "{a} not found".format(a=args.input_file)
    with open(args.input_file) as csvfile:
        header = csvfile.readline().split(',')
        try:
            column = header.index(args.ott_id_header)
        except ValueError:
            sys.stderr.write("Column label '{oth}' not found in header row. Exiting.\n".format(oth=args.ott_id_header))
            sys.exit()
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
            sys.stderr.write("{o} not an integer".format(o=ott_id))


## Call the OpenTree API's on the ids
## This call returns a dictionary 'response_dict' 
## with keys including
## 'newick', the tree in newick format
## 'supporting studies ', the input phylogeneies that go into thsee relationships.

api_call = OT.synth_induced_tree(ott_ids = ott_ids,
                               label_format = args.label_format)


## OpenTree labels internal nodes - which is handy sometimes, 
## but results in a bunch of 'unififurcations' - single labeled nodes in the middle of long branches.
## We can use dendropy to supress those extra nodes.
tree = dendropy.Tree.get(data = api_call.response_dict['newick'], schema='newick',  suppress_internal_node_taxa=True)
tree.suppress_unifurcations()

tree.print_plot()

treefile = "{o}.tre".format(o=args.output)
tree.write(path=treefile, schema="newick")
print("Newick tree saved to {of}".format(of = treefile))


print("Gathering citations...\n")
citefile = "{o}_citations.txt".format(o=args.output)

cf = open(citefile, 'w')
## The citation info in the response is in short form "study_id@tree_id"
for study in api_call.response_dict['supporting_studies']:
    study_id, tree_id = study.split('@')
    url = 'https://tree.opentreeoflife.org/curator/study/view/{s}/?tab=home&tree={t}'.format(s=study_id,
                                                                                             t=tree_id)
    cite = OT.get_citations([study_id])
    cf.write(cite)
    cf.write("Link to tree: " + url)
    cf.write("\n"+"-----------------------------------------------------------------------------"+"\n")

cf.close()
print("Citation info saved to {cf}".format(cf = citefile))


brokenfile = "{o}_broken_taxa.txt".format(o=args.output)
bf = open(brokenfile, 'w')
bf.write(json.dumps(api_call.response_dict['broken']))
bf.close()
