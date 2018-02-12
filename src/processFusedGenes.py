import os
import configuration as conf
import fileIO_Includes as fio
import random


# process the sequences files inside fusedPath in to a sequence file in the FASTA format.
# The processed file will contain:
# either one or all of each protein from the the fusion families
# this is toggled by the bool: includeAll
# all of the proteins from the gene family, located in conf.famPath2
def processFusedGenes(name, fusedPath, famPath, includeAll):
    # adding the fused proteins into the fasta file

    # obtain all the file names from fusedPath
    filenames = os.listdir(fusedPath)
    fuseDict = fio.readFusionEventLog(os.path.join(fusedPath, "$FusionLog.txt"))

    # generate the sequence file
    fio.generateDirectories(conf.sequenceFolder)
    seqPath = os.path.join(conf.sequenceFolder, name+".fasta")
    open(seqPath, "w")

    for filename in filenames:
        # checks for sequences files
        if "FuseFam" in filename:
            fuseID = int(filename.replace("FuseFam_", "").replace(".txt", ""))

            # read the sequences in the file
            seqs = fio.processSeqFile(os.path.join(fusedPath, filename))
            if not includeAll:
                # randomly picks one of the sequence from seq and delete the rest
                seq = random.choice(seqs)
                seqs = [seq]

            for i in range(len(seqs)):
                proteinName = "ID_" + fuseDict[fuseID][0] + "_F1_" + fuseDict[fuseID][1] + "_F2_" + fuseDict[fuseID][
                    2] + "_G_" + fuseDict[fuseID][3] + "_SplitPt_" + fuseDict[fuseID][4] + "_GenID_" + str(i)
                taxaName = "testTaxa"

                content = fio.toFASTA(proteinName, taxaName, seqs[i])
                fio.appendFile(seqPath, content)

    # adding the proteins from the gene family into the fasta file
    folders = os.listdir(famPath)
    for folder in folders:
        sequencePath = os.path.join(famPath, folder, "g4", "g4_seq.txt")
        seqs = fio.processSeqFile(sequencePath)

        for i in range(len(seqs)):
            proteinName = folder + "_" + str(i)
            taxaName = "testTaxa"
            content = fio.toFASTA(proteinName, taxaName, seqs[i])
            fio.appendFile(seqPath, content)


def main(name):
    fusedPath = os.path.join(conf.generatedFolder, name, conf.fusedFolder)
    # processedPath=os.path.join(conf.generatedFolder, name, conf.processedFolder)
    includeAll = conf.includeAll
    famPath = os.path.join(conf.generatedFolder, name, conf.famFolder)
    processFusedGenes(name, fusedPath, famPath, includeAll)


if __name__ == "__main__":
    main()
