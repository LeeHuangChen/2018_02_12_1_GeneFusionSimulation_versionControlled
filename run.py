from src import randomFamilies, fusedFamilies, processFusedGenes, fileIO_Includes as fio, blastpAndDataProc
import configuration as conf


def main():
    count = 0  # for printing status of the simulation
    total = len(conf.models) * len(conf.seqLens) * len(conf.numFamilies) * len(conf.numFusionEvents) * len(
        conf.totalEvolutionTimes) * len(conf.numGenerations)

    # generate the logfile
    fio.generateDirectories(conf.outputLogFolder)
    open(conf.outputLogFile, "w")

    # testing though all of the parameters completely
    for model in conf.models:
        for seqLen in conf.seqLens:
            for numFamily in conf.numFamilies:
                for numFusionEvent in conf.numFusionEvents:
                    for totalEvolutionTime in conf.totalEvolutionTimes:
                        for numGeneration in conf.numGenerations:
                            testName = fio.name(model, seqLen, numFamily, numFusionEvent, totalEvolutionTime,
                                                numGeneration)
                            fio.printL("\n=============================")
                            fio.printL("PROGRESS: "+str(int(float(count * 100) / float(total)))+"%")
                            count = count + 1
                            fio.printL("Processing test case: "+testName)
                            fio.printL("  Model: "+model+", SeqLen: "+str(seqLen))
                            fio.printL("  NumFamily: "+str(numFamily)+", NumFusions: "+str(numFusionEvent))
                            fio.printL("  TotalEvolutionTime: "+str(totalEvolutionTime)+", NumGeneration: "+str(numGeneration))
                            fio.printL("=============================")

                            fio.printL(" * Producing random protein families...")
                            randomFamilies.main(testName, model, seqLen, numFamily, numGeneration, totalEvolutionTime)
                            fio.printL(" * Producing fused protein families...")
                            fusedFamilies.main(model, seqLen, numFamily, numFusionEvent, totalEvolutionTime,
                                               numGeneration)
                            fio.printL(" * Processing fused protein data...")
                            processFusedGenes.main(testName)
                            fio.printL(" * Running BlastP all-to-all and data processing for ")
                            fio.printL("   MosaicFinder (by Pierre-Alain Jachiet et al.)...")
                            blastpAndDataProc.main(testName)


if __name__ == "__main__":
    main()
