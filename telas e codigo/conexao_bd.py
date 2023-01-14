
#imports do pyqt5 (parte grafica)
from PyQt5 import  uic,QtWidgets
app=QtWidgets.QApplication([])
import sys


#imports do mysql (banco de dados)
import mysql.connector
bnk = mysql.connector.connect(
	host='localhost',
	user='usuario do workbench',
	passwd='sua senha do workbench',
	database='bd_test'
)
c = bnk.cursor()

#variaveis globais
numero_id= 0


#tela de login***************************************************************************************************************************
#botao que faz logar e ter acesso(ou nao) as outras telas
def logar():
	tela1.lb_editavel.setText("")
	user = tela1.le_usuario.text()
	senha = tela1.le_senha.text()
	try:
		c.execute("SELECT senha FROM funcionarios WHERE user_name ='{}'".format(user))
		senha_bd = c.fetchall()
		
	except:
		print('erro ao validar o login')

	try:
		senha == senha_bd[0][0]
		tela1.close()
		tela2.show()
	
	except:
		tela1.lb_editavel.setText("Dados de login incorretos!")



#tela dashboard************************************************************************************************************************

#botao que escolhe a tela de cadastrar remedio
def ir_cadastro():
	tela2.close()
	tela3.show()

#botao que escolhe a tela de compra
def ir_compra():
	tela2.close()
	tela4.show()


#botao de ir cadastrar funcionario
def ir_funcionario():
	tela2.close()
	tela5.show()

#botao de ir a tela de visualizacao
def ir_visualizar():
	tela2.close()
	tela_listar.show()
#botao de voltar a tela de login (sair)
def voltar_login():
	tela2.close()
	tela1.show()





#TELA CADASTRAR REMEDIO***********************************************************************************************************************

#botao que cadastra o remedio
def cadastrar():

	if tela3.bt_creceita.isChecked():
		acesso = "Com receita"
		
	elif tela3.bt_sreceita.isChecked():
		acesso = "Sem Receita"
	 
	nome = tela3.le_nome.text()
	validade = tela3.le_validade.text()
	quantidade = tela3.le_qtd.text()
	valor = tela3.le_valor.text()


	insertando = f'INSERT INTO tbl_remedios (nome, validade, quantidade, valor, acesso) VALUES ("{nome}", "{validade}", {quantidade}, "{valor}", "{acesso}")'
	
	c.execute(insertando)
	bnk.commit()

	#parte que apaga as lineedit
	tela3.le_nome.setText('')
	tela3.le_qtd.setText('')
	tela3.le_validade.setText('')
	tela3.le_valor.setText('')

	tela3.lb_editavel.setText('Remédio cadastrado!')
#botao que volta para a tela de dashboard(sair)
def voltartela3():
	tela3.close()
	tela2.show()

#TELA COMPRA********************************************************************************************************************************
def registrar():
	if tela4.rb_aprazo.isChecked():
		metodo = "A prazo"
	elif tela4.rb_avista.isChecked():
		metodo = "A vista"
	codigo_remedio = tela4.le_codigo.text()
	quantidade = tela4.le_qtd.text()
	nota = tela4.le_nota.text()

	inserting = f'INSERT INTO registro_vendas (quantidade, metodo, nota, codigo_remedio) VALUES ("{quantidade}", "{metodo}", "{nota}", "{codigo_remedio}")'
	c.execute(inserting)
	bnk.commit()

	tela4.le_codigo.setText('')
	tela4.le_qtd.setText('')
	tela4.le_nota.setText('')

	tela4.lb_editavel.setText("Compra registrada!")
	

	c.execute(f'UPDATE tbl_remedios SET quantidade= quantidade-{quantidade} WHERE id_remedio={codigo_remedio}')
	dados1 = c.fetchall()
	
	bnk.commit()

	tela4.lb_editavel.setText("Registro salvo!")


def ver_registro():
	tela4.close()
	gui_registro.show()



def recarregar_registro():
	comsql = f'SELECT * FROM registro_vendas'
	c.execute(comsql)
	dados_lidos = c.fetchall()

	gui_registro.tableWidget.setRowCount(len(dados_lidos))
	gui_registro.tableWidget.setColumnCount(5)



	for i in range(0, len(dados_lidos)):
		for j in range(0,5):
			gui_registro.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def voltarvr():
	gui_registro.close()
	tela4.show()

#voltar a tela de dashboard(sair)
def voltar_r_d():
	tela4.close()
	tela2.show()










#TELA CADASTRAR FUNCIONARIO*****************************************************************************************************************
#botao cadastrar funcionario
def cadastrar_funcionario():
	nome = tela5.le_nome.text()
	cpf = tela5.le_cpf.text()
	email = tela5.le_email.text()

	user_name = tela5.le_user.text()
	senha = tela5.le_senha.text()
	rsenha = tela5.le_rsenha.text()



	if (senha == rsenha):
		try:
			insert_fun = f'INSERT INTO funcionarios(nome_completo, cpf, email, user_name, senha) VALUES ("{nome}", "{cpf}", "{email}", "{user_name}", "{senha}")'
		


		except mysql.connector.Error as erro:
			tela5.lb_editavel.setText('problema no banco de dados')

		tela5.lb_editavel.setText('usuario cadastrado')		
		c.execute(insert_fun)
		bnk.commit()

	else:
		tela5.lb_editavel.setText('senhas digitadas diferentes')


	tela5.le_nome.setText('')
	tela5.le_cpf.setText('')
	tela5.le_email.setText('')
	tela5.le_user.setText('')
	tela5.le_senha.setText('')
	tela5.le_rsenha.setText('')
