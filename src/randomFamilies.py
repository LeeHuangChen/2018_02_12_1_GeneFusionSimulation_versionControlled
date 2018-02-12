#!/bin/sh
import subprocess
import sys
import os
import random
import fileIO_Includes as fio
import configuration as conf


def random_AA_seq(length):
    seq = ''.join(random.choice('ACDEFGHIKLMNPQRSTVWY') for i in range(length))
    # return "TaxonA "+seq
    return seq


# Generate the trees required for random families, since we need to keep track of the sequences of
# the generations, we are only making binary tree of depth 1
def generateTree(path, seqs, seqLen, branchL):
    f = open(path, "w")
    f.write(str(len(seqs)) + " " + str(seqLen) + "\n")
    for i in range(len(seqs)):
        seq = seqs[i]
        f.write("Ancester" + str(i) + " " + seq + "\n")
    f.write("1\n(Taxon1:" + str(branchL) + ",Taxon2:" + str(branchL) + ");")
    f.close()


# main functions
def GenerateRandomFamilies(famPath, model, seqLen, numFamilies, numGenerations, TotalEvolutionTime):
    randomFamilies = famPath
    branchLen = float(TotalEvolutionTime) / float(numGenerations)

    # generate directories
    fio.generateDirectories(randomFamilies)

    # generate random ancestral sequences and the initial tree for the families
    for i in range(numFamilies):
        # create the family path
        familyPath = os.path.join(randomFamilies, "f" + str(i))
        fio.testPath(familyPath)

        # generate trees and sequences for each subsequent generations
        for j in range(numGenerations):
            # define all the paths needed
            generationPath = os.path.join(familyPath, "g" + str(j))
            fio.testPath(generationPath)

            treePath = os.path.join(generationPath, "f" + str(i) + "_g" + str(j) + ".tree")
            sequencePath = os.path.join(generationPath, "g" + str(j) + "_seq.txt")
            logPath = os.path.join(generationPath, "g" + str(j) + "_log.txt")
            fio.createEmptyFiles([sequencePath, logPath])

            sequences = []
            # first generation is generated randomly
            if j == 0:
                # generate the tree file for Seq-Gen
                sequences.append(random_AA_seq(seqLen))
            else:
                # then there exist a sequence file in the previous generation
                prevGenSeqPath = os.path.join(familyPath, "g" + str(j - 1), "g" + str(j - 1) + "_seq.txt")
                seqs = fio.processSeqFile(prevGenSeqPath)
                for seq in seqs:
                    sequences.append(seq)

            generateTree(treePath, sequences, seqLen, branchLen)

            for k in range(1, len(sequences) + 1):
                # custom code for my linux/windows setup
                if sys.platform == "linux2":
                    seqGenURL = conf.seqGenURL_Linux
                else:  # windows version
                    seqGenURL = conf.seqGenURL_Windows

                # seq-gen command
                cmd = [seqGenURL, model, "-l", str(seqLen), "-k", str(k)]

                seq_gen_proc = subprocess.Popen(cmd, stdin=open(treePath, "r"), stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)

                dataset, log = seq_gen_proc.communicate()

                fio.appendFile(sequencePath, dataset)
                fio.appendFile(logPath, log)


def main(name, model, seqLen, numFamilies, numGenerations, TotalEvolutionTime):
    famPath = os.path.join(conf.generatedFolder, name, conf.famFolder)
    GenerateRandomFamilies(famPath, model, seqLen, numFamilies, numGenerations, TotalEvolutionTime)


if __name__ == "__main__":
    main()
