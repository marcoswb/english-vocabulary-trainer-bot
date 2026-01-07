# English Vocabulary Trainer Bot

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Postgres](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

🔤 **English Vocabulary Trainer Bot** é um bot do Telegram focado no aprendizado contínuo de vocabulário em inglês, combinando **Spaced Repetition (SRS)**, quizzes progressivos e **suporte a áudio (TTS)** para treino de pronúncia.

O projeto foi pensado para simular a experiência de aplicativos profissionais de idiomas, mas de forma open-source e extensível.

---

## ✨ Principais funcionalidades

- 🤖 Bot do Telegram para estudo diário
- 🧠 Algoritmo de **Spaced Repetition (SRS)**
- 🔊 **Text-to-Speech (TTS)** para treino de pronúncia
- 📚 Banco de dados com palavras, frases e estados de aprendizado
- 📊 Dificuldade progressiva baseada no desempenho do usuário
- ⏰ Envio automático diário via **GitHub Actions**
- 🔁 Suporte a verbos irregulares e variações verbais

---

## 🎯 Objetivo

Ajudar no aprendizado diário de vocabulário em inglês através de quizzes inteligentes, com:

- traduções e frases contextualizadas
- exercícios adaptados ao nível do usuário
- feedback imediato de acerto ou erro
- reforço auditivo com pronúncia correta
- agendamento automático de revisões

---

## 🔊 Suporte a TTS (Text-to-Speech)

O bot possui suporte a **TTS (Text-to-Speech)** para reforçar o aprendizado da **pronúncia correta das palavras em inglês**.

O comportamento do áudio varia conforme o tipo de pergunta:

### 🟢 Inglês → Português
Quando a pergunta solicita a tradução de uma palavra do **inglês para o português**:

- o bot envia automaticamente o **áudio da palavra em inglês**
- em seguida, apresenta a pergunta com as alternativas

👉 O usuário **ouve a palavra antes de responder**, treinando compreensão auditiva (*listening*).

### 🔵 Outros tipos de pergunta (ex: Português → Inglês)
Quando a pergunta não exige escuta prévia:

- o bot envia apenas a pergunta inicialmente
- **após o usuário responder**, o áudio TTS da palavra correta é enviado

👉 O áudio atua como **reforço de aprendizado**, mesmo após a resposta.

### 🎧 Benefícios pedagógicos

- melhora da pronúncia
- associação entre escrita e som
- desenvolvimento de escuta ativa
- maior retenção de vocabulário

---

## 🧱 Estrutura do Projeto

| Componente            | Descrição                                                            |
|----------------------|----------------------------------------------------------------------|
| `.github/workflows`  | Automação de envio diário (GitHub Actions)                           |
| `data/`              | Arquivos de vocabulário e frases para carga no banco                 |
| `resource/`          | Scripts SQL de estrutura e dados iniciais                            |
| `src/`               | Código-fonte principal do bot                                        |
| `main.py`            | Inicialização do bot                                                 |
| `insert_vocab.py`    | Script para inserção de vocabulários no banco                        |

---

## 📈 Spaced Repetition System (SRS)

O bot utiliza um algoritmo de **Spaced Repetition**, semelhante aos usados em plataformas profissionais de ensino de idiomas.

Com base no desempenho do usuário (acertos, erros, streak e confiança), o sistema define quando cada palavra deve ser revisada novamente, garantindo que o aprendizado avance apenas quando o conteúdo foi realmente assimilado.

---

## 🔁 Verbos irregulares e variações verbais

O projeto conta com um algoritmo específico para aprendizado completo de verbos, incluindo:

- verbos regulares e irregulares
- diferentes tempos verbais (ex: infinitive, simple past, past continuous)
- frases contextualizadas

O usuário pode cadastrar o verbo na forma infinitiva e o bot espera automaticamente a forma verbal correta com base no contexto da frase apresentada.

---

## 🛠️ Como usar / Setup

### 1. Clonar o repositório
```bash
git clone https://github.com/marcoswb/english-vocabulary-trainer-bot.git
cd english-vocabulary-trainer-bot
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
API_ID=<api_id do Telegram>
API_HASH=<api_hash do Telegram>
TOKEN_BOT=<token do bot>
DB_HOST=<host do banco>
DB_DATABASE=<nome do banco>
DB_USER=<usuario do banco>
DB_PASSWORD=<senha do banco>
AUTHORIZED_USER_ID=<id do usuário autorizado no Telegram>
```

### 3. Execução via GitHub Actions

O workflow `daily_bot.yml` é responsável pelo envio automático do quiz.

- pode ser executado manualmente
- roda automaticamente todos os dias às **12:30 (horário de Brasília)**

Para funcionar corretamente, basta configurar as mesmas variáveis do `.env` como **Secrets do repositório no GitHub**.

---

## 📊 Exemplos

### Quiz enviado ao usuário

O quiz evolui conforme o nível de aprendizado:
- inicia com traduções simples
- avança para completar frases
- dicas são fornecidas nos níveis iniciais
- conforme o domínio aumenta, as dicas diminuem

Vídeo de demonstração:

https://github.com/user-attachments/assets/bcc1e839-71c8-4dd2-8ad1-2c55bab9a4f2

---

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
