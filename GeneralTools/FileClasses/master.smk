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


rule run_Metaspades:
    input:
        {sample}.txt
    output:
        {sample}.tkn
    params:
        threads=4,
        mem="10Gb"
    shell:
        """
        metaspades.py --mode meta --threads 4 --mem {params.mem} --input {input} --output {output}
        """


$ snakemake -s snake.smk file1.tkn



rule Unsimplify_Fasta:
    input:
        f'{{sample}}-SIMPLIFIED.fasta'
    output:
        f'{{sample}}-UNSIMPLIFIED.fasta'
    shell:
        """
        touch {output}
        """
