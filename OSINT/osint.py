import argparse

import os
import sys
import re


my_parser = argparse.ArgumentParser(description='Automatisation des outils OSINT')

my_parser.add_argument('-u', metavar='Nom d\'utilisateur', type=str, help='Le nom d\'utilisateur de scan')
my_parser.add_argument('-d', metavar='Nom de domaine', type=str, help='Nom de domaine de scan')
my_parser.add_argument('-e', metavar='Adresse email',type=str, help='Adresse email de scan')

args=my_parser.parse_args()


regex_domaine = "^((?!-)[A-Za-z0-9-]" +"{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
regex_username="^[A-Za-z_][A-Za-z0-9_]*$"
regex_email='\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'

if args.d:
    donnee=args.d
    if not re.search(regex_domaine, donnee):
        print('Le nom de domaine saisie est incorect.\nLe nom de domaine doit etre sous la forme : <domaine>.<dz,com,net,org,...>')
    else : 
        os.chdir(os.getcwd()+'/metagoofil')
        os.system("python3 metagoofil.py -d "+donnee+" -t pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx -o MetagoofilResults") 
        os.chdir('..')
        os.chdir(os.getcwd()+'/theHarvester')
        os.system("python3 theHarvester.py -d "+donnee+" -g -p -s --screenshot theHarvesterSSResults -v -f theHarvesterResults -b all")
        os.chdir('..')
        os.chdir(os.getcwd()+'/spiderfoot')
        os.system("python3 ./sf.py -m sfp_spider,sfp_names,sfp_email,sfp_phone -s "+donnee+" -q -F HUMAN_NAME,EMAILADDR,PHONE_NUMB")
        os.chdir('..')
        os.chdir(os.getcwd()+'/recon-ng')
        str=' '+donnee+'\n'
        temp = open('temp1.txt', "w+")
        with open('domain_file', 'r') as f:
            for line in f:
                if line.startswith('options set SOURCE'):line = line.strip() + str
                temp.write(line)
        temp.close()
        #shutil.move('temp.txt', 'username_file.txt')
        os.system("python3 recon-ng -r temp1.txt")
        os.chdir('..')
    
if args.u:
    donnee=args.u
    if not re.search(regex_username, donnee):
        print('Le nom d\'utilisateur saisie est incorrect.\nUn nom d\'utilisateur doit commencer un caractere et ne contient pas les symboles.')
    else:
        os.chdir(os.getcwd()+'/spiderfoot')
    os.system("python3 ./sf.py -m sfp_spider,sfp_accounts -s \""+donnee+"\" -q -n")
    os.chdir('..')
    os.chdir(os.getcwd()+'/sherlock')
    #print(os.getcwd())
    os.system("python3 sherlock "+donnee+" -o SherlockResults ")
    os.chdir('..')
    os.chdir(os.getcwd()+'/recon-ng')
    str=' '+donnee+'\n'
    temp = open('temp.txt', "w+")
    with open('username_file', 'r') as f:
        for line in f:
            if line.startswith('options set SOURCE'):line = line.strip() + str
            temp.write(line)
    temp.close()
    #shutil.move('temp.txt', 'username_file.txt')
    os.system("python3 recon-ng -r temp.txt")
    os.chdir('..')
    
if args.e:
    donnee=args.e
    if not re.search(regex_email, donnee):
        print('L\'adresse email saisie est incorrecte.\nL\'adresse email doit etre sur la forme Abc123_@example.com')
    else:
        os.chdir(os.getcwd()+'/spiderfoot')
    os.system("python3 ./sf.py -m sfp_spider,sfp_crawlr,sfp_format,sfp_email,sfp_hunter -s "+donnee+" -q -F HUMAN_NAME,EMAILADDR,PHONE_NUMB")
    os.chdir('..')