from app.models.usuario import Usuario
from app.extensions import db

def initialize_admin_user(app):
    # O comando with app.app_context() é essencial para acessar o db
    with app.app_context():
        # Verifique se o usuário admin já existe antes de tentar criar
        admin_email = 'roberto.admin@locarsdrive.com'
        if not Usuario.query.filter_by(email=admin_email).first():
            
            # Recria o objeto com a lógica de senha e permissões
            roberto_admin = Usuario(
                email=admin_email,
                nome_completo='Roberto Campos (Admin)',
                data_nasc='1990-05-15',
                cpf='12345678901',
                cnh='ABC12345678',
                id_admin=1,
                tipo_perfil='misto',
                id_funcionario=1,
                cargo='Administrador Geral',
                salario=10000.00
            )
            roberto_admin.set_password('senha_secreta_aqui')
            
            # Adiciona e salva
            db.session.add(roberto_admin)
            db.session.commit()
            print(f"Usuário Admin ({admin_email}) criado com sucesso!")
        else:
            print(f"Usuário Admin ({admin_email}) já existe. Pulando criação.")