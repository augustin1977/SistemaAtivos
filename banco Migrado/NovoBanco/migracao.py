import pandas as pd
import datetime
import cv2
import os
# instalar pandas e openpyxl para funcionar esse codigo
# não esquecer de alterar notas para ocorrencias em todo sistema
def run():

	df = pd.read_excel('planilha_mestra_ativos_2.0v.exp.xlsm', sheet_name='input')
	df = df.fillna(0)

	tipos_variavel = {'Lab':str, 'Predio':int, 'Sala':str, 'DetalheLocal':str, 'NomeEq':str, 'Apelido':str, 'Tipo':str, 'Cod_auto_raster':str, 'Fabricante':str,
						'Moeda':str, 'Custo de aquisição':float, 'Agência financiadora':str, 'ID_grupo':str, 'Responsável':str, 'Potência elétrica':str, 
						'Unidade potencia elétrica':str,'Tensão elétrica minima (V)':int, 'Tensão elétrica máxima (V)':int,
						'Detalhe da alimentação elétrica (bivolt, trifásico, etc)':str, 'Outras alimentações (ar, água, etc)':str, 'Modelo':str, 
						'Spec1':str, 'Unidade Spec1':str, 'Spec2':str, 'Unidade Spec2':str, 'Nacionalidade':str, 'Ano_compra':str, 'Projeto_financiador':str, 
						'Sist_patrimonio':str, 'Patrimonio':str, 'Finalidade':str, 'inter_calib':str, 'Condição Equipamento':str,
						'Data Atualização':str, 'Pasta_arquivos':str, 'OBS':str, 'Unnamed: 36':str, 'endereço':str}
	df = df.astype(tipos_variavel)	
	array_dados = df.values
	nomes_cabecalho = df.columns.tolist()
	#montando dados em dicionario a partir da planilha
	dados=[]
	for linha in array_dados:
		dado={}
		for k,j in enumerate(nomes_cabecalho):
			dado[j]=linha[k]
		dados.append(dado)
	
	# montando banco de dados
	banco_dados={}
	banco_dados['tipo']={}
	banco_dados['equipamento']={}
	banco_dados['fabricante']={}
	banco_dados['local']={}

	for registro in dados:
		arquivo=registro['Pasta_arquivos']
		if registro['Tipo'] not in banco_dados['tipo']:
			banco_dados['tipo'][registro['Tipo']]=len(banco_dados['tipo'])
		if registro['Fabricante'] not in banco_dados['fabricante']:
			banco_dados['fabricante'][registro['Fabricante']]=len(banco_dados['fabricante'])
		local=f"{registro['Lab']}.{registro['Predio']}.{registro['Sala']}"
		if local not in banco_dados['local']:
			banco_dados['local'][local]=len(banco_dados['fabricante'])
		codigo=registro['Tipo'][0:3]
		
		
		# ~ pastaAtual=os.getcwd()
		# ~ novaPasta=os.path.join(pastaAtual,"arquivos",arquivo)
		# ~ if os.path.isdir(novaPasta):
			# ~ arquivos=os.listdir(novaPasta)
	return banco_dados	
		
print(run())
