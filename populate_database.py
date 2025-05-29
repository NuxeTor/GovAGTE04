"""
Populate database with real PNAE program data
"""
from app import app, db, Program, Position
from datetime import datetime

def populate_database():
    with app.app_context():
        # Clear existing data
        Position.query.delete()
        Program.query.delete()
        
        # Create PNAE program
        pnae_program = Program(
            title='Mais Agentes da Educação',
            description='Em cumprimento à agenda estratégica de valorização da educação pública e fortalecimento da gestão escolar nos municípios, o Governo Federal, em articulação com as Prefeituras Municipais, institui o Programa Nacional de Agentes da Educação (PNAE). A iniciativa visa preencher, em caráter oficial e regulamentado, vagas para funções de apoio técnico-operacional nas unidades escolares municipais.',
            ministry='Ministério da Educação',
            program_type='Educação Básica',
            status='active',
            published_date=datetime(2025, 5, 24, 17, 37),
            updated_date=datetime(2025, 5, 24, 18, 29)
        )
        
        db.session.add(pnae_program)
        db.session.flush()  # Get the ID
        
        # Create positions for PNAE
        positions = [
            Position(
                name='Auxiliar Administrativo',
                description='Responsável pelo apoio às atividades administrativas da unidade escolar, incluindo organização de documentos, atendimento ao público e suporte à gestão.',
                requirements='Ensino Médio completo; Idade mínima de 18 anos; Participação em curso técnico preparatório.',
                salary_min=2149.35,
                salary_max=2800.00,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Auxiliar de Produção Escolar',
                description='Atua no preparo e distribuição da alimentação escolar, garantindo qualidade nutricional e segurança alimentar aos estudantes.',
                requirements='Ensino Médio completo; Curso de manipulação de alimentos; Idade mínima de 18 anos.',
                salary_min=2149.35,
                salary_max=2600.00,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Auxiliar de Secretaria',
                description='Presta suporte às atividades da secretaria escolar, incluindo matrícula de alunos, organização de prontuários e atendimento aos responsáveis.',
                requirements='Ensino Médio completo; Conhecimentos básicos de informática; Idade mínima de 18 anos.',
                salary_min=2300.00,
                salary_max=2900.00,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Auxiliar de Segurança Escolar',
                description='Responsável pela segurança do ambiente escolar, controle de acesso e proteção do patrimônio público.',
                requirements='Ensino Médio completo; Curso de segurança patrimonial; Idade mínima de 21 anos.',
                salary_min=2400.00,
                salary_max=3100.00,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Auxiliar de Serviços de Limpeza',
                description='Mantém a limpeza e organização dos espaços escolares, garantindo ambiente saudável e adequado para o aprendizado.',
                requirements='Ensino Médio completo; Experiência em limpeza institucional; Idade mínima de 18 anos.',
                salary_min=2149.35,
                salary_max=2500.00,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Auxiliar de Cozinha Escolar',
                description='Atua no preparo de refeições escolares, seguindo cardápios nutricionais e normas de higiene alimentar.',
                requirements='Ensino Médio completo; Curso de manipulação de alimentos; Idade mínima de 18 anos.',
                salary_min=2149.35,
                salary_max=2600.00,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Técnico em Manutenção Predial',
                description='Realiza manutenção preventiva e corretiva das instalações escolares, garantindo funcionamento adequado da infraestrutura.',
                requirements='Ensino Médio completo; Curso técnico em edificações ou manutenção; Idade mínima de 18 anos.',
                salary_min=2800.00,
                salary_max=3412.32,
                workload_hours=40,
                work_type='Presencial',
                program_id=pnae_program.id
            ),
            Position(
                name='Secretário Escolar',
                description='Coordena as atividades da secretaria escolar, gerencia documentação oficial e presta suporte à gestão pedagógica.',
                requirements='Ensino Médio completo; Experiência em secretaria escolar; Conhecimentos avançados de informática.',
                salary_min=2600.00,
                salary_max=3200.00,
                workload_hours=30,
                work_type='Home Office',
                program_id=pnae_program.id
            )
        ]
        
        for position in positions:
            db.session.add(position)
        
        # Add other education programs for search diversity
        other_programs = [
            Program(
                title='Programa Nacional do Livro Didático',
                description='O PNLD tem por objetivo subsidiar o trabalho pedagógico dos professores por meio da distribuição de coleções de livros didáticos aos alunos da educação básica.',
                ministry='Ministério da Educação',
                program_type='Material Didático',
                status='active',
                published_date=datetime(2025, 1, 15)
            ),
            Program(
                title='Programa Mais Alfabetização',
                description='Programa de apoio à alfabetização, destinado a fortalecer e apoiar as unidades escolares no processo de alfabetização dos estudantes.',
                ministry='Ministério da Educação',
                program_type='Alfabetização',
                status='active',
                published_date=datetime(2025, 2, 10)
            ),
            Program(
                title='Programa Nacional de Alimentação Escolar',
                description='O PNAE garante, por meio da transferência de recursos financeiros, a alimentação escolar dos alunos de toda a educação básica.',
                ministry='Ministério da Educação',
                program_type='Alimentação Escolar',
                status='active',
                published_date=datetime(2025, 3, 5)
            )
        ]
        
        for program in other_programs:
            db.session.add(program)
        
        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")
        print(f"✅ {len(positions)} vagas criadas para o programa PNAE")
        print(f"✅ {len(other_programs) + 1} programas educacionais adicionados")

if __name__ == '__main__':
    populate_database()