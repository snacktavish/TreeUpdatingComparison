# Data Set assembly
### Work in progress - please contact ejmctavish@ucmerced.edu with any issues or questions.


## Description

We will compare sequences assembled from short read data using a few different parameter choices, and assess accuracy of the consensus sequence, and of the phylogenetic inferences.


Clone the exercise repo and cd into the directory for this example if you havn't aleady done so:

    git clone git@github.com:snacktavish/sequence_data_exercise.git
    cd Neisseria_demo


## Background
We are going to investigate three newly published sequences of gonorrhea.

The [SRR19310037](https://www.ncbi.nlm.nih.gov/sra/SRX15370312[accn]) and [SRR19310038](https://www.ncbi.nlm.nih.gov/sra/SRX15370313[accn]) were just added to NCBI's sequence read archive (SRA) on May 27, 2022!
SRR19127720 is from early May.


We can get more information about where these lineages were sequences, and if they cary antimicrobial resistance (AMR) genes using the data in NCBI's Pathogen Database. (See the "AMR Genotype column")


  - https://www.ncbi.nlm.nih.gov/pathogens/isolates/#SRR19310037
  - https://www.ncbi.nlm.nih.gov/pathogens/isolates/#SRR19310038
  - https://www.ncbi.nlm.nih.gov/pathogens/isolates/#SRR19127720

**Q Do any of these lineages have known anti-microbial resistance genes?**


If you wanted to download the sequences directly from SRA you could use
*Don't run these at the workshop (they wont work anyways unless you have installed SRA toolkit)*

    fastq-dump --split-files SRR19310037
    fastq-dump --split-files SRR19310038
    fastq-dump --split-files SRR19127720

NCBI places these sequences in a SNP tree, but that does not incorporate any uncertainty, or a full phylogenetic analysis.
https://www.ncbi.nlm.nih.gov/pathogens/tree/#Neisseria/PDG000000032.278/PDS000104772.5?accessions=PDT001307203.3


We will add these sequences to an existing core genome alignment generated using [ParSNP](https://harvest.readthedocs.io/en/latest/content/parsnp.html), and Extensiphy, published [Field et al 2022](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13790) and the alignment stored in Dryad [data deposit](https://datadryad.org/stash/dataset/doi:10.6071/M38T0T)


[Extensiphy](https://github.com/McTavishLab/extensiphy.git) is a tool for updating an existing multiple sequence alignment [Field et al. 2022](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13790). Extensiphy works by taking an input alignment, and assembling homologous loci from raw short read data.

For more info on how to use Extensiphy, see https://github.com/snacktavish/Mole2022/blob/master/TreeUpdating.md and https://github.com/McTavishLab/extensiphy/blob/main/tutorial/extensiphy_tutoria.md


*I have run the assembly and subsampled the alignment from 1200 lineages to 30, and cut the sequences down to 100K BP to make inference faster for this demo. To see how to run this from raw data, see https://github.com/snacktavish/Mole2022/blob/master/TreeUpdating.md)*

The starting alignment is in neisseria_aln.fas.
The updated alignment is in EP_demo/RESULTS/extended.aln 

Estimate an ML tree using raxml


Open it in figtree
Root it with "ERR2525602" as an outgroup.

The new taxa we have added were sampled in the last two months - whereas the existing tips are from 2019 or earlier.

**Q Are our new sequences (SRR19310037, SRR19310038, and SRR19127720) closely related in the ML tree?**

You can have EP automatically bootstrap the tree as well by adding '-b ON' to the arguments.

Bootstrapping takes a little while - so I have run it for you, and put the output files in 'EP_demo/bootstrap_results/'

The majority rule consensus tree is in the file `bootstrap_results/RAxML_bipartitions.majority_rule_bootstrap_consensus
`

**Q Are our new sequences (SRR19310037, SRR19310038, and SRR19127720) closely related in the bootstrap consensus tree?**

**Q What do these relationships suggest about if this is a new outbreak cluster, or endemic variation?**


Many of the common antimicrobial resistance (AMR) genes are horizontally transferred, so close relatives can have different AMR genes and phenotypes.
Look up the two closest relatives of the new lineage with known AMR genes in https://www.ncbi.nlm.nih.gov/pathogens/

**Q Do these three lineages share the same known resistance genes?**


## Using an alternate reference

The reference that you choose can affect your consensus sequence calling, and therefore your phylogenetic inference. Lets see what happens if we try assembling these new taxa, but using the outgroup as a reference instead.


The consensus aligned sequence for each run is saved in combine_and_infer/seqname_align.fas (Where 'seqname' is the filename stub of the reads).


In your pre-workshop exercises, you developed a script to compare sequences in fasta files.

Use that script now to investigate how these sequences differ between assemblies! (or concatenate them, and open them in seqview, and eyeball it)


**Q Does changing the reference taxon change the inferred sequences?**


**Q What do the differences in the sequences consist of (in terms of different base calls)?**


We can then combine the previous extended alignment with these new, slightly different consensus sequence estimates.

Open each of the consensus sequences from the alternate reference in a text editor, and rename them to reflect that you used an alternate reference.

e.g. change ">SRR19310037" to  ">SRR19310037_alt"

Because they are already aligned, we can just concateneate them to form an alignment that includes both our original consesuses for these taxa, and these new inferences.


    cat EP_demo/RESULTS/extended.aln EP_demo_alternate_ref/combine_and_infer/SRR19310037_align.fas EP_demo_alternate_ref/combine_and_infer/SRR19310038_align.fas EP_demo_alternate_ref/combine_and_infer/SRR19127720_align.fas > combined_refs.fas


We can then estimate a tree on this updated alignment - e.g. using RAxML (or any other phylogenetic inference software)

    raxml-ng -msa combined_refs.fas -model GTR+G -prefix compare_references 

Take a look at your ML tree in figtree. (what model would you use?)


**Q Does changing the reference taxon change the phylogeny or inferences you would make from it?**


