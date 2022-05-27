#!/usr/bin/env python3
"""example usage:
python  get_dates.py --ott-ids 970153 937560  --output lizard
"""
import os
import argparse
import sys
import json
import requests
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
parser.add_argument("--output", default="synth_dates",
                    help='The file name stub for the outputs')


## this reads in the command line arguments
args = parser.parse_args()

assert(args.input_file or args.ott_ids), "Either an ott-ids argument or a file containing ids is required"

ott_ids = set()

assert(args.input_file or args.ott_ids), "Either an ott-ids argument or a file containing ids is required"
if args.input_file:
    assert os.path.exists(args.input_file), "{a} not found".format(a=args.input_file)
    with open(args.input_file) as csvfile:
        header = csvfile.readline().split(',')
        try:
            column = header.index(args.ott_id_header)
        except ValueError:
            sys.stderr.write("Column label '{oth}' not found in hearder row. Exiting.\n".format(oth=args.ott_id_header))
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

datefile = "{o}_dates.txt".format(o=args.output)
df = open(datefile, "w")

if len(ott_ids) == 1:
    ott_id = 'ott' + str(list(ott_ids)[0])
    r = requests.get('https://dates.opentreeoflife.org//v4/dates/synth_node_age/{o}'.format(o=ott_id))
    age_data = json.loads(r.content.decode())
    if age_data.get("ot:source_node_ages"):
        df.write("Ages for node {nl}\n\n".format(nl=ott_id))
        for source in age_data["ot:source_node_ages"]:
            df.write("Age: {a} Myr\n".format(a=source['age']))
            df.write("Study: {s} \n".format(s=source['source_id']))                
            cite = OT.get_citations([source['source_id']])
            df.write(cite)
            df.write("\n---\n\n")
    else:
        df.write("No age data found for {o}\n".format(o=ott_id))
    df.write("\n"+"*******************************************************************************"+"\n")
    df.close()
    print("Age information info saved to {df}".format(df = datefile))
    sys.exit()

## If multiple IDs, need to get the tree.
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
tree = dendropy.Tree.get(data = api_call.response_dict['newick'], schema='newick')

## You can actually get a lot more 
tree.suppress_unifurcations()

tree.print_plot()

treefile = "{o}.tre".format(o=args.output)
tree.write(path=treefile, schema="newick")
print("Newick tree saved to {of}".format(of = treefile))


for node in tree:
    if node.label:
        node_id = node.label.split()[-1]
        r = requests.get('https://dates.opentreeoflife.org//v4/dates/synth_node_age/{}'.format(node_id))
        age_data = json.loads(r.content.decode())
        if age_data.get("ot:source_node_ages"):
            df.write("Ages for node {nl}\n\n".format(nl=node.label))
            for source in age_data["ot:source_node_ages"]:
                df.write("Age: {a} Myr\n".format(a=source['age']))
                df.write("Study: {s} \n".format(s=source['source_id']))                
                cite = OT.get_citations([source['source_id']])
                df.write(cite)
                df.write("\n---\n\n")
            df.write("\n"+"*******************************************************************************"+"\n")
        else:
            df.write("no age data found for {nl}\n".format(nl=node.label))
df.close

print("Age information info saved to {df}".format(df = datefile))

