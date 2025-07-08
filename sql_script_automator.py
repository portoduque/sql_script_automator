import json
import re
import time
import sys
from datetime import datetime
from typing import Any, List, Dict, Optional
from io import StringIO

class ProgressBar:
    """
    Classe para exibir uma barra de progresso visual no terminal.
    """
    def __init__(self, total: int, description: str = "Processando", bar_length: int = 50):
        self.total = total
        self.current = 0
        self.description = description
        self.bar_length = bar_length
        self.start_time = time.time()
        self.last_update = 0
        
    def update(self, increment: int = 1):
        """
        Atualiza o progresso da barra.
        
        Args:
            increment: Quantidade a incrementar (padrão: 1)
        """
        self.current = min(self.current + increment, self.total)
        current_time = time.time()
        
        # Atualizar apenas a cada 0.1 segundos para melhor performance
        if current_time - self.last_update < 0.1 and self.current < self.total:
            return
            
        self.last_update = current_time
        self._draw()
    
    def _draw(self):
        """
        Desenha a barra de progresso no terminal.
        """
        if self.total == 0:
            return
            
        # Calcular percentual
        percent = (self.current / self.total) * 100
        filled_length = int(self.bar_length * self.current // self.total)
        
        # Criar barra visual
        bar = '█' * filled_length + '░' * (self.bar_length - filled_length)
        
        # Calcular tempo decorrido e estimativa
        elapsed_time = time.time() - self.start_time
        
        if self.current > 0:
            # Estimar tempo restante
            rate = self.current / elapsed_time
            remaining_items = self.total - self.current
            eta_seconds = remaining_items / rate if rate > 0 else 0
            eta_formatted = self._format_time(eta_seconds)
        else:
            eta_formatted = "calculando..."
        
        elapsed_formatted = self._format_time(elapsed_time)
        
        # Formatar linha de progresso
        progress_line = (f"\r{self.description}: |{bar}| "
                        f"{self.current}/{self.total} ({percent:.1f}%) "
                        f"⏱️ {elapsed_formatted} | ETA: {eta_formatted}")
        
        # Limpar linha anterior e escrever nova
        sys.stdout.write('\r' + ' ' * 120)  # Limpar linha
        sys.stdout.write(progress_line)
        sys.stdout.flush()
        
        # Nova linha quando completo
        if self.current >= self.total:
            print()  # Nova linha ao final
    
    def _format_time(self, seconds: float) -> str:
        """
        Formata tempo em segundos para formato legível.
        
        Args:
            seconds: Tempo em segundos
            
        Returns:
            String formatada (ex: "2m 30s", "45s")
        """
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def finish(self):
        """
        Finaliza a barra de progresso.
        """
        self.current = self.total
        self._draw()

class JSONToSQLConverter:
    def __init__(self, table_name: str = "unidade_saude"):
        self.table_name = table_name
        # Campos específicos que devem ser incluídos no SQL
        self.required_fields = [
            "codigo_cnes",
            "numero_cnpj_entidade",
            "nome_razao_social",
            "nome_fantasia",
            "natureza_organizacao_entidade",
            "tipo_gestao",
            "descricao_nivel_hierarquia",
            "descricao_esfera_administrativa",
            "codigo_tipo_unidade",
            "codigo_cep_estabelecimento",
            "endereco_estabelecimento",
            "numero_estabelecimento",
            "bairro_estabelecimento",
            "numero_telefone_estabelecimento",
            "latitude_estabelecimento_decimo_grau",
            "longitude_estabelecimento_decimo_grau",
            "endereco_email_estabelecimento",
            "numero_cnpj",
            "codigo_identificador_turno_atendimento",
            "descricao_turno_atendimento",
            "estabelecimento_faz_atendimento_ambulatorial_sus",
            "codigo_estabelecimento_saude",
            "codigo_uf",
            "codigo_municipio",
            "descricao_natureza_juridica_estabelecimento",
            "codigo_motivo_desabilitacao_estabelecimento",
            "estabelecimento_possui_centro_cirurgico",
            "estabelecimento_possui_centro_obstetrico",
            "estabelecimento_possui_centro_neonatal",
            "estabelecimento_possui_atendimento_hospitalar",
            "estabelecimento_possui_servico_apoio",
            "estabelecimento_possui_atendimento_ambulatorial",
            "codigo_atividade_ensino_unidade",
            "codigo_natureza_organizacao_unidade",
            "codigo_nivel_hierarquia_unidade",
            "codigo_esfera_administrativa_unidade",
            "data_atualizacao"
        ]
        
    def format_sql_value(self, value: Any) -> str:
        """
        Formata um valor Python para sua representação SQL adequada (versão otimizada).
        
        Args:
            value: O valor a ser formatado
            
        Returns:
            String com o valor formatado para SQL
        """
        if value is None:
            return "NULL"
        
        value_type = type(value)
        
        # Tratar strings (otimizado)
        if value_type is str:
            # Verificação rápida para datas
            if len(value) in (10, 8) and value.replace('-', '').replace('/', '').isdigit():
                formatted_date = self._format_date_fast(value)
                if formatted_date:
                    return f"'{formatted_date}'"
            
            # Escapar aspas simples (otimizado)
            if "'" in value:
                escaped = value.replace("'", "''")
                return f"'{escaped}'"
            return f"'{value}'"
        
        # Tratar números
        if value_type in (int, float):
            return str(value)
        
        # Tratar booleanos
        if value_type is bool:
            return "TRUE" if value else "FALSE"
        
        # Para outros tipos, converter para string
        str_value = str(value)
        if "'" in str_value:
            escaped = str_value.replace("'", "''")
            return f"'{escaped}'"
        return f"'{str_value}'"
    
    def _format_date_fast(self, date_string: str) -> Optional[str]:
        """
        Versão otimizada do formatador de data para casos comuns.
        
        Args:
            date_string: String contendo a data
            
        Returns:
            Data formatada como YYYY-MM-DD ou None se não conseguir converter
        """
        try:
            # Caso mais comum: YYYY-MM-DD (já no formato correto)
            if len(date_string) == 10 and date_string[4] == '-' and date_string[7] == '-':
                return date_string
            
            # Caso DD/MM/YYYY
            if len(date_string) == 10 and date_string[2] == '/' and date_string[5] == '/':
                day, month, year = date_string.split('/')
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Caso YYYY/MM/DD
            if len(date_string) == 10 and date_string[4] == '/' and date_string[7] == '/':
                year, month, day = date_string.split('/')
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Para outros casos, usar o método original (mais lento mas funciona)
            return self._format_date(date_string)
        except:
            return None
    
    def _format_date(self, date_string: str) -> Optional[str]:
        """
        Converte uma string de data para o formato YYYY-MM-DD.
        
        Args:
            date_string: String contendo a data
            
        Returns:
            Data formatada como YYYY-MM-DD ou None se não conseguir converter
        """
        try:
            # Tentar diferentes formatos de entrada
            formats = [
                '%Y-%m-%d',  # YYYY-MM-DD
                '%d/%m/%Y',  # DD/MM/YYYY
                '%Y/%m/%d',  # YYYY/MM/DD
                '%d-%m-%Y',  # DD-MM-YYYY
            ]
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_string, fmt)
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None
    
    def generate_bulk_insert_statement(self, json_data: List[Dict[str, Any]], show_progress: bool = True) -> str:
        """
        Gera um único comando SQL INSERT com múltiplos VALUES usando apenas os campos definidos (versão otimizada).
        
        Args:
            json_data: Lista de dicionários representando os registros
            show_progress: Se deve exibir barra de progresso
            
        Returns:
            String com o comando SQL INSERT único com múltiplos VALUES
        """
        if not json_data:
            return "-- Nenhum dado para converter\n"
        
        # Usar StringIO para melhor performance em grandes volumes
        output = StringIO()
        
        # Construir a parte dos campos
        columns_str = ",\n  ".join(self.required_fields)
        
        # Escrever cabeçalho do INSERT
        output.write(f"INSERT INTO {self.table_name} (\n  {columns_str}\n)\nVALUES\n")
        
        # Processar registros em lotes para melhor performance
        total_records = len(json_data)
        
        # Criar barra de progresso se solicitado e houver muitos registros
        progress_bar = None
        if show_progress and total_records > 100:
            progress_bar = ProgressBar(total_records, "Convertendo registros")
        
        for i, record in enumerate(json_data):
            # Construir VALUES de forma otimizada
            values = []
            for col in self.required_fields:
                values.append(self.format_sql_value(record.get(col)))
            
            values_str = ", ".join(values)
            
            if i == total_records - 1:  # Último registro
                output.write(f"({values_str});")
            else:
                output.write(f"({values_str}),\n")
            
            # Atualizar progresso
            if progress_bar:
                progress_bar.update()
        
        # Finalizar progresso
        if progress_bar:
            progress_bar.finish()
        
        return output.getvalue()

    def convert_json_to_sql(self, json_data: List[Dict[str, Any]], batch_size: int = 1000, show_progress: bool = True) -> str:
        """
        Converte uma lista de dicionários em comandos SQL INSERT otimizados.
        Para grandes volumes, divide em lotes menores para melhor compatibilidade.
        
        Args:
            json_data: Lista de dicionários representando os registros
            batch_size: Tamanho do lote (padrão: 1000 registros por INSERT)
            show_progress: Se deve exibir barra de progresso
            
        Returns:
            String com os comandos SQL INSERT
        """
        if not json_data:
            return "-- Nenhum dado para converter\n"
            
        total_records = len(json_data)
        
        # Para arquivos pequenos (menos de 1000 registros), usar método single
        if total_records <= batch_size:
            return self.convert_json_to_bulk_sql(json_data, show_progress)
        
        # Para arquivos grandes, dividir em lotes
        output = StringIO()
        
        # Adicionar comentário inicial
        output.write("-- Comandos SQL INSERT gerados automaticamente (modo lotes)\n")
        output.write(f"-- Tabela: {self.table_name}\n")
        output.write(f"-- Total de registros: {total_records}\n")
        output.write(f"-- Tamanho do lote: {batch_size}\n")
        output.write(f"-- Número de lotes: {(total_records + batch_size - 1) // batch_size}\n")
        output.write("\n")
        
        # Calcular número de lotes
        num_batches = (total_records + batch_size - 1) // batch_size
        
        # Criar barra de progresso para lotes se solicitado
        batch_progress = None
        if show_progress:
            batch_progress = ProgressBar(num_batches, "Processando lotes")
        
        # Processar em lotes
        for i in range(0, total_records, batch_size):
            batch = json_data[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            output.write(f"-- Lote {batch_num}\n")
            # Não mostrar progresso individual para cada lote (evita spam)
            output.write(self.generate_bulk_insert_statement(batch, show_progress=False))
            output.write("\n\n")
            
            # Atualizar progresso do lote
            if batch_progress:
                batch_progress.update()
        
        # Finalizar progresso
        if batch_progress:
            batch_progress.finish()
        
        return output.getvalue()
    
    def convert_json_to_bulk_sql(self, json_data: List[Dict[str, Any]], show_progress: bool = True) -> str:
        """
        Converte uma lista de dicionários em um único comando SQL INSERT com múltiplos VALUES (versão otimizada).
        
        Args:
            json_data: Lista de dicionários representando os registros
            show_progress: Se deve exibir barra de progresso
            
        Returns:
            String com o comando SQL INSERT único
        """
        if not json_data:
            return "-- Nenhum dado para converter\n"
        
        # Usar StringIO para melhor performance
        output = StringIO()
        
        # Adicionar comentário inicial
        output.write("-- Comandos SQL INSERT gerados automaticamente\n")
        output.write(f"-- Tabela: {self.table_name}\n")
        output.write(f"-- Total de registros: {len(json_data)}\n")
        output.write("\n")
        
        # Gerar INSERT único com múltiplos VALUES
        output.write(self.generate_bulk_insert_statement(json_data, show_progress))
        
        return output.getvalue()

    def convert_file(self, input_file: str, output_file: str = None, batch_size: int = 1000, show_progress: bool = True) -> str:
        """
        Lê um arquivo JSON e converte para SQL, salvando em arquivo ou retornando string (versão otimizada).
        
        Args:
            input_file: Caminho do arquivo JSON de entrada
            output_file: Caminho do arquivo SQL de saída (opcional)
            batch_size: Tamanho do lote para grandes arquivos (padrão: 1000)
            show_progress: Se deve exibir barra de progresso
            
        Returns:
            String com os comandos SQL gerados
        """
        try:
            print("🔄 Carregando arquivo JSON...")
            
            # Ler arquivo JSON com buffer otimizado
            with open(input_file, 'r', encoding='utf-8', buffering=8192) as f:
                json_data = json.load(f)
            
            print(f"✅ Arquivo carregado: {len(json_data)} registros")
            
            if show_progress and len(json_data) > 100:
                print("🔄 Convertendo para SQL (com barra de progresso)...")
            else:
                print("🔄 Convertendo para SQL...")
            
            # Converter para SQL
            sql_output = self.convert_json_to_sql(json_data, batch_size, show_progress)
            
            # Salvar em arquivo se especificado
            if output_file:
                print("💾 Salvando arquivo SQL...")
                
                # Criar barra de progresso para escrita do arquivo (se arquivo grande)
                if show_progress and len(sql_output) > 1024 * 1024:  # > 1MB
                    print("📝 Escrevendo arquivo SQL...")
                    
                with open(output_file, 'w', encoding='utf-8', buffering=8192) as f:
                    f.write(sql_output)
                print(f"✅ Arquivo SQL salvo em: {output_file}")
            
            return sql_output
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao decodificar JSON: {e}")
        except Exception as e:
            raise Exception(f"Erro inesperado: {e}")

def main():
    """
    Função principal que executa o conversor de forma simplificada e otimizada.
    """
    print("="*60)
    print("    CONVERSOR JSON PARA SQL - UNIDADES DE SAÚDE")
    print("        VERSÃO OTIMIZADA COM BARRA DE PROGRESSO")
    print("="*60)
    print()
    
    # Solicitar caminho do arquivo JSON
    json_file_path = input("Digite o caminho do arquivo JSON de entrada: ").strip()
    
    if not json_file_path:
        print("❌ Por favor, digite um caminho válido.")
        return
        
    # Verificar se o arquivo existe
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            pass  # Apenas verificar se o arquivo pode ser aberto
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {json_file_path}")
        return
    except Exception as e:
        print(f"❌ Erro ao acessar o arquivo: {e}")
        return
    
    # Gerar nome do arquivo de saída automaticamente
    if json_file_path.lower().endswith('.json'):
        output_file_path = json_file_path[:-5] + '_insert.sql'
    else:
        output_file_path = json_file_path + '_insert.sql'
    
    # Perguntar se deseja usar o nome padrão ou personalizar
    print(f"\nArquivo de saída sugerido: {output_file_path}")
    use_default = input("Deseja usar este nome? (s/n) [s]: ").strip().lower()
    
    if use_default in ['n', 'no', 'não']:
        output_file_path = input("Digite o caminho do arquivo SQL de saída: ").strip()
        if not output_file_path:
            output_file_path = json_file_path[:-5] + '_insert.sql'
    
    # Configurações de performance
    print("\n⚡ CONFIGURAÇÕES DE PERFORMANCE:")
    batch_size_input = input("Tamanho do lote (padrão: 1000) [Enter para usar padrão]: ").strip()
    batch_size = 1000
    if batch_size_input.isdigit():
        batch_size = int(batch_size_input)
        print(f"✅ Tamanho do lote definido: {batch_size}")
    else:
        print(f"✅ Usando tamanho padrão: {batch_size}")
    
    # Configuração da barra de progresso
    show_progress_input = input("Exibir barra de progresso? (s/n) [s]: ").strip().lower()
    show_progress = show_progress_input not in ['n', 'no', 'não']
    if show_progress:
        print("✅ Barra de progresso habilitada")
    else:
        print("✅ Barra de progresso desabilitada")
    
    # Executar conversão
    print("\n🚀 Processando arquivo JSON (modo otimizado)...")
    
    start_time = time.time()
    
    try:
        converter = JSONToSQLConverter("unidade_saude")
        sql_output = converter.convert_file(json_file_path, output_file_path, batch_size, show_progress)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Conversão concluída com sucesso!")
        print(f"📄 Arquivo SQL salvo em: {output_file_path}")
        print(f"⏱️  Tempo de processamento: {processing_time:.2f} segundos")
        
        # Mostrar estatísticas
        lines = sql_output.split('\n')
        values_count = len([line for line in lines if line.strip().startswith('(')])
        
        print(f"📊 Estatísticas:")
        print(f"   • Total de registros processados: {values_count}")
        print(f"   • Linhas no arquivo SQL: {len(lines)}")
        if processing_time > 0:
            print(f"   • Taxa de processamento: {values_count/processing_time:.0f} registros/segundo")
        
        # Perguntar se deseja visualizar uma amostra
        show_sample = input("\nDeseja visualizar uma amostra do SQL gerado? (s/n) [n]: ").strip().lower()
        if show_sample in ['s', 'sim', 'yes']:
            print("\n" + "="*60)
            print("AMOSTRA DO SQL GERADO:")
            print("="*60)
            sample_lines = lines[:20]  # Primeiras 20 linhas
            for line in sample_lines:
                print(line)
            if len(lines) > 20:
                print("...")
                print(f"[mais {len(lines) - 20} linhas no arquivo completo]")
    
    except Exception as e:
        print(f"❌ Erro durante a conversão: {e}")
        return
    
    print("\n🎉 Processo finalizado!")

def run_example():
    """
    Executa um exemplo de demonstração com dados fictícios.
    """
    print("="*60)
    print("    EXEMPLO DE DEMONSTRAÇÃO COM BARRA DE PROGRESSO")
    print("="*60)
    
    # Dados de exemplo baseados na estrutura fornecida
    exemplo_dados = [
        {
            "codigo_cnes": 9514104,
            "numero_cnpj_entidade": None,
            "nome_razao_social": "EDUARDO LUIZ SILVA DOS SANTOS",
            "nome_fantasia": "LABORATORIO VIDA FILIAL THEOBROMA",
            "natureza_organizacao_entidade": None,
            "tipo_gestao": "M",
            "descricao_nivel_hierarquia": None,
            "descricao_esfera_administrativa": None,
            "codigo_tipo_unidade": 39,
            "codigo_cep_estabelecimento": "76866000",
            "endereco_estabelecimento": "13 DE FEVEREIRO",
            "numero_estabelecimento": "1212",
            "bairro_estabelecimento": "SETOR 01",
            "numero_telefone_estabelecimento": "69 35212811",
            "latitude_estabelecimento_decimo_grau": -10.2446755608064,
            "longitude_estabelecimento_decimo_grau": -62.3508238792419,
            "endereco_email_estabelecimento": "estilocontabil.jaru@hotmail.com",
            "numero_cnpj": "15252308000282",
            "codigo_identificador_turno_atendimento": "03",
            "descricao_turno_atendimento": "ATENDIMENTOS NOS TURNOS DA MANHA E A TARDE",
            "estabelecimento_faz_atendimento_ambulatorial_sus": "SIM",
            "codigo_estabelecimento_saude": "1101609514104",
            "codigo_uf": 11,
            "codigo_municipio": 110160,
            "descricao_natureza_juridica_estabelecimento": "2305",
            "codigo_motivo_desabilitacao_estabelecimento": "10",
            "estabelecimento_possui_centro_cirurgico": 0,
            "estabelecimento_possui_centro_obstetrico": 0,
            "estabelecimento_possui_centro_neonatal": 0,
            "estabelecimento_possui_atendimento_hospitalar": 0,
            "estabelecimento_possui_servico_apoio": 1,
            "estabelecimento_possui_atendimento_ambulatorial": 0,
            "codigo_atividade_ensino_unidade": "04",
            "codigo_natureza_organizacao_unidade": None,
            "codigo_nivel_hierarquia_unidade": None,
            "codigo_esfera_administrativa_unidade": None,
            "data_atualizacao": "2025-04-06"
        }
    ]
    
    # Criar dados de exemplo maiores para demonstrar a barra de progresso
    exemplo_dados_grandes = exemplo_dados * 500  # 500 registros para demonstrar
    
    converter = JSONToSQLConverter("unidade_saude")
    
    print("SQL GERADO (MODO BULK - COM BARRA DE PROGRESSO):")
    print("-" * 60)
    sql_resultado = converter.convert_json_to_sql(exemplo_dados_grandes, show_progress=True)
    
    # Mostrar apenas as primeiras linhas
    lines = sql_resultado.split('\n')
    for i, line in enumerate(lines[:15]):
        print(line)
    print(f"... [total de {len(lines)} linhas]")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--exemplo":
        run_example()
    else:
        main()
