# GenotypeTable2Fasta.py
# version 1.0
#
# July 23, 2016
#
# Authors: Dominik Geissler & Hai D.T. Nguyen
# Correspondence: geissler_dominik@hotmail.com, hai.nguyen.1984@gmail.com
# Acknowledgements: Benjamin Furman for inspiration 
#
# This script will read in an SNP (single nucleotide polymorphism) genotype table called 
# file1.txt and convert it to a fasta file called file2.fasta.
# 
# Where there is a heterozygous site, the IUPAC code will be used (A/G = R; C/T = Y; etc.)
# Missing and other calls will be substituted with a gap (./. = -; C/* = -; etc.)
#
# The genotype table can have n individuals and the script will output n sequences in 
# a multi fasta file.
# This resulting multi fasta file is useful for genotyping with phylogenetic analysis
#
# REQUIREMENTS
#
# 1. Pandas has to be installed. 
# In Ubuntu, you can install it by typing "sudo apt-get install python-pandas"
# If using MacOS X, you can try this command "sudo easy_install pandas"
#
# 2. Generate a genotype table (file1.txt) from a VCF file with bcftools.  
# First make sure bcftools is installed (https://samtools.github.io/bcftools/)
# This script was tested with bcftools 1.3 (using htslib 1.3)
# 
# The VCF file tested was generated by GATK 3.6 (https://www.broadinstitute.org/gatk/).
# First use HaplotypeCaller on each sample or individual with the flag -ERC GVCF to
# generate one GVCF file per sample or individual.
#
# Then merge the GVCF files into a single VCF file with GenotypeGVCFs
#
# java -jar GenomeAnalysisTK.jar -T GenotypeGVCFs \
# -R reference_genome.fasta \
# -V individual_1.haplotypecaller.vcf \
# -V individual_2.haplotypecaller.vcf \
# -V individual_3.haplotypecaller.vcf \
# -V individual_4.haplotypecaller.vcf \
# -o all_individuals.joint.haplotypecaller.vcf
#
# Then select out the SNP's using SelectVariants
#
# java -jar GenomeAnalysisTK.jar -T SelectVariants \
# -R reference_genome.fasta \
# -V all_individuals.joint.haplotypecaller.vcf \
# -selectType SNP \
# -o all_individuals.joint.haplotypecaller.snps.vcf
#
# Optional: filter out false positives with manual filtering or other methods recommended
# by the makers of GATK
#
# Then process the final VCF file and run bcftools index:
#
# bgzip all_individuals.joint.haplotypecaller.snps.vcf
# bcftools index all_individuals.joint.haplotypecaller.snps.vcf.gz
#
# Output the table called file1.txt with this command:
#
# bcftools view all_individuals.joint.haplotypecaller.snps.vcf.gz | bcftools query -f '[%TGT\t]\n' > file1.txt
#
# Make sure this script and file1.txt are in the same folder. Then execute the script by typing:
#
# python GenotypeTable2Fasta.py
#

#import pandas as pd
from pandas import DataFrame
import csv
import os

path = 'file1.txt'	#name of input file
data0 = list(csv.reader(open(path, 'r'), delimiter='\t'))
data = DataFrame(data0)
#data = data.drop(4,axis=1) #this removes the 4th column because it starts with a tab

#replacing
ep0 = [['T/A', 'W'],['A/T', 'W'],['C/G', 'S'],['G/C', 'S'],['A/G', 'R'],['G/A', 'R'],['A/C', 'M'],['C/A', 'M'],['G/T', 'K'],['T/G', 'K']]
ep1 =[['C/T', 'Y'],['T/C', 'Y'],['G/*', '-'],['A/*', '-'],['C/*', '-'],['T/*', '-'],['G/G', 'G'],['A/A', 'A'],['C/C', 'C'],['T/T', 'T'],['./.', '-']]
ep2 = ep0+ep1
for x in ep2:
	data = data.replace(x[0],x[1])

##outputs
pp = 'file2.fasta'	#name of output file
data = data.transpose()
ff = open(pp,'w')
n = 0
for row in data.iterrows():
	tmp = list(row[:][1])
	tmp2= ''.join(tmp)
	if tmp2 != '':	#skip over empty columns
		n += 1
		ff.write('>individual_'+str(n)+'\n') #>individual_1
		ff.write(tmp2+'\n')
ff.close()
