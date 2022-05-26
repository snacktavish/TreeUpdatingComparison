#!/usr/bin/env python3
import json
import sys
from opentree import OTCommandLineTool

def main(arg_list, out, list_for_results=None):
    cli = OTCommandLineTool(usage='Look up trees in the "phylesystem" set of phylogenetic studies that are in the Open '
                        'system')
    cli.parser.add_argument("value", help="The value of the property to match")
    cli.parser.add_argument("--property", default=None, required=True,
                        help='The name of the field to search through.')
    cli.parser.add_argument("--verbose", action="store_true", help='include meta-data in response')
    cli.parser.add_argument("--exact", action="store_true", help='disables fuzzy matching')
    OT, args = cli.parse_cli(arg_list)

    output = OT.find_trees(args.value, search_property=args.property, verbose=args.verbose, exact=args.exact)

    if list_for_results is not None:
        list_for_results.append(output)
    if out is not None:
        sf = json.dumps(output.response_dict, indent=2, sort_keys=True)
        out.write('{}\n'.format(sf))


if __name__  == '__main__':
    rc = main(sys.argv[1:], sys.stdout)
    sys.exit(rc)

json_file = "main.json"
assert os.path.isfile(json_file) #check the file exists and the path is correct


citations_file = "cites.txt"
induced_subtree = "synth_subtree.tre"


print("Getting synth subtree...\n")

#Use the bulk TNRS output to match your existing tree to standard labels
otu_dict = opentree_helpers.bulk_tnrs_load(json_file)

#Get the synthetic tree for the taxa in your estimated tree
ott_ids =set()
for otu in otu_dict:
   ott_ids.add(otu_dict[otu].get("^ot:ottId"))

#turn it back into a list
ott_ids = list(ott_ids)

tre = opentree_helpers.get_tree_from_synth(ott_ids=ott_ids, label_format="name", citation= citations_file)

# The synth tree doesn't have any branch lengths. That's generally fine, but some tree viewers want them!
# Lets set each branch length to 1
# Thanks Jeet Sukumaran and Dendropy for making this easy!!
for edge in tre.postorder_edge_iter():
    edge.length = 1.0


tre.write(path=induced_subtree,
          schema="newick",
          suppress_internal_taxon_labels=True,
          suppress_internal_node_labels=True)
