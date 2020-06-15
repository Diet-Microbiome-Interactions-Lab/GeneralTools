#!/bin/bash

# Read in a multi-fasta file and split into n files, all labeled according to ident line

while read line
do
    if [[ ${line:0:1} == '>' ]]
    then
        outfile=${line#>}.fa
        echo $line > $outfile
    else
        echo $line >> $outfile
    fi
done < $1