def voltar_c_d():
	tela5.close()
	tela2.show()



#TELA DE VISUALIZACAO BD REMEDIOS***********************************************************************************************************
#botao de recarregar refresh
def recarregar():
	comsql = f'SELECT * FROM tbl_remedios'
	c.execute(comsql)
	dados_lidos = c.fetchall()
	print(dados_lidos[0][0])


	tela_listar.tableWidget.setRowCount(len(dados_lidos))
	tela_listar.tableWidget.setColumnCount(6)

	for i in range(0, len(dados_lidos)):
		for j in range(0, 6):
			tela_listar.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

#botao de excluir linha selecionada da tabela
def excluir_dados_rmd():
	row = tela_listar.tableWidget.currentRow()
	tela_listar.tableWidget.removeRow(row)
	c.execute('SELECT id_remedio FROM tbl_remedios')
	dados_lidos = c.fetchall()
	valor_id = dados_lidos[row][0]
	c.execute('DELETE FROM tbl_remedios WHERE id_remedio='+ str(valor_id))
	bnk.commit()
#botao editar linha selecionada da tabela(abre a janela pequena de editar)
def editar_tbl():
	global numero_id
	row = tela_listar.tableWidget.currentRow()

	c.execute('SELECT id_remedio FROM tbl_remedios')
	dados_lidos = c.fetchall()
	valor_id = dados_lidos[row][0]
	c.execute('SELECT * FROM tbl_remedios WHERE id_remedio='+ str(valor_id))
	med = c.fetchall()

	gui_editar.show()
	
	numero_id = valor_id

	gui_editar.le_id.setText(str(med[0][0]))
	gui_editar.le_nome.setText(str(med[0][1]))
	gui_editar.le_validade.setText(str(med[0][2]))
	gui_editar.le_qtd.setText(str(med[0][3]))
	gui_editar.le_valor.setText(str(med[0][4]))
	gui_editar.le_acesso.setText(str(med[0][5]))


#botao de salvar dados editados
def salvar_edit():

	#pega o numero do id
	global numero_id
	nome =	gui_editar.le_nome.text()
	validade = gui_editar.le_validade.text()
	quantidade = gui_editar.le_qtd.text()
	valor = gui_editar.le_valor.text()
	acesso = gui_editar.le_acesso.text()

	#atualizar os dados no banco
	c.execute('UPDATE tbl_remedios SET nome = "{}", validade = "{}", quantidade = "{}", valor = "{}", acesso = "{}" WHERE id_remedio = {}'.format(nome,validade,quantidade,valor,acesso,numero_id))
	
	bnk.commit()


#botao de voltar a tela de dashboard
def voltar_v_d():
	tela_listar.close()
	tela2.show()

#variaveis das telas***********************************************************************************************************************
tela1=uic.loadUi('gui_login.ui')
tela2=uic.loadUi('gui_dashboard.ui')
tela3=uic.loadUi('gui_cad_remedio.ui')
tela4=uic.loadUi('gui_vendas.ui')
tela5=uic.loadUi('gui_cad_funcionario.ui')
tela_listar=uic.loadUi('listar.ui')
gui_editar=uic.loadUi('gui_editar.ui')
gui_registro=uic.loadUi('gui_ver_registro.ui')

#cria as conexoes com os botoes************************************************************************************************************
tela1.bt_entrar.clicked.connect(logar)
tela2.bt_exit.clicked.connect(voltar_login)
tela2.bt_add.clicked.connect(ir_cadastro)
tela3.bt_cadastrar.clicked.connect(cadastrar)
tela3.bt_voltar.clicked.connect(voltartela3)
tela4.bt_registrar.clicked.connect(registrar)
tela4.bt_voltar.clicked.connect(voltar_r_d)
gui_registro.bt_voltar.clicked.connect(voltarvr)
tela4.bt_ver_registro.clicked.connect(ver_registro)
gui_registro.bt_recarregar.clicked.connect(recarregar_registro)
tela2.bt_comprar.clicked.connect(ir_compra)
tela2.bt_funcionario.clicked.connect(ir_funcionario)
tela5.bt_lgcadastrar.clicked.connect(cadastrar_funcionario)
tela5.bt_voltar.clicked.connect(voltar_c_d)
tela2.bt_ver.clicked.connect(ir_visualizar)
tela_listar.bt_recarregar.clicked.connect(recarregar)
tela_listar.bt_voltar.clicked.connect(voltar_v_d)
tela_listar.bt_excluir.clicked.connect(excluir_dados_rmd)
tela_listar.bt_editar.clicked.connect(editar_tbl)
gui_editar.bt_salvar.clicked.connect(salvar_edit)
tela1.show()
app.exec()
