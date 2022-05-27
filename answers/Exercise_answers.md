**Q1** Are the relationships in 'turtle_iqtree_OTT.tre' different than the relationships from OpenTree?


Yes


**Q2** How so?
OpenTree: ((Python,Anolis carolinensis), Podarcis) 
Iqtree: ((Anolis carolinensis, Podarcis), Python)


OpenTree: (((Alligator, Caiman),(Gallus, Taeniopygius)),(((Emys, Chelonius), Caretta), Phyrnops));
Iqtree: (((Alligator, Caiman),(((Emys, Chelonius), Caretta), Phyrnops)),(Gallus, Taeniopygius));



Q3: 

Casseopia 811884
Aurellia 404483 
Mastigias 775011
Rhopilema 657620 (Non monopyletic, click on "look in taxonomy browser for genus id)

python get_synth_subtree.py --ott-ids 811884 404483 775011 657620 --output jellyfish


Q4 Kayal et al 2013, Bayha et al 2010

Q5 Rhopilema

Q6 ((Rhizostoma pulmo, Rhopilema verrilli), Rhopilema esculentum)

Q7 No.