import os
import re
import shutil

print("Veuillez saisir un nom de domaine|nom d'utilisateur|adresse e-mail... ==> ")
donnee=input()


#with open('username_file.txt', 'r+') as f1:
#	lines=f1.readlines()
#	for i,l in enumerate(lines):
#   		if l.startswith("options set SOURCE"):
#   			str=l[i].strip()+donnee
#   			l[i]= str
#	f.seek(0)
#	for line in lines:
#		f.write(line)

#os.system("python3 recon-ng -r username_file.txt ")

str=' '+donnee+'\n'

temp = open('temp', 'w+')
with open('username_file', 'r+') as f:
    for line in f:
        if line.startswith('options set SOURCE'):
            line = line.strip() + str
        temp.write(line)
temp.close()
#shutil.move('temp', 'username_file')
