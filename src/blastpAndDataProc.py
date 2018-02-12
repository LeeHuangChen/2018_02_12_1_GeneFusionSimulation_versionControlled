import os
import configuration as conf
import subprocess
from src import fileIO_Includes as fio

infilename = "fam.csv"
outfilename = "famh.csv"


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


def makeblastdb(processedPath, filename):
    cmd = ["makeblastdb", "-in", os.path.join(processedPath, filename), "-dbtype", "prot"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data, log = proc.communicate()

    f = open(os.path.join(processedPath, filename.replace(".fasta", "") + "makeblastdb_log.txt"), "w")
    f.write(data + "\n" + log)
    f.close()


def alltoallBlastP(processedPath, filename, outpath, outfmt=6, num_threads=4):
    cmd = ["blastp", "-db", os.path.join(processedPath, filename), "-query", os.path.join(processedPath, filename),
           "-outfmt", str(outfmt), "-out", outpath, "-num_threads", str(num_threads)]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data, log = proc.communicate()

    f = open(os.path.join(processedPath, filename.replace(".fasta", "") + "blastp_log.txt"), "w")
    f.write(data + "\n" + log)
    f.close()


def main(name):
    # processedPath=conf.processedPath
    processedPath = os.path.join(conf.resultFolder, conf.processedFolder)
    filename = name + ".fasta"
    # outfilename=conf.blastpOutfilename
    outfilename = name + ".csv"
    # processedOutfilename=conf.blastpOutfilename_processed
    processedOutfilename = name + "_proc.csv"

    resultPath = conf.resultFolder
    procResultPath = conf.processedResultFolder
    fio.generateDirectoriesMult([resultPath, procResultPath])

    makeblastdb(processedPath, filename)
    alltoallBlastP(processedPath, filename, os.path.join(resultPath, outfilename))

    generateReorderedFileFromBlastResults(os.path.join(resultPath, outfilename),
                                          os.path.join(procResultPath, processedOutfilename))


if __name__ == "__main__":
    main()
