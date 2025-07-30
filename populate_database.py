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
        
        # Create Correios Contrata program
        correios_program = Program(
            title='Correios Contrata',
            description='Em cumprimento à modernização dos serviços postais e fortalecimento da infraestrutura logística nacional, a Empresa Brasileira de Correios e Telégrafos (ECT), em articulação com o Governo Federal, institui o Programa Correios Contrata. A iniciativa visa preencher, em caráter oficial e regulamentado, vagas para funções operacionais e administrativas nas unidades dos Correios em todo o território nacional.',
            ministry='Empresa Brasileira de Correios e Telégrafos - ECT',
            program_type='Serviços Postais',
            status='active',
            published_date=datetime(2025, 5, 24, 17, 37),
            updated_date=datetime(2025, 5, 24, 18, 29)
        )
        
        db.session.add(correios_program)
        db.session.flush()  # Get the ID
        
        # Create positions for Correios Contrata
        positions = [
            Position(
                name='Carteiro',
                description='Responsável pela entrega de correspondências e encomendas, seguindo rotas pré-estabelecidas e mantendo contato direto com clientes.',
                requirements='Ensino Médio completo; CNH categoria A ou B; Idade mínima de 18 anos; Capacidade física para longas caminhadas.',
                salary_min=2429.26,
                salary_max=3230.88,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Atendente Comercial',
                description='Atendimento ao público nas agências dos Correios, realizando vendas de produtos e serviços postais.',
                requirements='Ensino Médio completo; Experiência em atendimento ao público; Conhecimentos básicos de informática.',
                salary_min=2429.26,
                salary_max=3230.88,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Auxiliar de Triagem e Transbordo',
                description='Organização e distribuição de correspondências e encomendas nos centros de distribuição dos Correios.',
                requirements='Ensino Médio completo; Capacidade física para levantamento de peso; Idade mínima de 18 anos.',
                salary_min=2429.26,
                salary_max=3230.88,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Auxiliar Administrativo',
                description='Apoio administrativo nas unidades dos Correios, incluindo controle de documentos e suporte operacional.',
                requirements='Ensino Médio completo; Conhecimentos avançados de informática; Experiência administrativa.',
                salary_min=2429.26,
                salary_max=3230.88,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Operador de Triagem',
                description='Operação de equipamentos de triagem automatizada e organização de volumes nas unidades operacionais.',
                requirements='Ensino Médio completo; Curso técnico em logística (desejável); Experiência com equipamentos automatizados.',
                salary_min=2429.26,
                salary_max=3230.88,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Auxiliar de Serviços Postais',
                description='Apoio geral nas atividades postais, incluindo embalagem, etiquetagem e controle de qualidade.',
                requirements='Ensino Médio completo; Disponibilidade para trabalhar em turnos; Idade mínima de 18 anos.',
                salary_min=2429.26,
                salary_max=3230.88,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Motorista',
                description='Condução de veículos para transporte de correspondências e encomendas entre agências e centros de distribuição.',
                requirements='Ensino Médio completo; CNH categoria D; Experiência comprovada como motorista profissional.',
                salary_min=2800.00,
                salary_max=3750.00,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            ),
            Position(
                name='Supervisor de Agência',
                description='Coordenação das atividades operacionais e comerciais das agências dos Correios, supervisionando equipes.',
                requirements='Ensino Superior completo; Experiência em liderança; Conhecimentos em gestão e vendas.',
                salary_min=3500.00,
                salary_max=4800.00,
                workload_hours=44,
                work_type='Presencial',
                program_id=correios_program.id
            )
        ]
        
        for position in positions:
            db.session.add(position)
        
        # Add other postal service programs for search diversity
        other_programs = [
            Program(
                title='Programa de Modernização dos Correios',
                description='Iniciativa de modernização da infraestrutura tecnológica e operacional dos Correios para melhor atendimento ao público.',
                ministry='Empresa Brasileira de Correios e Telégrafos - ECT',
                program_type='Modernização',
                status='active',
                published_date=datetime(2025, 1, 15)
            ),
            Program(
                title='Programa de Capacitação Profissional',
                description='Programa de treinamento e capacitação continuada para funcionários dos Correios em novas tecnologias e processos.',
                ministry='Empresa Brasileira de Correios e Telégrafos - ECT',
                program_type='Capacitação',
                status='active',
                published_date=datetime(2025, 2, 10)
            ),
            Program(
                title='Programa de Expansão da Rede Postal',
                description='Expansão da rede de agências e pontos de atendimento dos Correios para melhor cobertura territorial.',
                ministry='Empresa Brasileira de Correios e Telégrafos - ECT',
                program_type='Expansão',
                status='active',
                published_date=datetime(2025, 3, 5)
            )
        ]
        
        for program in other_programs:
            db.session.add(program)
        
        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")
        print(f"✅ {len(positions)} vagas criadas para o programa Correios Contrata")
        print(f"✅ {len(other_programs) + 1} programas dos Correios adicionados")

if __name__ == '__main__':
    populate_database()