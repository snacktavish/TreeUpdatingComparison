**Q** *Are any of the genera non-monophyletic? What one(s)?*
Laomedea, Obelia


**Q** *Look at this genus/genera in the tree viewer. What studies break the monophyly of each taxon?*

Maronna 2016, Cuhna 2017, Leclere 2009

**Q** *Is there conflict among the input sources? Does the alternate resolution demonstrate reciprocal monophyly?*

There is conflict across the different Cuhna trees, but still not reciprocal monophyly.

**Q** *Are the relationships in 'turtle_iqtree_OTT.tre' different than the relationships from OpenTree?*

Yes


**Q** *How so?*  

OpenTree: ((Python,Anolis carolinensis), Podarcis) 
Iqtree: ((Anolis carolinensis, Podarcis), Python)


OpenTree: (((Alligator, Caiman),(Gallus, Taeniopygius)),(((Emys, Chelonius), Caretta), Phyrnops));
Iqtree: (((Alligator, Caiman),(((Emys, Chelonius), Caretta), Phyrnops)),(Gallus, Taeniopygius));

**Q** *Is there anything surprisng about these relationships? (The answer probably depends on your pre-existing herp phylogeny knowledge :P)*

'lizards' are not a monophyletic group!

**Q** What are the maximum and minimum age estimates for the root of this three taxon tree?

Root is Episquamata ott4945816

Max age is 
Age: 206.62653 Myr
Study: ot_2008@tree3 
https://tree.opentreeoflife.org/curator/study/view/ot_2008?tab=trees&tree=tree3
Roquet, C., Lavergne, S., & Thuiller, W. (2014). One Tree to Link Them All: A Phylogenetic Dataset for the European Tetrapoda. PLoS Currents. doi:10.1371/currents.tol.5102670fff8aa5c918e78f5592790e48

http://dx.doi.org/10.1371/currents.tol.5102670fff8aa5c918e78f5592790e48


Min age is:
Age: 163.041626 Myr
Study: ot_307@tree2 
https://tree.opentreeoflife.org/curator/study/view/ot_307?tab=trees&tree=tree2
Wright, April M., Kathleen M. Lyons, Matthew C. Brandley, David M. Hillis. 2015. Which came first: The lizard or the egg? Robustness in phylogenetic reconstruction of ancestral states. Journal of Experimental Zoology Part B: Molecular and Developmental Evolution 324 (6): 504-516
http://dx.doi.org/10.1002/jez.b.22642



**Q** Is there overlap between the age estimates for the root and for the internal node?

Yes - root is 163-209 MYA, internal node is 160-198 Mya


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
