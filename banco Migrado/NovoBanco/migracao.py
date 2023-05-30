import pandas as pd
import datetime
# instalar pandas e openpyxl para funcionar esse codigo

def pandas_to_dic(linha,cabecalho):
	dado={}
	for k,j in enumerate(cabecalho):
		dado[j]=linha[k]
	return dado
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
dados=[]
for i in array_dados:
	dados.append(pandas_to_dic(i,nomes_cabecalho))

for i,linha in enumerate(dados):
	for j,campo in enumerate(linha):

		if linha[campo]=="- ":
			print(i,j)
	
