import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
import oracledb
import json

print("Programa CRUD Primeiros Socorros Maternidade")


class meuApp(App):

    def __init__(self):
        super().__init__()
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")
        print("Conectado")

    def build(self):
        self.screen_manager = ScreenManager()
        self.Screen_main = Screen_main(name='validacao_usuario')
        self.Screen_usuario = Screen_usuario(name='cadastro_usuario')
        self.Screen_login = Screen_login(name='login')
        self.Screen_menu = Screen_menu(name='menu-opcoes')
        self.Screen_medico = Screen_medico(name='cadastro_medico')
        self.Screen_consultar_medico = Screen_consultar_medico(
            name='consultar_medico')
        self.Screen_atualizar_medico = Screen_atualizar_medico(
            name='atualizar_medico')
        self.Screen_deletar_medico = Screen_deletar_medico(
            name='deletar_medico')
        self.Screen_exportar_json = Screen_exportar_json(name='exportar_json')
        self.screen_manager.add_widget(self.Screen_main)
        self.screen_manager.add_widget(self.Screen_usuario)
        self.screen_manager.add_widget(self.Screen_login)
        self.screen_manager.add_widget(self.Screen_menu)
        self.screen_manager.add_widget(self.Screen_medico)
        self.screen_manager.add_widget(self.Screen_consultar_medico)
        self.screen_manager.add_widget(self.Screen_atualizar_medico)
        self.screen_manager.add_widget(self.Screen_deletar_medico)
        self.screen_manager.add_widget(self.Screen_exportar_json)
        return self.screen_manager

# LOGIN


