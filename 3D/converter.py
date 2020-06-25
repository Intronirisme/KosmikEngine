path = input('fichier à convertir ? : ')
outFile = input('fichier de sortie ? : ')
file = []
with open(path, 'r') as modelFile:
	for ligne in modelFile:
		file.append(ligne[:-1])
for ligne in file:
	if ligne.find('//') != -1
		while ligne.find
