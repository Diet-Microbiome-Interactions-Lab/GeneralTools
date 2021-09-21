# import os
# import sys


# '''
# Three different categories:
# Early/Late
# Particle/Supernatant
# Small/Medium/Large
# 3 separate layers
# '''


# def setup_index():
#     '''
#     '''
#     index = {}
#     index['time'] = {}
#     index['sampling'] = {}
#     index['size'] = {}

#     index['time']['24'] = list(range(8, 22))
#     index['time']['48'] = list(range(22, 36))
#     index['sampling']['particle'] = list(range(15, 22)) + list(range(29, 36))
#     index['sampling']['supernatant'] = list(range(8, 15)) + list(range(22, 29))
#     index['size']['small'] = [8, 9, 15, 16, 22, 23, 29, 30]
#     index['size']['medium'] = [10, 11, 17, 18, 24, 25, 31, 32]
#     index['size']['large'] = [12, 13, 14, 19, 20, 21, 26, 27, 28, 33, 34, 35]

#     return index


# b = setup_index()
# for key in b.keys():
#     print(key)
#     for val in b[key].keys():
#         print(val)
#         print(len(b[key][val]))


# def test(file):
#     '''
#     '''
#     idx = setup_index()

#     associations = {}

#     with open(file) as f:
#         line = f.readline()   # Skip header
#         line = f.readline().strip()
#         while line:
#             values = line.split('\t')
#             MAG = values[0]
#             # Test a time dependence
#             twentyfour = sum([float(values[i])
#                               for i in idx['time']['24']]) / 14
#             fortyeight = sum([float(values[i])
#                               for i in idx['time']['48']]) / 14
#             if (twentyfour * 0.75) > fortyeight:
#                 associations[MAG] = ['Early']
#             elif (fortyeight * 0.75) > twentyfour:
#                 associations[MAG] = ['Late']
#             else:
#                 associations[MAG] = ['None']

#             # Test a sampling dependence
#             particle = sum([float(values[i])
#                             for i in idx['sampling']['particle']]) / 14
#             supernatant = sum([float(values[i])
#                                for i in idx['sampling']['supernatant']]) / 14
#             if (particle * 0.75) > supernatant:
#                 associations[MAG].append('Particle')
#             elif (supernatant * 0.75) > particle:
#                 associations[MAG].append('Supernatant')
#             else:
#                 associations[MAG].append('None')

#             # Test a size dependence
#             small = sum([float(values[i]) for i in idx['size']['small']]) / 8
#             medium = sum([float(values[i]) for i in idx['size']['medium']]) / 8
#             large = sum([float(values[i]) for i in idx['size']['large']]) / 12
#             print(f"Small: {small}\tMedium: {medium}\tLarge: {large}")
#             if ((small * 0.80) > medium and (small * 0.80) > large):
#                 associations[MAG].append('Small')
#             elif ((medium * 0.80) > small and (medium * 0.80) > large):
#                 associations[MAG].append('Medium')
#             elif ((large * 0.80) > small and (large * 0.80) > medium):
#                 associations[MAG].append('Large')
#             else:
#                 associations[MAG].append('None')

#             line = f.readline().strip()
#     return associations


# os.chdir('/Users/ddeemer/OneDrive - purdue.edu/AshProject/29Mar21')
# a = test('Merged-Bins-Abundances.txt')


# with open('Categories.txt', 'w') as out:
#     for mag in a:
#         writeline = [mag] + a[mag]
#         writeline = '\t'.join(writeline) + '\n'
#         out.write(writeline)


mystring = 'dane.gregory.deemer'

mys = mystring.rsplit('.', 1)[0]
print(mys)
