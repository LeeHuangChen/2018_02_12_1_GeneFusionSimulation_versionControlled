from src import randomFamilies, fusedFamilies, processFusedGenes, fileIO_Includes as fio, blastpAndDataProc
import configuration as conf


def main():
    count = 0  # for printing status of the simulation
    total = len(conf.models) * len(conf.seqLens) * len(conf.numFamilies) * len(conf.numFusionEvents) * len(
        conf.totalEvolutionTimes) * len(conf.numGenerations)
    # testing though all of the parameters completely
    for model in conf.models:
        for seqLen in conf.seqLens:
            for numFamily in conf.numFamilies:
                for numFusionEvent in conf.numFusionEvents:
                    for totalEvolutionTime in conf.totalEvolutionTimes:
                        for numGeneration in conf.numGenerations:
                            testName = fio.name(model, seqLen, numFamily, numFusionEvent, totalEvolutionTime,
                                                numGeneration)
                            print "\n============================="
                            print "PROGRESS: ", int(float(count * 100) / float(total)), "%"
                            count = count + 1
                            print "Processing test case:", testName
                            print "  Model:", model, ", SeqLen:", seqLen
                            print "  NumFamily: ", numFamily, ", NumFusions:", numFusionEvent
                            print "  TotalEvolutionTime:", totalEvolutionTime, ", NumGeneration:", numGeneration
                            print "============================="
                            print " * Producing random protein families..."
                            randomFamilies.main(testName, model, seqLen, numFamily, numGeneration, totalEvolutionTime)
                            print " * Producing fused protein families..."
                            fusedFamilies.main(model, seqLen, numFamily, numFusionEvent, totalEvolutionTime,
                                               numGeneration)
                            print " * Processing fused protein data..."
                            processFusedGenes.main(testName)
                            print " * Running BlastP all-to-all and data processing for MosaicFinder (by Pierre-Alain Jachiet et al.)..."
                            blastpAndDataProc.main(testName)


if __name__ == "__main__":
    main()
