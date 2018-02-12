import os
import configuration as conf
import subprocess
from src import fileIO_Includes as fio
from Bio import SeqIO


def generateProtLenInfo(sequenceFolder, filename):
    seqs = SeqIO.parse(os.path.join(sequenceFolder, filename), "fasta")
    protLenDict = {}
    for seq in seqs:
        protName = seq.description.split("[")[0].strip()
        protLenDict[protName] = len(seq)

    fio.generateDirectories(conf.protLenFolder)
    protLenFileDir = os.path.join(conf.protLenFolder, filename.replace(".fasta", ".txt"))
    with open(protLenFileDir, "w") as f:
        f.write("protein\tlength\n")
        prots = protLenDict.keys()
        prots.sort()
        for protName in prots:
            f.write(protName+"\t"+str(protLenDict[protName])+"\n")


def generateReorderedFileFromBlastResults(infilepath, outfilepath):
    outfile = open(outfilepath, "w")
    hline = "qseqid\tsseqid\tevalue\tpident\tlength\tgaps\tsstart\tsend\tqstart\tqend\n"
    outfile.write(hline)

    infile = open(infilepath, "r")
    content = infile.read()
    infile.close()

    lines = content.split("\n")

    for line in lines:
        if (len(line) > 0):
            arr = line.split("\t")
            # newline="Gi|"+arr[0].split("F")[0]+"|"+"\t"+"Gi|"+arr[1].split("F")[0]+"|"+"\t"+arr[10]+"\t"+arr[2]+"\t"+arr[3]+"\t"+arr[5]+"\t"+arr[8]+"\t"+arr[9]+"\t"+arr[6]+"\t"+arr[7]+"\n"
            newline = arr[0] + "\t" + arr[1] + "\t" + arr[10] + "\t" + arr[2] + "\t" + arr[3] + "\t" + arr[5] + "\t" + \
                      arr[8] + "\t" + arr[9] + "\t" + arr[6] + "\t" + arr[7] + "\n"
            outfile.write(newline)
    outfile.close()


def makeblastdb(seqFolder, filename):
    seqPath = os.path.join(seqFolder, filename)
    dbPath = os.path.join(conf.blastDBFolder, filename)
    cmd = ["makeblastdb", "-in", seqPath, "-dbtype", "prot", "-out", dbPath]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data, log = proc.communicate()

    logDir = os.path.join(conf.logFolder, filename.replace(".fasta", "") + "makeblastdb_log.txt")
    with open(logDir, "w") as f:
        f.write(data + "\n" + log)


def alltoallBlastP(filename, outpath, outfmt=6, num_threads=1):
    cmd = ["blastp", "-db", os.path.join(conf.blastDBFolder, filename),
           "-query", os.path.join(conf.sequenceFolder, filename),
           "-outfmt", str(outfmt), "-out", outpath, "-num_threads", str(num_threads)]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data, log = proc.communicate()

    f = open(os.path.join(conf.logFolder, filename.replace(".fasta", "") + "blastp_log.txt"), "w")
    f.write(data + "\n" + log)
    f.close()


def main(name):
    filename = name + ".fasta"
    outfilename = name + ".csv"
    processedOutfilename = name + "_proc.csv"

    resultPath = conf.resultFolder
    procResultPath = conf.processedResultFolder
    fio.generateDirectoriesMult([resultPath, procResultPath, conf.allToAllFolder, conf.logFolder, conf.blastDBFolder])

    generateProtLenInfo(conf.sequenceFolder, filename)
    makeblastdb(conf.sequenceFolder, filename)
    alltoallBlastP(filename, os.path.join(conf.allToAllFolder, outfilename))

    generateReorderedFileFromBlastResults(os.path.join(resultPath, outfilename),
                                          os.path.join(procResultPath, processedOutfilename))


if __name__ == "__main__":
    main()
