def gcContent(string):
    """
    Function to be used inside of 'read_fasta' in order to obtain
    gcContentent of a string
    """
    string = string.upper()
    g = string.count('G')
    c = string.count('C')
    return round((g + c) / len(string), 3)
