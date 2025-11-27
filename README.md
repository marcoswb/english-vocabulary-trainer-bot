# 📚 English Vocabulary Trainer Bot

Ferramenta pessoal em Python para aprender vocabulário em inglês utilizando:
- Telegram Bot
- Spaced Repetition (SRS)
- Exercícios intercalados
- Hints adaptativos
- Geração automática diária (GitHub Actions)

---

# 🎯 Objetivo do Projeto
Criar um bot que auxilia no aprendizado de vocabulário inglês através de quizzes diários enviados via Telegram, utilizando frases de contexto, typing ativo e repetição espaçada.

---

# 🧱 Arquitetura Geral
```
Python (Telegram Bot)
       |
       |-- SQLite (palavras, frases, streak, SRS)
       |
GitHub Actions (job diário automatizado)
       |
       |-- executa script que envia quiz do dia via Telegram
```

---

# 🗂️ Estrutura do Banco SQLite

## **Tabela: vocabulary**
Campos:
- id
- word (inglês)
- meaning (português)
- created_at

## **Tabela: training_state**
Campos:
- id
- vocab_id (FK)
- streak
- last_review
- next_review
- next_exercise_type

## **Tabela: example_sentences**
Campos:
- id
- vocab_id (FK)
- sentence (frase em inglês)

---

# 🔁 Sistema de Spaced Repetition (simples e eficiente)
Regras sugeridas:
```
Acertou  → streak += 1
Errou    → streak = 0

streak 0 → revisar hoje
streak 1 → +1 dia
streak 2 → +3 dias
streak 3 → +7 dias
streak 4 → +14 dias
streak 5 → +30 dias (revisão esporádica)
```

---

# 🎮 Tipos de Exercícios (intercalados por dia)
Cada palavra só aparece **uma vez por dia**, usando um tipo de exercício adequado ao seu nível (streak).

## **1. Inglês → Português**
- Mostra frase em inglês
- Palavra destacada
- Pergunta: *qual o significado em PT?*

## **2. Português → Inglês**
- Mostra frase traduzida para PT
- Palavra ausente
- Pergunta: *qual a palavra em inglês?*

## **3. Cloze deletion (completar palavra)**
- Palavra removida da frase
- Ex: `They want to ______ their skills.`

---

# 💡 Hints Adaptativos
Combinam:
- definição curta da palavra (em inglês)
- quantidade de letras
- opcional: primeira letra

## **Sugestão por streak:**
| streak | hint | exercício |
|--------|-------|-----------|
| 0 | definição + tamanho + primeira letra | inglês → portugês |
| 1 | definição + tamanho | português → inglês |
| 2 | definição + tamanho | cloze com hint forte |
| 3 | apenas definição | cloze com hint leve |
| 4 | sem hint | cloze puro |
| 5 | revisão ocasional | qualquer tipo |

---

# 🕒 Gatilho Diário com GitHub Actions
O GitHub Actions executa um script Python diariamente para:
1. Acessar o banco SQLite
2. Determinar as palavras do dia
3. Gerar os exercícios
4. Enviar via Telegram

Exemplo de workflow:
```yaml
name: Daily Quiz

on:
  schedule:
    - cron: '0 11 * * *'  # ~08:00 Brasil (ajustar)
  workflow_dispatch:

jobs:
  quiz:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install python-telegram-bot requests

      - name: Run quiz script
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python daily_quiz.py
```

---

# 🔗 APIs para Buscar Frases e Definições

## ⭐ **Lingua Robot API** (frases + definições)
https://www.linguarobot.com/

Endpoint exemplo:
```
GET https://lingua-robot.p.rapidapi.com/language/v1/entries/en_US/<word>
```

---

## ⭐ **WordsAPI**
https://www.wordsapi.com/

Disponível também via RapidAPI.

---

# 📌 Fluxo Diário do Usuário
1. Bot envia primeiro exercício do dia
2. Usuário responde
3. Bot verifica acerto/erro
4. atualiza streak + próxima revisão
5. envia próximo exercício (ou finaliza)

---

# 🧩 Lógica de Seleção de Exercício por streak
```
if streak == 0: ingles→portugues
elif streak == 1: portugues→ingles
elif streak == 2: cloze + hint forte
elif streak == 3: cloze + hint leve
elif streak >= 4: cloze sem hint
```

---

# 🚀 Próximos Passos de Implementação
1. Criar estrutura do banco SQLite
2. Implementar módulo SRS
3. Criar funções para geração de exercícios
4. Implementar hints adaptativos
5. Criar bot do Telegram
6. Criar script diário (daily_quiz.py)
7. Configurar GitHub Actions

---

# 📦 Objetivo Final
Criar um sistema totalmente automatizado que envia quizzes diários personalizados baseado na dificuldade e domínio real de cada palavra.

---

Caso queira expandir este projeto:
- suporte a áudio TTS das frases
- dashboard web simples
- estatísticas de performance
- exportação CSV/JSON do vocabulário

