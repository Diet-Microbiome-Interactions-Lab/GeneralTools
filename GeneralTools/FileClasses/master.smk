rule Reformat_Fasta:
    input:
        f'{{sample}}.{{extension}}'
    output:
        f'{{sample}}-SIMPLIFIED.{{extension}}'
    log: f'Logs/Reformat_Fasta/{{sample}}.log' 
    group: "Indexing"
    priority: 100
    shell:
        """
        touch {output}
        myProgram --fasta {input}
        """

# A-Simplified.fna
# B-Simplified.fasta




# $ dgt fasta -i MyFile.fasta filter
# $ filtering_progam -i MyFile.fasta -o MyOutput.txt

# $ dgt fasta -i MyFile.fasta annotate
# $ snakemake -s snake.smk MyFile.gff.gz

# MyFile.fna
# <config.yaml> annot_ext: gff3

# $ dgt fasta -i MyFile.fasta
# >> MyFile.fasta.gz
# {MyFile}.fasta.gz

# $ dgt fasta -i MyFile.fna --what-can-i-do?
# > Validates to MyFile.fasta.gz
#     Can run: Reformat_Fasta
#              Filter


# Ran through /Data (type=Fasta)<insert> --> Fasta(data).Validates
# {mydata}.Filter.Trim.Annotate.Compress


rule Unsimplify_Fasta:
    input:
        f'{{sample}}-SIMPLIFIED.fasta'
    output:
        f'{{sample}}-UNSIMPLIFIED.fasta'
    shell:
        """
        touch {output}
        """
