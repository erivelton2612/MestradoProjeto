from gurobipy import *
import estdados
import progressbar 
from time import sleep

#-------------Criação de Variáveis

def variables(model,d,v):
	#estoque
	v.I_jt = model.addVars(d.J,d.T+1,vtype=GRB.CONTINUOUS,lb=0.0)		
	#producao
	v.Q_jtk = model.addVars(d.J,d.T,d.M,vtype=GRB.CONTINUOUS,lb=0.0)		
	#setup
	v.Y_jtk = model.addVars(d.J,d.T, d.M,vtype=GRB.BINARY,lb=0.0)	
	model.update()

#-------------Criação da FO

def cost_function(model,d,v):
	
	bar = progressbar.ProgressBar(maxval=d.J, \
    widgets=[progressbar.Bar('=', '\n[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	inventory = 0
# 	for j in range(d.J):
# 		inventory += v.I_jt[j,0] * 10000000000
# 		for t in range(d.T):
#  			inventory += v.I_jt[j,t+1] #* d.h_j[j] 

	inventory = sum(v.I_jt[j,t+1] * d.h_j[j]
 				 for j in range(d.J) for t in range(d.T))
 	
	setup=0
	for j in range(d.J): 
		bar.update(j+1)
		sleep(0.1)
		for t in range(d.T): 
			for k in range(d.M):
				setup += v.Y_jtk[j,t,k] * d.cs_jk [j,k] *100
				
	bar.finish()
	
	total = inventory + setup
	model.setObjective(total, GRB.MINIMIZE)
	model.update()

#-------------Criação de Restrições

def constraints(model, d, v):
	#INDICES DO ESTOQUE JOGADOS 1 PRA FRENTE
		#0 = ESTOQUE NO FINAL DE 0 USADO EM 1
		#1 = ESTOQUE NO FINAL DE 1
		#d.T = ESTOQUE NO FINAL DE TUDO QUE VAI SER ZERO

	#Estoque inicial produto
	for j in range(d.J):
		model.addConstr(v.I_jt[j,0] == d.stk_j[j]) #iniciar como varial
# 		model.addConstr(v.I_jt[j,0] >= d.stk_j[j]) #iniciar como varial

	#Fluxo de estoque produto
	bar = progressbar.ProgressBar(maxval=d.J, \
    widgets=[progressbar.Bar('=', '\n[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	print("Fluxo de estoque em andamento")
	
	for j in range(d.J):
		bar.update(j+1)
		sleep(0.1)
		for t in range(d.T):
			lhs = v.I_jt[j,t]
			#Melhoria aplicada selecionando apenas as colunas que possuem valor no item j
			for k in d.b_jk[j,:].nonzero()[1]:
# 			for k in range(d.M):
				lhs += v.Q_jtk[j,t,k] 
				
			rhs = d.d_jt[j,t] + v.I_jt[j,t+1]
			#Melhoria aplicada selecionando apenas as colunas que possuem valor no item j
			for i in d.S_j[j,:].nonzero()[1]:
# 			for i in range(d.J):
				for k in d.b_jk[i,:].nonzero()[1]:	
# 				for k in range(d.M):
					rhs += d.S_j[j,i] * v.Q_jtk[i,t,k] 
				
			model.addConstr(lhs == rhs)
	bar.finish()
			
			
	#Capacidade
	print("Capacidade em andamento")
	bar = progressbar.ProgressBar(maxval=d.M, \
    widgets=[progressbar.Bar('=', '\n[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	for k in range(d.M):
		bar.update(k+1)
		sleep(0.1)
		for t in range(d.T):
			usage = 0
			for j in d.b_jk[:,k].nonzero()[0]:
				usage += d.b_jk[j,k] * v.Q_jtk[j,t,k] + d.s_jk[j,k]*v.Y_jtk[j,t,k]
			model.addConstr(usage <= d.cap_kt[k][t])
	bar.finish()
	
	#Setup
	print("Setup em andamento")
	bar = progressbar.ProgressBar(maxval=d.J, \
    widgets=[progressbar.Bar('=', '\n[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	
	for j in range(d.J):
		bar.update(k+1)
		sleep(0.1)
		for t in range(d.T):
			for k in range(d.M):
				#model.addConstr(v.Q_jtk[j,t,k] <= d.beta[j][t]*v.Y_jtk[j,t,k])
				model.addConstr(v.Q_jtk[j,t,k] <= 100000*v.Y_jtk[j,t,k])
	bar.finish()

	model.update()

def printsolution(argv,model,d,v):
	print("Print da solução em andamento")
	
	
	solt = open(str(argv[0])+".txt","w") 

	solt.write("Solucao\tGap\tTempo\tStatus Gurobi\n")
	solt.write(str(round(model.objVAl))+"\t"+str(round(100*model.MIPGap,2))+"\t")
	solt.write(str(round(model.Runtime,2))+"\t"+str(model.Status)+"\n")


	inv_prod = sum(v.I_jt[j,t+1].X#*d.h_j[j] 
				for j in range(d.J) for t in range(d.T))
	setup = sum(v.Y_jtk[j,t,k].X#*d.cs_jk[j,k]
			 *100 for j in range(d.J) for t in range(d.T) for k in range(d.M))

	solt.write("Custos\nEstoque\tSetup\n")
	solt.write(str(round(inv_prod))+"\t"+str(round(setup))+"\n")

	solt.write("J\tT\tM\n")
	solt.write(str(d.J)+"\t"+str(d.T)+"\t"+str(d.M)+"\n\n")
	
	solt.write("Ocupacao de Maquinas Por Periodo\n")
	
	for k in range(d.M):
		for t in range(d.T):
			a = 0
			for j in range(d.J):
				a += d.b_jk[j,k] * v.Q_jtk[j,t,k].X + d.s_jk[j,k]*v.Y_jtk[j,t,k].X
						
			a = a/d.cap_kt[k][t]
			solt.write(str(round(100*a,2))+"\t")
		solt.write("\n")
	solt.write("\n")

	solt.write("Custos Estoque Por Periodo\n")
	for t in range(d.T):
		a = sum(v.I_jt[j,t+1].X#*d.h_j[j] 
		  for j in range(d.J))
		solt.write(str(round(a))+"\t")
	solt.write("\n\n")
	

	solt.write("Item\tT\tMaq\tProd\tInv\tDem E\tDem I\n")
	for j in range(d.J):
		for t in range(d.T):
			for k in range(d.M):
				a += sum(d.S_j[j,i]*v.Q_jtk[i,t,k].X  for i in range(d.J) #if type(d.S_j[j,i]) == float
			 )
				solt.write(
						str(j+1)+"\t"+
						str(t+1)+"\t"+
						str(k+1)+"\t"+
						str(round(v.Q_jtk[j,t,k].X))+"\t"+
						str(round(v.I_jt[j,t+1].X))+"\t"+
						str(round(d.d_jt[j,t]))+"\t"+
						str(round(a))+"\n")
		solt.write("\n")

	solt.close()

