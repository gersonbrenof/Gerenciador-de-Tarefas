## Instalação

### 1. Clone o repositório:

```bash
git clone https://github.com/gersonbrenof/Gerenciador-de-Tarefas.git)
cd tarefas-api
python -m venv venv
source venv/bin/activate   # Para sistemas Linux/Mac
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