class Screen_main(Screen):

    def __init__(self, **kwargs):
        super(Screen_main, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_bem_vindo = Label(text='Bem Vindo!')
        box.add_widget(lbl_bem_vindo)

        btn_cadastrar_usuario = Button(text='Cadastrar usuário')
        box.add_widget(btn_cadastrar_usuario)
        btn_cadastrar_usuario.bind(on_press=self.tela_cadastro_usuario)

        btn_login = Button(text='Login')
        box.add_widget(btn_login)
        btn_login.bind(on_press=self.tela_login)

        self.add_widget(box)

    def tela_cadastro_usuario(self, instance):
        self.manager.current = 'cadastro_usuario'

    def tela_login(self, instance):
        self.manager.current = 'login'


# Cadastro usuário
class Screen_usuario(Screen):
    def __init__(self, **kwargs):
        super(Screen_usuario, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_email = Label(text='Email: ')
        box.add_widget(lbl_email)
        self.txt_email = TextInput()
        box.add_widget(self.txt_email)

        lbl_senha = Label(text='Senha: ')
        box.add_widget(lbl_senha)
        self.txt_senha = TextInput()
        box.add_widget(self.txt_senha)

        btn_cadastrar = Button(text='Cadastrar')
        box.add_widget(btn_cadastrar)
        btn_cadastrar.bind(on_press=self.cadastrar_usuario)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def cadastrar_usuario(self, instance):

        email = self.txt_email.text
        senha = self.txt_senha.text

        try:
            conn = oracledb.connect(user="rm551154",
                                    password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO gs_usuario (email, senha) VALUES (:email, :senha)",
                           email=email, senha=senha)
            conn.commit()
            cursor.close()
            print('Seu cadastro foi realizado com sucesso!')
        except Exception as e:
            print('Erro ao cadastrar usuário: ', e)

    # Voltar ao menu inicial

    def voltar(self, instance):
        self.manager.current = 'validacao_usuario'


class Screen_login(Screen):
    def __init__(self, **kwargs):
        super(Screen_login, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_email = Label(text='Email: ')
        box.add_widget(lbl_email)
        self.txt_email = TextInput()
        box.add_widget(self.txt_email)

        lbl_senha = Label(text='Senha: ')
        box.add_widget(lbl_senha)
        self.txt_senha = TextInput()
        box.add_widget(self.txt_senha)

        btn_login = Button(text='Login')
        box.add_widget(btn_login)
        btn_login.bind(on_press=self.login)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def login(self, instance):

        email = self.txt_email.text
        senha = self.txt_senha.text

        try:
            conn = oracledb.connect(user="rm551154",
                                    password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gs_usuario WHERE email = :email AND senha = :senha",
                           email=email, senha=senha)
            validacao = cursor.fetchone()
            conn.commit()
            cursor.close()
            if validacao:
                print('Login realizado com sucesso!')
                self.manager.current = 'menu-opcoes'
            else:
                print('Email e/ou senha inválidos. Tente novamente.')
        except Exception as e:
            print('Erro ao realizar login: ', e)

    def voltar(self, instance):
        self.manager.current = 'validacao_usuario'

# MENU


class Screen_menu(Screen):

    def __init__(self, **kwargs):
        super(Screen_menu, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_menu = Label(text='MENU DE OPÇÕES')
        box.add_widget(lbl_menu)
        btn_cadastro_medico = Button(text='Cadastrar médico')
        btn_cadastro_medico.bind(on_press=self.tela_cadastro_medico)
        btn_consultar_medico = Button(text='Consultar médico')
        btn_consultar_medico.bind(on_press=self.tela_consulta_medico)
        btn_atualizar_medico = Button(text='Atualizar médico')
        btn_atualizar_medico.bind(on_press=self.tela_atualizar_medico)
        btn_deletar_medico = Button(text='Deletar médico')
        btn_deletar_medico.bind(on_press=self.tela_deletar_medico)
        btn_exportar_json = Button(text='Exportar para JSON')
        btn_exportar_json.bind(on_press=self.tela_exportar_json)
        btn_sair = Button(text='Sair')
        btn_sair.bind(on_press=self.sair)
        box.add_widget(btn_cadastro_medico)
        box.add_widget(btn_consultar_medico)
        box.add_widget(btn_atualizar_medico)
        box.add_widget(btn_deletar_medico)
        box.add_widget(btn_exportar_json)
        box.add_widget(btn_sair)

        self.add_widget(box)

    def tela_consulta_medico(self, instance):
        self.manager.current = 'consultar_medico'

    def tela_cadastro_medico(self, instance):
        self.manager.current = 'cadastro_medico'

    def tela_atualizar_medico(self, instance):
        self.manager.current = 'atualizar_medico'

    def tela_deletar_medico(self, instance):
        self.manager.current = 'deletar_medico'

    def tela_exportar_json(self, instance):
        self.manager.current = 'exportar_json'

    def sair(self, instance):
        App.get_running_app().stop()
        print("Ate logo! :)")


# Cadastrar médico - Create
class Screen_medico(Screen):
    def __init__(self, **kwargs):
        super(Screen_medico, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_nome = Label(text='Nome completo: ')
        box.add_widget(lbl_nome)
        self.txt_nome = TextInput()
        box.add_widget(self.txt_nome)

        lbl_crm = Label(text='CRM: ')
        box.add_widget(lbl_crm)
        self.txt_crm = TextInput()
        box.add_widget(self.txt_crm)

        lbl_especialidade = Label(text='Especialidade: ')
        box.add_widget(lbl_especialidade)
        self.txt_especialidade = TextInput()
        box.add_widget(self.txt_especialidade)

        lbl_formacao = Label(text='Formação: ')
        box.add_widget(lbl_formacao)
        self.txt_formacao = TextInput()
        box.add_widget(self.txt_formacao)

        btn_cadastrar = Button(text='Cadastrar')
        box.add_widget(btn_cadastrar)
        btn_cadastrar.bind(on_press=self.cadastrar_medico)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def cadastrar_medico(self, instance):

        nome = self.txt_nome.text
        crm = self.txt_crm.text
        formacao = self.txt_formacao.text
        especialidade = self.txt_especialidade.text

        try:
            conn = oracledb.connect(user="rm551154",
                                    password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO gs_medico (nome, crm, especialidade, formacao) VALUES (:nome, :crm, :especialidade, :formacao)",
                           nome=nome, crm=crm, especialidade=especialidade, formacao=formacao)
            conn.commit()
            cursor.close()
            print(f'Médico(a) {crm} cadastrado(a) com sucesso!')
        except Exception as e:
            print('Erro ao cadastrar médico: ', e)

    # Voltar ao menu inicial

    def voltar(self, instance):
        self.manager.current = 'menu-opcoes'


# Consultar médico - Read
class Screen_consultar_medico(Screen):
    def __init__(self, **kwargs):
        super(Screen_consultar_medico, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_crm_medico = Label(text='CRM do médico: ')
        box.add_widget(lbl_crm_medico)
        self.txt_crm_medico = TextInput()
        box.add_widget(self.txt_crm_medico)

        btn_consultar = Button(text='Consultar')
        box.add_widget(btn_consultar)
        btn_consultar.bind(on_press=self.listar_medico)

        btn_consultar_todos = Button(text='Consultar Todos')
        box.add_widget(btn_consultar_todos)
        btn_consultar_todos.bind(on_press=self.listar_medicos)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def voltar(self, instance):
        self.manager.current = 'menu-opcoes'

    # Consultar 1 médico

    def listar_medico(self, *args):

        crm_medico = self.txt_crm_medico.text

        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            sql = """SELECT nome, crm, especialidade, formacao FROM gs_medico WHERE crm = :crm_medico"""

            cursor.execute(sql, {'crm_medico': crm_medico})

            medico = cursor.fetchone()

            if medico:
                print(
                    f"Nome: {medico[0]}, CRM: {medico[1]}, Especialidade: {medico[2]}, Formação: {medico[3]}")
            else:
                print(f"Nenhum médico encontrado com o CRM: {crm_medico}")

            cursor.close()

        except Exception as e:
            print('Erro ao consultar médico: ', e)

    # Consultar todos os médicos

    def listar_medicos(self, *args):
        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()
            sql = """SELECT nome, crm, especialidade, formacao FROM gs_medico"""
            cursor.execute(sql)

            medicos = cursor.fetchall()

            for medico in medicos:
                print(
                    f"Nome: {medico[0]}, CRM: {medico[1]}, Especialidade: {medico[2]}, Formação: {medico[3]}")

            cursor.close()

        except Exception as e:
            print('Erro ao consultar médicos: ', e)


# Atualizar médico - Update
class Screen_atualizar_medico(Screen):
    def __init__(self, **kwargs):
        super(Screen_atualizar_medico, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_novo_nome = Label(text='Novo nome do médico: ')
        box.add_widget(lbl_novo_nome)
        self.txt_novo_nome = TextInput()
        box.add_widget(self.txt_novo_nome)

        lbl_nova_especialidade = Label(text='Nova especialidade do médico: ')
        box.add_widget(lbl_nova_especialidade)
        self.txt_nova_especialidade = TextInput()
        box.add_widget(self.txt_nova_especialidade)

        lbl_nova_formacao = Label(text='Nova formação do médico: ')
        box.add_widget(lbl_nova_formacao)
        self.txt_nova_formacao = TextInput()
        box.add_widget(self.txt_nova_formacao)

        lbl_crm = Label(text='CRM do médico: ')
        box.add_widget(lbl_crm)
        self.txt_crm = TextInput()
        box.add_widget(self.txt_crm)

        btn_atualizar = Button(text='Atualizar')
        box.add_widget(btn_atualizar)
        btn_atualizar.bind(on_press=self.atualizar_medico)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def voltar(self, instance):
        self.manager.current = 'menu-opcoes'

    def atualizar_medico(self, *args):

        novo_nome = self.txt_novo_nome.text
        nova_especialidade = self.txt_nova_especialidade.text
        nova_formacao = self.txt_nova_formacao.text
        crm_medico = self.txt_crm.text

        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            sql = """
                UPDATE gs_medico
                SET nome = :novo_nome, crm = :crm_medico, especialidade = :nova_especialidade, formacao = :nova_formacao
                WHERE crm = :crm_medico
            """
            cursor.execute(sql, novo_nome=novo_nome, nova_especialidade=nova_especialidade,
                           nova_formacao=nova_formacao, crm_medico=crm_medico)

            conn.commit()

            if cursor.rowcount > 0:
                print(f"O médico {crm_medico} foi atualizado com sucesso.")
            else:
                print(f"Nenhum médico encontrado com o CRM {crm_medico}.")

            cursor.close()

        except Exception as e:
            print('Erro ao atualizar médico: ', e)


# Deletar médico - Delete
class Screen_deletar_medico(Screen):
    def __init__(self, **kwargs):
        super(Screen_deletar_medico, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        lbl_deletar_crm = Label(text='CRM do médico: ')
        box.add_widget(lbl_deletar_crm)
        self.txt_deletar_crm = TextInput()
        box.add_widget(self.txt_deletar_crm)

        btn_deletar = Button(text='Deletar')
        box.add_widget(btn_deletar)
        btn_deletar.bind(on_press=self.deletar_medico)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def voltar(self, instance):
        self.manager.current = 'menu-opcoes'

    def deletar_medico(self, *args):

        crm_medico = self.txt_deletar_crm.text

        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            sql = """
                DELETE FROM gs_medico
                WHERE crm = :crm_medico
            """
            cursor.execute(sql, crm_medico=crm_medico)
            conn.commit()

            if cursor.rowcount > 0:
                print(f"O médico {crm_medico} foi excluído com sucesso.")
            else:
                print(f"Nenhum médico encontrado com o CRM {crm_medico}.")

            cursor.close()

        except Exception as e:
            print('Erro ao deletar médico: ', e)

# Exportar consultas para JSON


class Screen_exportar_json(Screen):
    def __init__(self, **kwargs):
        super(Screen_exportar_json, self).__init__(**kwargs)
        self.conn = oracledb.connect(user="rm551154", password="210105",
                                     dsn="oracle.fiap.com.br:1521/orcl")

        box = BoxLayout(orientation='vertical')

        btn_expo_nome_crm = Button(text='Exportar Nomes e CRMs')
        btn_expo_nome_crm.bind(on_press=self.expo_nome_crm)
        box.add_widget(btn_expo_nome_crm)

        btn_ultimas_consultas = Button(text='Exportar 3 últimas consultas')
        btn_ultimas_consultas.bind(on_press=self.expo_ultimas_consultas)
        box.add_widget(btn_ultimas_consultas)

        btn_consulta_formacao = Button(
            text='Exportar médicos com formação USP')
        btn_consulta_formacao.bind(on_press=self.expo_formacao_USP)
        box.add_widget(btn_consulta_formacao)

        btn_voltar = Button(text='Voltar')
        box.add_widget(btn_voltar)
        btn_voltar.bind(on_press=self.voltar)

        self.add_widget(box)

    def voltar(self, instance):
        self.manager.current = 'menu-opcoes'

    def expo_nome_crm(self, *args):
        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            sql = """SELECT nome, crm FROM gs_medico"""

            cursor.execute(sql)

            medicos = cursor.fetchall()

            nomes_crms = json.dumps(medicos, indent=2)

            with open('nomes_crms.json', 'w') as json_file:
                json_file.write(nomes_crms)

            print(f"Consultas exportadas para 'nomes_crms.json'")

            cursor.close()

        except Exception as e:
            print('Erro ao exportar consultas para JSON: ', e)

    def expo_ultimas_consultas(self, *args):
        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            sql = """SELECT * FROM gs_medico ORDER BY crm DESC FETCH FIRST 3 ROWS ONLY"""

            cursor.execute(sql)

            medicos = cursor.fetchall()

            ultimas_consultas = json.dumps(medicos, indent=2)

            with open('ultimas_consultas.json', 'w') as json_file2:
                json_file2.write(ultimas_consultas)

            print(f"Consultas exportadas para 'ultimas_consultas.json'")

            cursor.close()

        except Exception as e:
            print('Erro ao exportar consultas para JSON: ', e)

    def expo_formacao_USP(self, *args):
        try:
            conn = oracledb.connect(user="rm551154", password="210105",
                                    dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            sql = """SELECT * FROM gs_medico WHERE formacao = 'USP'"""

            cursor.execute(sql)

            medicos = cursor.fetchall()

            formacao = json.dumps(medicos, indent=2)

            with open('consulta_formacao.json', 'w') as json_file3:
                json_file3.write(formacao)

            print(f"Consultas exportadas para 'consulta_formacao.json'")

            cursor.close()

        except Exception as e:
            print('Erro ao exportar consultas para JSON: ', e)


if __name__ == "__main__":
    app = meuApp()
    app.run()