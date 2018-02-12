#!/bin/sh
from subprocess import call
import subprocess
import sys
import os
import random
import fileIO_Includes as fio
import configuration as conf

def random_AA_seq(length):
	seq=''.join(random.choice('ACDEFGHIKLMNPQRSTVWY') for i in range(length))
	#return "TaxonA "+seq
	return seq

#Generate the trees required for random families, since we need to keep track of the sequences of the generations, we are only making binary tree of depth 1
def generateTree(path,seqs,seqLen,branchL):
	f=open(path,"w")
	f.write(str(len(seqs))+" "+str(seqLen)+"\n")
	for i in range(len(seqs)):
		seq=seqs[i]
		f.write("Ancester"+str(i)+" "+seq+"\n")
	f.write("1\n(Taxon1:"+str(branchL)+",Taxon2:"+str(branchL)+");")
	f.close()


#main functions
def GenerateRandomFamilies(famPath, model, seqLen, numFamilies, numGenerations, TotalEvolutionTime):
	#directories
	#randomFamilies="RandomFamilies/"
	randomFamilies=famPath

	#parameters
	# numFamilies=4
	# numGenerations=5
	# TotalEvolutionTime=2
	# seqLen=1000
	# model="-mjtt"

	#calculated parameters
	branchLen=float(TotalEvolutionTime)/float(numGenerations)

	#generate directories
	fio.generateDirectories(randomFamilies)
	# if not os.path.exists(randomFamilies):
	# 	os.mkdir(randomFamilies)

	#generate random ancestrial sequences and the initial tree for the families
	for i in range(numFamilies):
		#create the family path
		familyPath=os.path.join(randomFamilies,"f"+str(i))
		fio.testPath(familyPath)

		#generate random ancestrial sequences and the initial tree
		#generateTree(os.path.join(familyPath,"f"+str(i)+"_g0.tree"),random_AA_seq(seqLen),branchLen)

		#generate trees and sequences for each subsequent generations
		for j in range(numGenerations):
			#define all the paths needed
			generationPath=os.path.join(familyPath,"g"+str(j))
			fio.testPath(generationPath)

			treePath=os.path.join(generationPath,"f"+str(i)+"_g"+str(j)+".tree")
			sequencePath=os.path.join(generationPath,"g"+str(j)+"_seq.txt")
			logPath=os.path.join(generationPath,"g"+str(j)+"_log.txt")
			fio.createEmptyFiles([sequencePath,logPath])

			sequences=[]
			#first generation is generated randomly
			if j==0:
				#generate the tree file for Seq-Gen
				sequences.append(random_AA_seq(seqLen))
				
				
			else:
				#then there exist a sequence file in the previous generation
				prevGenSeqPath=os.path.join(familyPath,"g"+str(j-1),"g"+str(j-1)+"_seq.txt")
				seqs=fio.processSeqFile(prevGenSeqPath)
				for seq in seqs:
					sequences.append(seq)
			


			generateTree(treePath,sequences,seqLen,branchLen)

			
			#generate the tree file for Seq-Gen
			#generateTree(treePath,random_AA_seq(seqLen),branchLen)
		
			for k in range(1,len(sequences)+1):
				#custom code for my linux/windows setup
				seqGenURL=""
				if sys.platform=="linux2":
					seqGenURL="./Seq-Gen_linux/source/seq-gen"
				else: #windows version
					seqGenURL="./Seq-Gen/source/seq-gen"

				#seq-gen command
				cmd=[seqGenURL,model,"-l",str(seqLen),"-k",str(k)]
				
				seq_gen_proc=subprocess.Popen(cmd, stdin=open(treePath,"r"),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

				dataset, log = seq_gen_proc.communicate()

			
				# seq-gen does not exit with an error code when it fails.  I don't know why!!
				if seq_gen_proc.returncode != 0 or len(dataset) == 0:
					sys.exit('seq-gen failed! Family:'+str(i)+',Generation:'+str(j)+",Ancester (k):"+str(k)+'\n')
				fio.appendFile(sequencePath,dataset)
				fio.appendFile(logPath,log)

def main(name, model, seqLen, numFamilies, numGenerations, TotalEvolutionTime):
	#configuration pulled from the configuration file
	#parameters
	famPath=os.path.join(conf.generatedFolder, name, conf.famFolder)
	# numFamilies=conf.numFamilies
	# numGenerations=conf.numGenerations
	# TotalEvolutionTime=conf.TotalEvolutionTime
	# seqLen=conf.seqLen
	# model=conf.model



	GenerateRandomFamilies(famPath, model, seqLen, numFamilies, numGenerations, TotalEvolutionTime)
if __name__=="__main__":
	main()