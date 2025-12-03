# 🐾 Pet Maniacos | Sistema de Gerenciamento de Pet Shop & Clínica Veterinária

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap)](https://getbootstrap.com/)

Um sistema completo para gestão de clínicas veterinárias e pet shops, desenvolvido em Python com o framework Django.  
O **Pet Maniacos** gerencia cadastro de tutores, pets, agendamentos, serviços e histórico de saúde dos animais.

---

## 🌟 Recursos Principais

- **Gestão de Clientes (Tutores):** Cadastro, edição e histórico dos responsáveis pelos pets.
- **Gestão de Pets:** Registro detalhado dos animais com informações médicas.
- **Agendamentos:** Interface amigável para consultas, banho e tosa, com visualização intuitiva.
- **Serviços:** Cadastro e gerenciamento de serviços oferecidos pela clínica ou pet shop.
- **Controle de Acesso:** Painel administrativo (`/admin`) e permissões por cargo.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologias |
|--------|-------------|
| Backend | Python 3.10+, Django 4.2+ |
| Banco de Dados | SQLite (dev) / PostgreSQL (produção recomendado) |
| Frontend | HTML5, CSS3, JavaScript |
| Estilização | Bootstrap 5.3+ |
| Ícones | Font Awesome 6.5+ |

---

## 🚀 Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para rodar o projeto localmente.

### 🔹 1. Clonar o Repositório

```bash
git clone https://github.com/rodrigo12crt/PetManiacos.git
```

### 🔹 2. Criar e Ativar o Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv
```

```bash
# Ativar no Windows
.\venv\Scripts\activate

# Ativar no Linux / macOS
source venv/bin/activate
```

### 🔹 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 🔹 4. Configuração Inicial do Django

```bash
📌 Aplicar migrações:

python manage.py migrate
python manage.py makemigrations

📌 Criar superusuário:

python manage.py createsuperuser
```

### 🔹 5. Rodar o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em:

http://127.0.0.1:8000/

📂 Estrutura do Projeto
```bash
DAYCARE/
├── app/                   # App principal (home, dashboard)
├── tutores/               # App de Tutores e Pets
├── services/              # App de Serviços e Agendamentos
├── templates/             # Templates HTML compartilhados
├── static/                # Arquivos estáticos (img, css, js)
├── daycare/               # Configurações do projeto
├── manage.py
├── requirements.txt
└── README.md
```

📄 Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo LICENSE para mais informações.
