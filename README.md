# 🏥 SQL Script Automator - Conversor JSON para SQL

Um conversor otimizado e eficiente que transforma arquivos JSON de unidades de saúde em comandos SQL INSERT para bancos de dados relacionais.

## ⚡ Início Rápido (5 minutos)

**Quer rodar AGORA? Siga estes 4 passos:**

1. **📥 Instale o Python** (se não tiver):

   - Vá em [python.org/downloads](https://www.python.org/downloads/)
   - Baixe e instale - **CRÍTICO: Marque "Add Python to PATH"!**

2. **📂 Baixe este projeto**:

   - **Opção fácil**: Baixe ZIP do GitHub e extraia
   - **Opção avançada**: `git clone https://github.com/seu-usuario/sql_script_automator.git`

3. **💻 Abra terminal na pasta** do projeto:

   - **Windows**: Shift + Clique direito na pasta → "Abrir PowerShell aqui"
   - **Mac/Linux**: Abra Terminal e use `cd` para navegar

4. **🚀 Execute o programa**:

   ```bash
   # Para ver exemplo funcionando (recomendado primeiro)
   python sql_script_automator.py --exemplo

   # Para usar com seus próprios dados JSON
   python sql_script_automator.py
   ```

**✅ Funcionou? Parabéns! 🎉**  
**❌ Não funcionou? Veja [resolução rápida](#-resolução-rápida---problemas-comuns) abaixo.**

## 📋 Descrição

Este projeto foi desenvolvido para automatizar a conversão de grandes volumes de dados de unidades de saúde (formato JSON) em comandos SQL INSERT otimizados. O conversor inclui funcionalidades avançadas como:

- ✅ **Barra de progresso visual** para acompanhar o processamento
- ✅ **Processamento em lotes** para arquivos grandes
- ✅ **Otimização de memória** usando StringIO e bufferização
- ✅ **Formatação automática de dados** (datas, strings, números, booleanos)
- ✅ **Tratamento de valores nulos** e caracteres especiais
- ✅ **Escape automático** de aspas simples em strings
- ✅ **Campos específicos** para unidades de saúde do CNES (Cadastro Nacional de Estabelecimentos de Saúde)

## 🎯 Características Principais

- **Performance otimizada**: Processamento rápido de arquivos grandes (testado com 300k+ registros)
- **Interface amigável**: Menu interativo com opções claras
- **Flexibilidade**: Configuração de tamanho de lotes e opções de progresso
- **Robustez**: Tratamento de erros e validação de entrada
- **Compatibilidade**: Funciona com diferentes SGBDs (MySQL, PostgreSQL, SQL Server, etc.)

## 🔧 Requisitos do Sistema

### Pré-requisitos

- **Python 3.7 ou superior**
- **Sistema Operacional**: Windows, macOS ou Linux
- **Memória RAM**: Mínimo 4GB (recomendado 8GB para arquivos grandes)
- **Espaço em disco**: Espaço suficiente para o arquivo de saída (aproximadamente 2-3x o tamanho do JSON)

### Dependências Python

O projeto utiliza apenas bibliotecas padrão do Python:

- `json` - Para leitura de arquivos JSON
- `re` - Para expressões regulares
- `time` - Para medição de tempo e barra de progresso
- `datetime` - Para formatação de datas
- `typing` - Para type hints
- `io.StringIO` - Para otimização de memória

## 📥 Instalação e Configuração

### 1. Instalar o Python (Se Necessário)

**🪟 Windows:**

1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe a versão mais recente (3.7+)
3. **IMPORTANTE**: Durante a instalação, marque "Add Python to PATH"
4. Execute como administrador se necessário

**🐧 Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3 python3-pip
```

**🍎 macOS:**

```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python
```

### 2. Clone o Repositório

**Opção A: Via Git (Recomendado)**

```bash
# Via HTTPS (funciona sempre)
git clone https://github.com/seu-usuario/sql_script_automator.git

# Via SSH (se você tem chave SSH configurada)
git clone git@github.com:seu-usuario/sql_script_automator.git
```

**Opção B: Download Direto**

1. Acesse a página do projeto no GitHub
2. Clique no botão verde "Code"
3. Selecione "Download ZIP"
4. Extraia o arquivo ZIP em uma pasta de sua escolha

### 3. Navegue até o Diretório

```bash
# Windows (PowerShell/CMD)
cd sql_script_automator

# Linux/macOS (Terminal)
cd sql_script_automator
```

### 4. Verifique a Instalação do Python

```bash
# Testar Python - tente estas opções na ordem:

# Opção 1 (mais comum)
python --version

# Opção 2 (Linux/macOS)
python3 --version

# Opção 3 (Windows com Python Launcher)
py --version
```

**Se aparecer algo como `Python 3.8.5` ou superior, está tudo certo!**

**❌ Se aparecer erro "comando não encontrado":**

- **Windows**: Reinstale o Python marcando "Add to PATH"
- **Linux**: Execute `sudo apt install python3`
- **macOS**: Execute `brew install python`

### 5. Verificação dos Arquivos

Certifique-se de que os seguintes arquivos estão presentes:

```
sql_script_automator/
├── sql_script_automator.py           # Script principal
├── exemplo_unidades_saude.json       # Arquivo de exemplo (3 registros)
├── README.md                         # Este arquivo
├── .gitignore                        # Configuração Git
└── __pycache__/                      # Cache do Python (gerado automaticamente)
```

**📁 Arquivos de dados:**

- `exemplo_unidades_saude.json` - Arquivo pequeno com 3 registros para testes
- `unidades_de_saude.json` - Arquivo grande (15MB, 328k registros) - não incluído no Git por ser muito grande

### 6. Teste Rápido (Opcional)

Para verificar se tudo está funcionando:

```bash
# Teste o script com dados de exemplo
python sql_script_automator.py --exemplo

# OU teste com o arquivo de exemplo incluído
python sql_script_automator.py
# Quando solicitar o arquivo, digite: exemplo_unidades_saude.json
```

**Se você ver uma barra de progresso e SQL sendo gerado, está tudo pronto! 🎉**

## 🚀 Como Usar

### Modo Interativo (Recomendado)

1. **Execute o script principal:**

```bash
# Tente estas opções (na ordem) até uma funcionar:

# Opção 1 - Mais comum
python sql_script_automator.py

# Opção 2 - Linux/macOS
python3 sql_script_automator.py

# Opção 3 - Windows com Python Launcher
py sql_script_automator.py
```

2. **Siga as instruções do menu:**
   - Digite o caminho do arquivo JSON de entrada
   - Confirme ou altere o nome do arquivo SQL de saída
   - Configure o tamanho do lote (padrão: 1000 registros)
   - Escolha se deseja ver a barra de progresso
   - Aguarde o processamento

### Modo de Demonstração

Para ver um exemplo funcionando (sem precisar de arquivo JSON):

```bash
python sql_script_automator.py --exemplo
```

### ⚡ Exemplo Completo - Do Zero ao SQL

**Passo 1**: Abra o terminal/prompt de comando na pasta do projeto

**Passo 2**: Execute o programa

```bash
python sql_script_automator.py
```

**Passo 3**: Interaja com o programa (exemplo real):

```bash
# 1. Execute o programa
python sql_script_automator.py

# 2. Interface será apresentada:
============================================================
    CONVERSOR JSON PARA SQL - UNIDADES DE SAÚDE
        VERSÃO OTIMIZADA COM BARRA DE PROGRESSO
============================================================

# 3. Digite o caminho do seu arquivo JSON
Digite o caminho do arquivo JSON de entrada: unidades_de_saude.json

# 4. Confirme o arquivo de saída
Arquivo de saída sugerido: unidades_de_saude_insert.sql
Deseja usar este nome? (s/n) [s]: s

# 5. Configure as opções (ou use padrões)
⚡ CONFIGURAÇÕES DE PERFORMANCE:
Tamanho do lote (padrão: 1000) [Enter para usar padrão]:
Exibir barra de progresso? (s/n) [s]: s

# 6. Aguarde o processamento com barra de progresso
🚀 Processando arquivo JSON (modo otimizado)...
🔄 Carregando arquivo JSON...
✅ Arquivo carregado: 150000 registros
🔄 Convertendo para SQL (com barra de progresso)...
Processando lotes: |████████████████████████████████| 150/150 (100.0%) ⏱️ 2m 30s | ETA: 0s
```

## 📊 Estrutura dos Dados

### Campos Suportados

O conversor processa os seguintes campos específicos de unidades de saúde:

| Campo                                   | Tipo    | Descrição                     |
| --------------------------------------- | ------- | ----------------------------- |
| `codigo_cnes`                           | INTEGER | Código CNES da unidade        |
| `numero_cnpj_entidade`                  | VARCHAR | CNPJ da entidade mantenedora  |
| `nome_razao_social`                     | VARCHAR | Razão social da unidade       |
| `nome_fantasia`                         | VARCHAR | Nome fantasia                 |
| `natureza_organizacao_entidade`         | VARCHAR | Natureza da organização       |
| `tipo_gestao`                           | CHAR    | Tipo de gestão (M/E/D)        |
| `codigo_cep_estabelecimento`            | VARCHAR | CEP do estabelecimento        |
| `endereco_estabelecimento`              | VARCHAR | Endereço completo             |
| `latitude_estabelecimento_decimo_grau`  | DECIMAL | Latitude geográfica           |
| `longitude_estabelecimento_decimo_grau` | DECIMAL | Longitude geográfica          |
| `data_atualizacao`                      | DATE    | Data da última atualização    |
| ...                                     | ...     | E mais 25+ campos específicos |

### Exemplo de Entrada (JSON)

```json
[
  {
    "codigo_cnes": 9514104,
    "numero_cnpj_entidade": null,
    "nome_razao_social": "EDUARDO LUIZ SILVA DOS SANTOS",
    "nome_fantasia": "LABORATORIO VIDA FILIAL THEOBROMA",
    "tipo_gestao": "M",
    "codigo_cep_estabelecimento": "76866000",
    "endereco_estabelecimento": "13 DE FEVEREIRO",
    "data_atualizacao": "2025-04-06"
  }
]
```

### Exemplo de Saída (SQL)

```sql
INSERT INTO unidade_saude (
  codigo_cnes,
  numero_cnpj_entidade,
  nome_razao_social,
  nome_fantasia,
  tipo_gestao,
  codigo_cep_estabelecimento,
  endereco_estabelecimento,
  data_atualizacao
)
VALUES
(9514104, NULL, 'EDUARDO LUIZ SILVA DOS SANTOS', 'LABORATORIO VIDA FILIAL THEOBROMA', 'M', '76866000', '13 DE FEVEREIRO', '2025-04-06');
```

## ⚙️ Configurações Avançadas

### Tamanho dos Lotes

Para arquivos muito grandes, você pode ajustar o tamanho dos lotes:

- **Pequenos (100-500)**: Para bancos com limitações de memória
- **Médios (1000-2000)**: Padrão recomendado
- **Grandes (5000+)**: Para máquinas potentes e bancos robustos

### Desempenho

**Para arquivos pequenos (< 10k registros):**

- Processamento instantâneo
- Uso de memória mínimo

**Para arquivos médios (10k-100k registros):**

- Processamento em 10-60 segundos
- Barra de progresso ativa
- Uso moderado de memória

**Para arquivos grandes (100k+ registros):**

- Processamento em lotes automático
- Monitoramento de progresso detalhado
- Otimização de memória ativa

## 🔍 Solução de Problemas

### Problemas Comuns

#### 1. Erro: "Arquivo não encontrado"

```bash
❌ Arquivo não encontrado: arquivo.json
```

**Solução**: Verifique se o caminho está correto e o arquivo existe.

#### 2. Erro: "Erro ao decodificar JSON"

```bash
❌ Erro ao decodificar JSON: Expecting ',' delimiter
```

**Solução**: Verifique se o arquivo JSON está bem formatado usando um validador online.

#### 3. Python não encontrado

```bash
'python' is not recognized as an internal or external command
```

**Solução**:

- Instale o Python do site oficial
- Adicione Python ao PATH do sistema
- Use `python3` em vez de `python`

#### 4. Memória insuficiente

```bash
MemoryError: Unable to allocate array
```

**Solução**:

- Reduza o tamanho do lote
- Processe o arquivo em partes menores
- Aumente a memória RAM disponível

## 🚨 Resolução Rápida - Problemas Comuns

**❌ "python não é reconhecido como comando"**

```bash
# Windows: Tente estas alternativas
py sql_script_automator.py
python3 sql_script_automator.py

# Se nada funcionar, reinstale o Python marcando "Add to PATH"
```

**❌ "Arquivo não encontrado"**

```bash
# Verifique se está na pasta correta
ls          # Linux/macOS
dir         # Windows

# Deve aparecer: sql_script_automator.py
```

**❌ "Permission denied" ou "Acesso negado"**

```bash
# Linux/macOS: Adicione permissão
chmod +x sql_script_automator.py

# Windows: Execute como administrador
```

---

### Dicas de Performance

1. **Para arquivos grandes**: Use lotes de 1000-2000 registros
2. **Para máquinas lentas**: Desabilite a barra de progresso
3. **Para SSDs**: Tamanhos de lote maiores funcionam melhor
4. **Para HDDs**: Prefira lotes menores

## 🤝 Contribuindo

### Como Contribuir

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Padrões de Código

- Use **type hints** em todas as funções
- Mantenha **docstrings** atualizadas
- Siga o padrão **PEP 8**
- Adicione **testes** para novas funcionalidades

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para facilitar o trabalho com dados de saúde pública.

## 📞 Suporte

- **Issues**: Reporte bugs e solicite features no [GitHub Issues](https://github.com/seu-usuario/sql_script_automator/issues)
- **Discussões**: Participe das discussões na aba [Discussions](https://github.com/seu-usuario/sql_script_automator/discussions)

## 🔄 Atualizações

### Versão Atual: 2.0

- ✅ Barra de progresso visual
- ✅ Processamento em lotes otimizado
- ✅ Melhor tratamento de memória
- ✅ Interface de usuário aprimorada

### Próximas Versões

- 🔄 Suporte a outros formatos (CSV, XML)
- 🔄 Interface gráfica (GUI)
- 🔄 Integração direta com bancos de dados
- 🔄 Validação de dados automática

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!**

## 📚 Tutorial Completo por Sistema Operacional

### 🪟 Windows (Passo a Passo Completo)

1. **Instalar Python**:

   - Vá em https://python.org/downloads
   - Baixe a versão mais recente
   - **CRÍTICO**: Marque "Add Python to PATH" durante instalação
   - Clique "Install Now"

2. **Baixar o projeto**:

   - Baixe como ZIP do GitHub OU clone via Git
   - Extraia em uma pasta (ex: `C:\projetos\sql_script_automator`)

3. **Abrir terminal**:

   - Pressione `Win + R`, digite `cmd`, Enter
   - OU clique com botão direito na pasta → "Abrir no Terminal"

4. **Navegar até a pasta**:

   ```cmd
   cd C:\projetos\sql_script_automator
   ```

5. **Executar**:
   ```cmd
   python sql_script_automator.py
   ```

### 🐧 Linux (Ubuntu/Debian)

1. **Instalar Python** (se necessário):

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```

2. **Clonar projeto**:

   ```bash
   git clone https://github.com/seu-usuario/sql_script_automator.git
   cd sql_script_automator
   ```

3. **Executar**:
   ```bash
   python3 sql_script_automator.py
   ```

### 🍎 macOS

1. **Instalar Homebrew** (se necessário):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Instalar Python**:

   ```bash
   brew install python git
   ```

3. **Clonar e executar**:
   ```bash
   git clone https://github.com/seu-usuario/sql_script_automator.git
   cd sql_script_automator
   python3 sql_script_automator.py
   ```

## ✅ Checklist Final - Funciona em Qualquer Computador?

**Antes de usar, verifique:**

- [ ] ✅ Python 3.7+ instalado (`python --version`)
- [ ] ✅ Arquivo `sql_script_automator.py` presente na pasta
- [ ] ✅ Terminal/CMD aberto na pasta correta
- [ ] ✅ Teste básico funcionou (`python sql_script_automator.py --exemplo`)

**Se todos os itens estão marcados, você está pronto para converter qualquer arquivo JSON em SQL! 🚀**

**❗ Se algum item falhou, consulte as seções de tutorial por sistema operacional acima.**
