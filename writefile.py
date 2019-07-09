import os
files = [f for f in os.listdir('first') if not f.startswith('.')]
replacements = {'<center':'!!!\n<center', '</center>':'</center>\n!!!'}
for f in files:
    lines = []
    with open("./first/"+f) as infile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            lines.append(line)
    with open("./first/"+f, 'w') as outfile:
        for line in lines:
            outfile.write(line)
