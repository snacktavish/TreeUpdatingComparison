# Updating phylogenetic trees with genomic data
### Work in progress - please contact ejmctavish@ucmerced.edu with any issues or questions.


## Description

[Extensiphy](https://github.com/McTavishLab/extensiphy.git) is a tool for updating an existing multiple sequence alignment [Field et al. 2022](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13790). Extensiphy works by taking an input alignment, and assembling homologous loci from raw short read data.

Say you built a sequence alignment and phylogeny for a group of bacteria during an outbreak and then received some new sequencing data that you wish to quickly incorporate into the phylogeny. Extensiphy makes it convenient to do this while also ensuring you can easily do this again any time you acquire new data.

### Use cases and required files

You can use Extensiphy in multiple ways. Depending on the input and output you wish to receive, you will need different data in different formats. 

In this tutorial we will update a *Neisseria gonhorrhea* core genome alignemnt with newly sequences short read data.

You need:
* Alignment file (fasta format)
* Directory of paired-end read files
* (Optional) a phylogeny generated from the input alignment

## Installation and testing


The repository and data should already be on your virtual machine, in the folder `extensiphy`.

All of the dependencies are already installed on the virtual machine except raxmlHPC
You can install it using:

```
    sudo apt-get install raxml
```

Check that the install is working by running:

```
    cd extensiphy
   ./extensiphy.sh -a ./testdata/combo.fas -d ./testdata -1 _R1.fq -2 _R2.fq -u PHYLO -o EP_output
```


### Extensiphy Help Menu
Extensiphy takes command line arguments to update a sequence alignment with new taxa sequences. Lets look at the options used by Extensiphy. Extensiphy use revolves around calling extensiphy.sh followed by flags (dashes next to a letter corresponding the option you wish to use or input).
Calling the help menu with the following command:

```bash
   $ ./extensiphy.sh -h
```

has the following output:

```
Extensiphy is a program for quickly adding genomic sequence data to multiple sequence alignments and phylogenies. 
     View the README for more specific information. 
     Inputs are generally a multiple sequence file in fasta format and a directory of 
     Fastq paired-end read sequences.     


 EXAMPLE COMMAND:     

 /path/to/extensiphy.sh -u ALIGN -a /path/to/alignment_file -d /path/to/directory_of_reads [any other options]     

 REQUIRED FLAGS     
 (-a) alignment in fasta format,     
 (-d) directory of paired end fastq read files for all query taxa,     
 (-u) produce only an updated alignment or perform full phylogenetic estimation (ALIGN or PHYLO) (DEFAULT: ALIGN)
    

 OPTIONAL FLAGS     
 (-t) tree in Newick format produced from the input alignment that you wish to update with new sequences or specify NONE to perform new inference (DEFAULT: NONE),     
 (-m) alignment type (SINGLE_LOCUS_FILES, PARSNP_XMFA or CONCAT_MSA) (DEFAULT: CONCAT_MSA),     
 (-o) directory name to hold results (DEFAULT: creates EP_output),     
 (-i) clean up intermediate output files to save HD space (Options: CLEAN, KEEP)(DEFAULT: KEEP),     
 (-r) Select a reference sequence from the alignment file for read mapping or leave as default and the first sequence in the alignment used (DEFAULT: RANDOM),     
 (-p) number of taxa to process in parallel,     
 (-c) number of threads per taxon being processed,     
 (-e) set read-type as single end (SE) or pair-end (PE) (DEFAULT: PE)     
 (-1, -2) suffix (ex: R1.fastq or R2.fastq) for both sets of paired end files (DEFAULTS: R1.fq and R2.fq),     
 (-g) output format (CONCAT_MSA or SINGLE_LOCUS_FILES) (DEFAULT: CONCAT_MSA),     
 (-s) specify the suffix (.fa, .fasta, etc) (DEFAULT: .fasta),     
 (-b) bootstrapping tree ON or OFF (DEFAULT: OFF)     


 if using single locus MSA files as input,     
 (-f) csv file name to keep track of individual loci when concatenated (DEFAULT: loci_positions.csv),     
 (-n) Set size of loci size cutoff used as input or output (Options: int number)     
 ```

Extensiphy has a number of default settings for these so you will not always have to explicitly use all of these options for every run. The use of these flags depends on the input you wish to use and the output you desire to have at the end of a run.



## Updating a phylogeny



We will try updating our existing alignment with three newly published sequences of gonorrhea.

The [SRR19310037](https://www.ncbi.nlm.nih.gov/sra/SRX15370312[accn]) and [SRR19310038](https://www.ncbi.nlm.nih.gov/sra/SRX15370313[accn]) were just added to NCBI's sequence read archive (SRA) on May 27, 2022!
SRR19127720 is from early May.


We can get more information about where these lineages were sequences, and if they cary antimicrobial resistance (AMR) genes using the data in NCBI's Pathogen Database


  - https://www.ncbi.nlm.nih.gov/pathogens/isolates/#SRR19310037
  - https://www.ncbi.nlm.nih.gov/pathogens/isolates/#SRR19310038
  - https://www.ncbi.nlm.nih.gov/pathogens/isolates/#SRR19127720


**Q** *Do any of these lineages have known anti-microbial resistance genes?*


The new sequence data and alignment to update are in the folder `extensiphy/Neisseria_demo`
```
    cd Neisseria_demo
```

(If you are are not running this on the MOLE virtual machines, you can download the data from [tar ball link](https://ucmerced.box.com/s/h6lxm9zwj1p013ek5lqea09oyyp2h5hy) and extract it)


If you wanted to download the sequences directly from SRA you could use
*Don't run these at the workshop (they wont work anyways unless you have installed SRA toolkit)*
```
    fastq-dump --split-files SRR19310037
    fastq-dump --split-files SRR19310038
    fastq-dump --split-files SRR19127720
```

NCBI places these sequences in a SNP tree, but that does not incorporate any uncertainty, or a full phylogenetic analysis.
https://www.ncbi.nlm.nih.gov/pathogens/tree/#Neisseria/PDG000000032.278/PDS000104772.5?accessions=PDT001307203.3


We will add these sequences to an existing core genome alignment generated using [ParSNP](https://harvest.readthedocs.io/en/latest/content/parsnp.html), and Extensiphy, published [Field et al 2022](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13790) and the alignment stored in Dryad [data deposit](https://datadryad.org/stash/dataset/doi:10.6071/M38T0T)

(I have subsampled the alignment from 1200 lineages to 30, and cut the sequences down to 500K BP to make inference faster for this demo).

```
    ../extensiphy.sh -a neisseria_aln.fas -1 _1.fastq -2 _2.fastq -d neisseria_reads/ -u PHYLO -o EP_demo_1
```
(This may take 5-10 min.)

The ML tree file will be in the file `EP_demo_1/RESULTS/RAxML_bestTree.consensusFULL`

Transfer it to your computer, and open it in figtree
Root it with "ERR2525602" as an outgroup.

By default, EP uses RaxmlHPC to estimate ML phylogenies - but the updated alignemnet is saved as output_dir/RESULTS/extended.aln, which you can use to estimate a phylogeny using any method.


The new taxa we have added were sampled in the last month - whereas the existing tips are from 2019 or earlier.

**Q** *Are our new sequences (SRR19310037, SRR19310038, and SRR19127720) closely related in the ML tree?*

You can have EP automatically bootstrap the tree as well by adding '-b ON' to the arguments.

Bootstrapping takes a little while - so I have run it for you, and put the output files in 'EP_demo/bootstrap_results/'

The majority rule consensus tree is in the file `bootstrap_results/RAxML_bipartitions.majority_rule_bootstrap_consensus
`

**Q** *Are our new sequences (SRR19310037, SRR19310038, and SRR19127720) closely related in the bootstrap consensus tree?*


Many of the common antimicrobial resistance (AMR) genes are horizontally transferred, so close relatives can have different AMR genes and phenotypes.
Look up the two closest relatives of the new lineage with known AMR genes in https://www.ncbi.nlm.nih.gov/pathogens/

**Q**  *Do these three lineages share the same resistance genes?*

## Using an alternate reference

The reference that you choose can affect your consensus sequencee calling, and therefore your phylogenetic inference. Lets try assemebling these new taxa, but using the outgroup as a reference instead.

```
../extensiphy.sh -a neisseria_aln.fas -1 _1.fastq -2 _2.fastq -d neisseria_reads/ -u ALIGN -r ERR2525602 -o EP_demo_alternate_ref
```

The consensus aligned sequence for each run is saved in output_dir/seqname_outputdir/seqname_align.fas (Where 'seqname' is the filename stub of the reads).

In the EP_demo folder is a really simple script that counts the differences between aligned sequences.

```
    python diff_counter.py <seq1> <seq2>
```

**Q** *Does changing the reference taxon change the sequences?*


We can then combine the previous extended alignemnt with these new, slightly different consensus sequence estimates.

Open each of your newly estimated sequences in a text editor (e.g. nano), and rename them to reflect that you used an alternate reference.

e.g. change ">SRR19310037" to  ">SRR19310037_alt"

Because they are already aligned, we can just concateneate them to form an alignment that includes both our original consesuses for these taxa, and these new inferences.

```cat EP_demo_1/RESULTS/extended.aln EP_demo_alternate_ref/SRR19310037output_dir/SRR19310037_align.fas EP_demo_alternate_ref/SRR19310038output_dir/SRR19310038_align.fas EP_demo_alternate_ref/SRR19127720output_dir/SRR19127720_align.fas > combined_refs.fas
```

We can then estimate a tree on this updated alignment - e.g. using RAxML (or any other phylogenetic inference software)

```
    raxmlHPC -s combined_refs.fas -m GTRGAMMA -p 1 -n compare_references 
```

Your ML tree will be saved as RAxML_bestTree.compare_references. Take a look at it in figtree.


**Q** *Does changing the reference taxon change the phylogeny?*





## Searching GenBank for homologous sequences
We also have a python package for updating trees by searching GenBank for homologous loci.

Check it out on GitHub [Physcraper](https://github.com/McTavishLab/physcraper), [Sanchez-Reyes 2021](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-021-04274-6)

