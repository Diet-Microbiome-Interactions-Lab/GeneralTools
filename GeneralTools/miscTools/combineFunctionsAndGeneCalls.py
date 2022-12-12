'''
'''


def parseFunctions(function_file):
    functions = {}
    with open(function_file) as file:
        next(file)
        line = file.readline().strip()
        while line:
            values = line.split('\t')
            assert len(values) == 5, f'Invalid number of fields: {len(values)}'
            gene, source, accession, fx, evalue = values
            functions.setdefault(gene, {})
            functions[gene][source] = [fx, evalue]
            line = file.readline().strip()
    return functions


def createAttributeLine(gene, functions):
    annotations = ['FigFams', 'KEGG_Module', 'COG20_PATHWAY', 'TIGRFAM',
                   'KOfam', 'KEGG_Class', 'Transfer_RNAs', 'COG20_FUNCTION',
                   'Pfam', 'COG20_CATEGORY']
    all_values = [f'Locus={gene};']

    if gene in functions:
        for annotation in annotations:
            try:
                description = functions[gene][annotation][0]
                evalue = functions[gene][annotation][1]
            except KeyError:
                description = 'Not_Annotated'
                evalue = '0'
            current_value = '='.join([annotation, description])
            current_evalue = '='.join([annotation, evalue])
            current_line = ';'.join([current_value, current_evalue])
            all_values.append(current_line)
    else:
        for annotation in annotations:
            current_value = '='.join([annotation, 'Not_Annotated'])
            current_evalue = '='.join([annotation, '0'])
            current_line = ';'.join([current_value, current_evalue])
            all_values.append(current_line)
    return ';'.join(all_values)


def parseCalls(call_file, function_file, output_file):
    functions = parseFunctions(function_file)
    calls = {}
    with open(output_file, 'w') as output:
        output.write(f"#gff3 - DaneDeemer - combineFunctionsAndGeneCalls.py\n")
        with open(call_file) as file:
            next(file)
            line = file.readline().strip()
            while line:
                values = line.split('\t')
                assert len(
                    values) == 10, f'Invalid number of fields: {len(values)}'
                gene, contig, start, stop, direction, partial = values[0:6]
                if direction == 'f':
                    direction = '+'
                elif direction == 'r':
                    direction = '-'
                else:
                    pass
                attributes = createAttributeLine(gene, functions)
                write_values = [contig, 'prodigal', 'cds', start,
                                stop, '0', direction, partial, attributes]
                writeline = '\t'.join(write_values) + '\n'
                output.write(writeline)
                line = file.readline().strip()
    return calls


parseCalls('100_Roseburia_hominis-P-GCA_003390885.1.gff',
           '100_Roseburia_hominis-P-GCA_003390885.1.gff3',
           '100_test_output.gff3')
