# English Vocabulary Trainer Bot

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)  
[![Postgres](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  

🔤 **English Vocabulary Trainer Bot** é uma ferramenta para aprender vocabulário em inglês de forma automatizada, inteligente e baseada em **Spaced Repetition (SRS)**.

Este projeto combina:
- 👨‍💻 **Telegram Bot** para interação conversacional
- 📚 Banco de dados com vocabulário, exemplos e estados de revisão
- 🧠 Algoritmo SRS para revisar palavras no momento ideal
- 🗓️ **GitHub Actions** para envio diário de quizzes

---

## 📌 Objetivo

Criar um sistema automatizado que ajude no aprendizado diário de vocabulário em inglês por meio de quizzes, com:
- frases de contexto relevantes
- exercícios adaptados ao nível do usuário
- feedback de acerto/erro
- programação diária de envio

---

## 🧱 Estrutura do Projeto

| Componente          | Descrição                                   |
|---------------------|---------------------------------------------|
| `.github/workflows` | Automação de envio diário                   |
| `data/`             | Arquivos texto de vocabulário / frases      |
| `resource/`         | Arquivos .sql de estrutura do banco de dados | 
| `src/`              | Código principal do bot                     |
| `main.py`           | Inicialização do bot                        |

---

## 📈 Spaced Repetition System (SRS)

Este bot usa uma lógica SRS(assim como os algoritmos dos principais cursos de inglês do mercado) para decidir quando cada palavra deve aparecer novamente para aprendizado, ajustando os dias conforme o desempenho do usuário (streak + confidence), garantindo assim que o usuário só irá para o próximo nível do quiz quando realmente tiver aprendido a nova palavra.

---

## 🛠 Como usar / Setup  

### 1. Clone o repositório  
```bash
git clone https://github.com/marcoswb/english-vocabulary-trainer-bot.git
cd english-vocabulary-trainer-bot
```

### 2. Configure variáveis de ambiente  
Crie um arquivo `.env` na raiz do projeto com as credenciais para envio de mensagens no telegram e de acesso ao banco de dados:  
```env
API_ID=<chave do bot(gerado pelo telegram)>
API_HASH=<hash do bot(gerado pelo telegram)>
TOKEN_BOT=<token do bot(gerado pelo telegram)>
DB_HOST=<host do banco de dados>
DB_DATABASE=<nome do banco de dados>
DB_USER=<usuario do banco de dados>
DB_PASSWORD=<senha do banco de dados>
AUTHORIZED_USER_ID=<id do usuário(no telegram) com quem o bot irá se comunicar>
```

### 3. Iniciar script com GitHub Actions
Esse projeto possui o arquivo `daily_bot.yml` que é responsável por executar o scraper via [Github Actions](https://github.com/features/actions), ele está configurado para ser executado manualmente quando o usuário desejar e também via cron(agendador de tarefas) todos os dias as 12:15(horário de Brasília).

Para que a Action funcione corretamente basta configurar as mesmas variáveis de ambiente descritas no item 2 como [secrets do projeto github](https://docs.github.com/en/actions/concepts/security/secrets), com isso ela já estará agendada para executar todos os dias e você já pode testar também pois esse fluxo permite a execução manual da Action sempre que necessário.

---

## 📊 Exemplos / Resultados  

### Quiz inicial que o usuário recebe
<img width="686" height="669" alt="image" src="https://github.com/user-attachments/assets/01c18862-c5ec-461e-b55f-5d9266c7235e" />



---

## 📝 Licença  

Este projeto está licenciado sob a [MIT License](LICENSE).  


