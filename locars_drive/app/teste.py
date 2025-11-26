from app.models.usuario import Usuario
from app.extensions import db

def initialize_admin_user(app):
    # O comando with app.app_context() é essencial para acessar o db
    with app.app_context():
        # Verifique se o usuário admin já existe antes de tentar criar
        admin_email = 'sofia.admin@locarsdrive.com' # <--- NOVO EMAIL
        if not Usuario.query.filter_by(email=admin_email).first():
            
            # Recria o objeto com a lógica de senha e permissões
            novo_admin = Usuario(
                email=admin_email,
                nome_completo='Sofia Lima (Admin)', # <--- NOVO NOME
                data_nasc='1995-08-20', # Nova Data de Nascimento
                cpf='11115432109', # Novo CPF
                cnh='DEF98765432', # Nova CNH
                id_admin=1,
                tipo_perfil='misto',
                id_funcionario=1,
                cargo='Administrador Geral',
                Salario=1000.00
            )
            # A senha de login será 'senha_secreta_aqui'
            novo_admin.set_password('senha_secreta_aqui')
            
            # Adiciona e salva
            db.session.add(novo_admin)
            db.session.commit()
            print(f"Usuário Admin ({admin_email}) criado com sucesso!")
        else:
            print(f"Usuário Admin ({admin_email}) já existe. Pulando criação.")