
Gene Fusion Simulator



Running the program
to have the program conduct blastp all-to-all, you must install the blast command line available at:
	ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/

this also uses Biopython (http://biopython.org/)

Before executing this program, check if there is a folder called "GeneratedFiles" in the folder.  The folder contains generated files from the previous execution and you can delete it
To execute this program, open and check the configuration.py file.  This file contains all the configuration for the simulation.

After finishing editing the configuration file. Open up the root directory in the terminal and type:

$ python run.py

to execute the program

The FASTA file containing all the generated sequences should be located at "processedPath from configuation.py"/mergedSequences.fasta

The protein names represent the following:

protein name: [fid]F[f1]F[f2]G[g]S[s]GID[gid]
	fid:the fusion id of this protein (i.e. which fusion is this protein from)
	f1: the first family sequence used to conduct the fusion (for the first part of the sequence) 
	f2: the second family sequence used to conduct the fusion (for the last part of the sequence) 
	g: the generation that the splitting occurred (the current implementation requires this to be at least 1, which means that all sequences had the fusion even at least one iteration before the current time)
	s: this number indicate the splitting location for the fusion event
	gid: