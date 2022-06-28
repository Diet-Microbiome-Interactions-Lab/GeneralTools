header = True
with open('z') as _file:
    if header:
        next(_file)
    lines = _file.readlines()

print(lines)

mydic = {val.split('\t')[0]: val.split('\t')[1].strip() for val in lines}
print(mydic)
