import os

def entrada(): 

	arquivo = open('instance_9.bpk', 'r')

	for linha in arquivo:
		t1,t2 = linha.split()
		print("bloco:", t1 ,"- peso:", t2)
	
	arquivo.close()

entrada()

os.system("pause")