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
        
        # Create IBGE Trabalhe Conosco program
        ibge_program = Program()
        ibge_program.title = 'IBGE - Trabalhe Conosco'
        ibge_program.description = 'O Instituto Brasileiro de Geografia e Estatística (IBGE) está com processo seletivo simplificado aberto para contratação por tempo determinado. São 9.580 vagas para os cargos de Agente de Pesquisa e Mapeamento e Supervisor de Coleta e Qualidade, distribuídas em todo o território nacional.'
        ibge_program.ministry = 'Instituto Brasileiro de Geografia e Estatística - IBGE'
        ibge_program.program_type = 'Processo Seletivo Simplificado'
        ibge_program.status = 'active'
        ibge_program.published_date = datetime(2025, 7, 5, 10, 0)
        ibge_program.updated_date = datetime(2025, 7, 25, 23, 59)
        
        db.session.add(ibge_program)
        db.session.flush()  # Get the ID
        
        # Create positions for IBGE
        positions = []
        
        # Position 1: Agente de Pesquisa e Mapeamento
        pos1 = Position()
        pos1.name = 'Agente de Pesquisa e Mapeamento'
        pos1.description = 'Execução de atividades de coleta de dados e informações para pesquisas do IBGE, mapeamento territorial e apoio às operações censitárias e estatísticas.'
        pos1.requirements = 'Ensino Médio completo; Idade mínima de 18 anos; Disponibilidade para trabalhar em campo; Conhecimentos básicos de informática.'
        pos1.salary_min = 4379.00
        pos1.salary_max = 4379.00
        pos1.workload_hours = 40
        pos1.work_type = 'Campo'
        pos1.program_id = ibge_program.id
        positions.append(pos1)
        
        # Position 2: Supervisor de Coleta e Qualidade  
        pos2 = Position()
        pos2.name = 'Supervisor de Coleta e Qualidade'
        pos2.description = 'Coordenação e supervisão das equipes de coleta de dados, garantindo a qualidade das informações coletadas e o cumprimento dos cronogramas estabelecidos.'
        pos2.requirements = 'Ensino Médio completo; CNH categoria B; Experiência em supervisão; Conhecimentos de informática; Disponibilidade para viagens.'
        pos2.salary_min = 4978.00
        pos2.salary_max = 4978.00
        pos2.workload_hours = 40
        pos2.work_type = 'Supervisão'
        pos2.program_id = ibge_program.id
        positions.append(pos2)

        
        for position in positions:
            db.session.add(position)
        
        # Add other IBGE programs for search diversity
        other_programs = []
        
        # Program 2: PNAD
        prog2 = Program()
        prog2.title = 'PNAD - Pesquisa Nacional por Amostra de Domicílios'
        prog2.description = 'Pesquisa que tem por objetivo produzir informações básicas sobre as características demográficas e socioeconômicas da população.'
        prog2.ministry = 'Instituto Brasileiro de Geografia e Estatística - IBGE'
        prog2.program_type = 'Pesquisa Nacional'
        prog2.status = 'active'
        prog2.published_date = datetime(2025, 1, 15)
        other_programs.append(prog2)
        
        # Program 3: Censo Demográfico
        prog3 = Program()
        prog3.title = 'Censo Demográfico 2030'
        prog3.description = 'Principal fonte de referência sobre a situação de vida da população nos 5.570 municípios brasileiros.'
        prog3.ministry = 'Instituto Brasileiro de Geografia e Estatística - IBGE'
        prog3.program_type = 'Censo Nacional'
        prog3.status = 'planejamento'
        prog3.published_date = datetime(2025, 2, 10)
        other_programs.append(prog3)
        
        # Program 4: Sistema de Contas Nacionais
        prog4 = Program()
        prog4.title = 'Sistema de Contas Nacionais'
        prog4.description = 'Sistema integrado de informações econômicas que permite conhecer a evolução da economia nacional.'
        prog4.ministry = 'Instituto Brasileiro de Geografia e Estatística - IBGE'
        prog4.program_type = 'Sistema Econômico'
        prog4.status = 'active'
        prog4.published_date = datetime(2025, 3, 5)
        other_programs.append(prog4)
        
        for program in other_programs:
            db.session.add(program)
        
        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")
        print(f"✅ {len(positions)} vagas criadas para o programa IBGE Trabalhe Conosco")
        print(f"✅ {len(other_programs) + 1} programas do IBGE adicionados")

def main():
    """Função principal para popular o banco"""
    try:
        from app import app, db, Program, Position
        
        with app.app_context():
            # Verificar se já existem dados
            existing_program = Program.query.filter_by(title='IBGE - Trabalhe Conosco').first()
            if existing_program:
                print("✅ Banco já possui dados do IBGE Trabalhe Conosco")
                return
            
            print("🔄 Populando banco de dados...")
            populate_database()
            print("✅ Processo concluído!")
            
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        
if __name__ == '__main__':
    main()