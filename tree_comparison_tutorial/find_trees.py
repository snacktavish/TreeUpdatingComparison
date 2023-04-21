#!/usr/bin/env python3
"""example usage:
python find_trees.py "Homarus americanus" --property ot:ottTaxonName
"""

import argparse
import sys
import json
from opentree import OT

parser = argparse.ArgumentParser(description='Look up trees in the "phylesystem" set of phylogenetic studies that are in Open Tree')
parser.add_argument("value", help="The value of the property to match")
parser.add_argument("--property", default=None, required=True,
                     help='The name of the field to search through. e.g.  "ot:originalLabel", "ot:ottTaxonName", "ot:studyId", "ot:ottId"')
parser.add_argument("--exact", action="store_true", help='disables fuzzy matching')
#parser.print_help()

args = parser.parse_args()

api_call = OT.find_trees(args.value, 
                       search_property=args.property,
                       exact=args.exact)


for study in api_call.response_dict['matched_studies']:
   for tree in study['matched_trees']:
      study_id = tree['ot:studyId']
      tree_id = tree['ot:treeId']
      url = 'https://tree.opentreeoflife.org/curator/study/view/{s}/?tab=home&tree={t}'.format(s=study_id,
                                                                                                t=tree_id)
      cite = OT.get_citations([study_id])
      print(cite)
      print("Link to tree: " + url)
      print("\n"+"-----------------------------------------------------------------------------"+"\n")
