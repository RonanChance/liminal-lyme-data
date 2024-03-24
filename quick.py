import fileinput

file = fileinput.input('./txts/medications.txt')

for line in file:
    line = line.strip().split(',')
    line[0] = line[0].lower()
    line[0] = line[0][0].upper() + line[0][1:]
    print(",".join(line))