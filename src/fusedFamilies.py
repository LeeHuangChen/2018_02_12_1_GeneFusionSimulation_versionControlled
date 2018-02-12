import os
import random
import sys
import subprocess
import fileIO_Includes as fio
import configuration as conf


# Finds the sequences of a given family and generation and returns it as a list of sequences
def FindSequencesByGeneration(familyPath, famID, genID):
    # navigate to the right sequence file
    curdir = familyPath
    allfam = os.listdir(curdir)
    for family in allfam:
        if family == ("f" + str(famID)):
            curdir = os.path.join(curdir, family)
            break
    if curdir == familyPath:
        sys.exit(
            "FindSequencesByGeneration(" + familyPath + ", " + famID + ", " + genID + "). Failed!\nCurdir=" + curdir)
    genPath = curdir
    gens = os.listdir(curdir)
    for gen in gens:
        if gen == ("g" + str(genID)):
            curdir = os.path.join(curdir, gen, gen + "_seq.txt")
            break
    if curdir == genPath:
        sys.exit(
            "FindSequencesByGeneration(" + familyPath + ", " + famID + ", " + genID + "). Failed!\nCurdir=" + curdir)
    # the resulting curdir would be the path of the seuence file. return the processed list.
    return fio.processSeqFile(curdir)


# Generate the tree required for the fused genes. This will be a binary tree with flexible number of generations
def generateTreeFlexible(path, seqs, seqLen, branchL, numGen):
    f = open(path, "w")
    f.write(str(len(seqs)) + " " + str(seqLen) + "\n")
    for i in range(len(seqs)):
        seq = seqs[i]
        f.write("Ancester " + seq + "\n")
    # write the number of trees (1)
    f.write("1\n")
    # tree for 1 generation
    tree = "(Taxoni:" + str(branchL) + ",Taxoni:" + str(branchL) + ")"
    # generate the multiple generation tree
    for i in range(1, numGen):
        tree = "(" + tree + ":" + str(branchL) + "," + tree + ":" + str(branchL) + ")"
    treeEdited = ""
    count = 1
    # replace the "i"'s in the tree as numbers
    for letter in tree:
        if letter == 'i':
            treeEdited = treeEdited + str(count)
            count = count + 1
        else:
            treeEdited = treeEdited + letter
    f.write(treeEdited)
    f.write(";")
    f.close()


def GenerateFusedGeneFamilies(famPath, fusedPath, model, numFusionEvents, seqLen, numFamilies, numGenerations,
                              TotalEvolutionTime):
    # directories
    fusedGeneFamilies = fusedPath

    branchLen = float(TotalEvolutionTime) / float(numGenerations)

    # check for directory and generate the directory
    fio.generateDirectories(fusedGeneFamilies)
    # if not os.path.exists(fusedGeneFamilies):
    # 	os.mkdir(fusedGeneFamilies)

    # make an empty log file
    log = open(os.path.join(fusedGeneFamilies, "$FusionLog.txt"), "w")
    log.write("#Fusion Events Log:\n")
    log.write("#evnt, fam1, fam2, gen, spliceLoc\n")
    log.close()

    # for each fusion event
    for i in range(numFusionEvents):
        # pick the random variable for
        rFam1 = random.randint(0, numFamilies - 1)
        rFam2 = random.randint(0, numFamilies - 1)
        rGen = random.randint(0, numGenerations - 1)
        rSpliceLoc = random.randint(seqLen / 10, seqLen / 2)

        # log the reneration of the fused genes
        with open(os.path.join(fusedGeneFamilies, "$FusionLog.txt"), "a") as log:
            line = str(i) + "\t" + str(rFam1) + "\t" + str(rFam2) + "\t" + str(rGen) + "\t" + str(rSpliceLoc) + "\n"
            log.write(line)

        # Find the two sequence families to combine
        family1 = FindSequencesByGeneration(famPath, rFam1, rGen)
        family2 = FindSequencesByGeneration(famPath, rFam2, rGen)
        seq1 = random.choice(family1)
        seq2 = random.choice(family2)

        newSeq = seq1[0:rSpliceLoc] + seq2[rSpliceLoc:seqLen]

        # the fused protein and the log for the seqgen will be this if there is no need for seqgen
        dataset = " 1 " + str(seqLen) + "\nTaxon1   " + newSeq
        log = "SeqGen is not used for this test case"

        # the the fused generation is not the last generation, use SeqGen to evolve the sequence further
        if rGen != (numGenerations - 1):
            # Generate the tree for this fusion event
            treePath = os.path.join(fusedGeneFamilies, "FuseT_" + str(i) + ".tree")

            generateTreeFlexible(treePath, [newSeq], seqLen, branchLen, numGenerations - rGen)

            if not len(newSeq) == seqLen:
                sys.exit("FusedSequence has wrong length: length=" + str(len(newSeq)))

            # custom code for my linux/windows setup
            if sys.platform == "linux2":
                seqGenURL = conf.seqGenURL_Linux
            else:  # windows version
                seqGenURL = conf.seqGenURL_Windows

            # seq-gen command
            cmd = [seqGenURL, model, "-l", str(seqLen), "-k", "1"]

            seq_gen_proc = subprocess.Popen(cmd, stdin=open(treePath, "r"), stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

            dataset, log = seq_gen_proc.communicate()

        with open(os.path.join(fusedGeneFamilies, "FuseFam_" + str(i)) + ".txt", "w") as f:
            f.write(dataset)
        with open(os.path.join(fusedGeneFamilies, "log_" + str(i)) + ".txt", "w") as f:
            f.write(log)


def main(model, seqLen, numFamilies, numFusionEvents, TotalEvolutionTime, numGenerations):
    name = fio.name(model, seqLen, numFamilies, numFusionEvents, TotalEvolutionTime, numGenerations)
    famPath = os.path.join(conf.generatedFolder, name, conf.famFolder)

    fusedPath = os.path.join(conf.generatedFolder, name, conf.fusedFolder)
    GenerateFusedGeneFamilies(famPath, fusedPath, model, numFusionEvents, seqLen, numFamilies, numGenerations,
                              TotalEvolutionTime)


if __name__ == "__main__":
    main()
