**Q** *How many published trees were used in this synthetic tree estimate?*  

13 tree from 12 published papers

**Q** *Are the relationships in 'turtle_iqtree_OTT.tre' different than the relationships from OpenTree?*

Yes


**Q** *How so?*  

OpenTree: ((Python,Anolis carolinensis), Podarcis) 
Iqtree: ((Anolis carolinensis, Podarcis), Python)


OpenTree: (((Alligator, Caiman),(Gallus, Taeniopygius)),(((Emys, Chelonius), Caretta), Phyrnops));
Iqtree: (((Alligator, Caiman),(((Emys, Chelonius), Caretta), Phyrnops)),(Gallus, Taeniopygius));


**Q** *What are the relationships among these taxa?*  


Casseopia 811884
Aurellia 404483 
Mastigias 775011
Rhopilema 657620 (Non monopyletic, click on "look in taxonomy browser for genus id)

python get_synth_subtree.py --ott-ids 811884 404483 775011 657620 --output jellyfish

((Rhizostomatidae_ott369199,(Cassiopea_ott811884,Mastigias_ott775011)Kolpophorae_ott5665229)Rhizostomeae_ott570654,'Aurelia (genus in phylum Cnidaria) ott404483')mrcaott3524ott12088;



**Q** *Which taxon is most closely related to mastigias?*

Cassiopiea


**Q** *What studies support this inference?*  

 Kayal et al 2013, Bayha et al 2010


**Q** *Which genus is not in the output tree? Why not?*  
Rhopilema  
The genus is not monophyletic  

**Q**  *What phylogenetically supported three-taxon relationship breaks up this genus?*  

((Rhizostoma pulmo, Rhopilema verrilli), Rhopilema esculentum)  
