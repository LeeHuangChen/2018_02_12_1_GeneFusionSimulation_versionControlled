# configureation file for the simulator

generatedFolder = "GeneratedFiles"

# parameters
models = ["-mjtt"]
seqLens = [500]
numFamilies = [20]
numFusionEvents = [64, 128, 256, 512]
totalEvolutionTimes = [1.5, 2, 2.5, 2.75, 3]
numGenerations = [5]

seqGenURL_Linux = "./Resources/Seq-Gen_linux/source/seq-gen"
seqGenURL_Windows = "./Resources/Seq-Gen/source/seq-gen"

# Main Result Folders
protLenFolder = "Results/ProtLen"
fusionInfoFolder = "Results/FusionInfo"
allToAllFolder = "Results/allToall/"
sequenceFolder = "Results/FastaSequences"
blastDBFolder = "GeneratedFiles/BlastDataBase"

# log folders
logFolder = "GeneratedFiles/LogFiles"


# RandomFamilies Parameters
famFolder = "RandomFamilies"

# FusedGene Families Parameters
fusedFolder = "FusedGenesFamilies"

# processFusedGenes Parameters
processedFolder = "ProcessedFiles"
# famPath used for this program

# whether to include all sequences produced from a particular fusion event to compiling the fasta file
# includeAll=True
includeAll = False

# blastpAndDataProc Parameters
# processedPath is used
blastpOutfilename = "test.csv"  # the output file name for the all-to-all blastp
add = "_proc"
# the processed output file for MosaicFinder developed by Pierre-Alain Jachiet et al.
blastpOutfilename_processed = blastpOutfilename.replace(".csv", add + ".csv")
resultFolder = "Results/allToall/"
processedResultFolder = "Results/allToall_mosaicFinder/"
