import os
import re
import argparse


print("Veuillez saisir un nom de domaine, nom d'utilisateur ou adresse e-mail... ==> ")
donnee=input()

regex_domaine = "^((?!-)[A-Za-z0-9-]" +"{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
regex_username="^[A-Za-z_][A-Za-z0-9_]*$"
regex_email='\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'

if re.search(regex_domaine, donnee): 
    
    #####Cas 1: de saisie d'un nom de domaine####
    
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
    
    ####Fin Cas1####
if re.search(regex_username, donnee):
    ####Cas 1: Saise d'un nom d'utilisateur####
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
    

if re.search(regex_email, donnee):
    os.chdir(os.getcwd()+'/spiderfoot')
    os.system("python3 ./sf.py -m sfp_spider,sfp_names,sfp_email,sfp_hunter -s "+donnee+" -q -F HUMAN_NAME,EMAILADDR,PHONE_NUMB")
    os.chdir('..')