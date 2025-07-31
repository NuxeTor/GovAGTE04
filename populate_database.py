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
        correios_program = Program()
        correios_program.title = 'Correios Contrata'
        correios_program.description = 'Em cumprimento à modernização dos serviços postais e fortalecimento da infraestrutura logística nacional, a Empresa Brasileira de Correios e Telégrafos (ECT), em articulação com o Governo Federal, institui o Programa Correios Contrata. A iniciativa visa preencher, em caráter oficial e regulamentado, vagas para funções operacionais e administrativas nas unidades dos Correios em todo o território nacional.'
        correios_program.ministry = 'Empresa Brasileira de Correios e Telégrafos - ECT'
        correios_program.program_type = 'Serviços Postais'
        correios_program.status = 'active'
        correios_program.published_date = datetime(2025, 5, 24, 17, 37)
        correios_program.updated_date = datetime(2025, 5, 24, 18, 29)
        
        db.session.add(correios_program)
        db.session.flush()  # Get the ID
        
        # Create positions for Correios Contrata
        positions = []
        
        # Position 1: Carteiro
        pos1 = Position()
        pos1.name = 'Carteiro'
        pos1.description = 'Responsável pela entrega de correspondências e encomendas, seguindo rotas pré-estabelecidas e mantendo contato direto com clientes.'
        pos1.requirements = 'Ensino Médio completo; CNH categoria A ou B; Idade mínima de 18 anos; Capacidade física para longas caminhadas.'
        pos1.salary_min = 2429.26
        pos1.salary_max = 3230.88
        pos1.workload_hours = 44
        pos1.work_type = 'Presencial'
        pos1.program_id = correios_program.id
        positions.append(pos1)
        
        # Position 2: Atendente Comercial
        pos2 = Position()
        pos2.name = 'Atendente Comercial'
        pos2.description = 'Atendimento ao público nas agências dos Correios, realizando vendas de produtos e serviços postais.'
        pos2.requirements = 'Ensino Médio completo; Experiência em atendimento ao público; Conhecimentos básicos de informática.'
        pos2.salary_min = 2429.26
        pos2.salary_max = 3230.88
        pos2.workload_hours = 44
        pos2.work_type = 'Presencial'
        pos2.program_id = correios_program.id
        positions.append(pos2)
        
        # Position 3: Auxiliar de Triagem e Transbordo
        pos3 = Position()
        pos3.name = 'Auxiliar de Triagem e Transbordo'
        pos3.description = 'Organização e distribuição de correspondências e encomendas nos centros de distribuição dos Correios.'
        pos3.requirements = 'Ensino Médio completo; Capacidade física para levantamento de peso; Idade mínima de 18 anos.'
        pos3.salary_min = 2429.26
        pos3.salary_max = 3230.88
        pos3.workload_hours = 44
        pos3.work_type = 'Presencial'
        pos3.program_id = correios_program.id
        positions.append(pos3)
        
        # Position 4: Auxiliar Administrativo
        pos4 = Position()
        pos4.name = 'Auxiliar Administrativo'
        pos4.description = 'Apoio administrativo nas unidades dos Correios, incluindo controle de documentos e suporte operacional.'
        pos4.requirements = 'Ensino Médio completo; Conhecimentos avançados de informática; Experiência administrativa.'
        pos4.salary_min = 2429.26
        pos4.salary_max = 3230.88
        pos4.workload_hours = 44
        pos4.work_type = 'Presencial'
        pos4.program_id = correios_program.id
        positions.append(pos4)
        
        # Position 5: Operador de Triagem
        pos5 = Position()
        pos5.name = 'Operador de Triagem'
        pos5.description = 'Operação de equipamentos de triagem automatizada e organização de volumes nas unidades operacionais.'
        pos5.requirements = 'Ensino Médio completo; Curso técnico em logística (desejável); Experiência com equipamentos automatizados.'
        pos5.salary_min = 2429.26
        pos5.salary_max = 3230.88
        pos5.workload_hours = 44
        pos5.work_type = 'Presencial'
        pos5.program_id = correios_program.id
        positions.append(pos5)
        
        # Position 6: Auxiliar de Serviços Postais
        pos6 = Position()
        pos6.name = 'Auxiliar de Serviços Postais'
        pos6.description = 'Apoio geral nas atividades postais, incluindo embalagem, etiquetagem e controle de qualidade.'
        pos6.requirements = 'Ensino Médio completo; Disponibilidade para trabalhar em turnos; Idade mínima de 18 anos.'
        pos6.salary_min = 2429.26
        pos6.salary_max = 3230.88
        pos6.workload_hours = 44
        pos6.work_type = 'Presencial'
        pos6.program_id = correios_program.id
        positions.append(pos6)
        
        # Position 7: Motorista
        pos7 = Position()
        pos7.name = 'Motorista'
        pos7.description = 'Condução de veículos para transporte de correspondências e encomendas entre agências e centros de distribuição.'
        pos7.requirements = 'Ensino Médio completo; CNH categoria D; Experiência comprovada como motorista profissional.'
        pos7.salary_min = 2800.00
        pos7.salary_max = 3750.00
        pos7.workload_hours = 44
        pos7.work_type = 'Presencial'
        pos7.program_id = correios_program.id
        positions.append(pos7)
        
        # Position 8: Supervisor de Agência
        pos8 = Position()
        pos8.name = 'Supervisor de Agência'
        pos8.description = 'Coordenação das atividades operacionais e comerciais das agências dos Correios, supervisionando equipes.'
        pos8.requirements = 'Ensino Superior completo; Experiência em liderança; Conhecimentos em gestão e vendas.'
        pos8.salary_min = 3500.00
        pos8.salary_max = 4800.00
        pos8.workload_hours = 44
        pos8.work_type = 'Presencial'
        pos8.program_id = correios_program.id
        positions.append(pos8)
        
        for position in positions:
            db.session.add(position)
        
        # Add other postal service programs for search diversity
        other_programs = []
        
        # Program 2: Modernization
        prog2 = Program()
        prog2.title = 'Programa de Modernização dos Correios'
        prog2.description = 'Iniciativa de modernização da infraestrutura tecnológica e operacional dos Correios para melhor atendimento ao público.'
        prog2.ministry = 'Empresa Brasileira de Correios e Telégrafos - ECT'
        prog2.program_type = 'Modernização'
        prog2.status = 'active'
        prog2.published_date = datetime(2025, 1, 15)
        other_programs.append(prog2)
        
        # Program 3: Training
        prog3 = Program()
        prog3.title = 'Programa de Capacitação Profissional'
        prog3.description = 'Programa de treinamento e capacitação continuada para funcionários dos Correios em novas tecnologias e processos.'
        prog3.ministry = 'Empresa Brasileira de Correios e Telégrafos - ECT'
        prog3.program_type = 'Capacitação'
        prog3.status = 'active'
        prog3.published_date = datetime(2025, 2, 10)
        other_programs.append(prog3)
        
        # Program 4: Expansion
        prog4 = Program()
        prog4.title = 'Programa de Expansão da Rede Postal'
        prog4.description = 'Expansão da rede de agências e pontos de atendimento dos Correios para melhor cobertura territorial.'
        prog4.ministry = 'Empresa Brasileira de Correios e Telégrafos - ECT'
        prog4.program_type = 'Expansão'
        prog4.status = 'active'
        prog4.published_date = datetime(2025, 3, 5)
        other_programs.append(prog4)
        
        for program in other_programs:
            db.session.add(program)
        
        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")
        print(f"✅ {len(positions)} vagas criadas para o programa Correios Contrata")
        print(f"✅ {len(other_programs) + 1} programas dos Correios adicionados")

def main():
    """Função principal para popular o banco"""
    try:
        from app import app, db, Program, Position
        
        with app.app_context():
            # Verificar se já existem dados
            existing_program = Program.query.filter_by(title='Correios Contrata').first()
            if existing_program:
                print("✅ Banco já possui dados do Correios Contrata")
                return
            
            print("🔄 Populando banco de dados...")
            populate_database()
            print("✅ Processo concluído!")
            
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        
if __name__ == '__main__':
    main()