# Atualiza os pacotes e instala o venv para Python 3.12
sudo apt update
sudo apt install python3.12-venv

# Cria o ambiente virtual
python3.12 -m venv venv

# Ativa o ambiente
source venv/bin/activate

# Instala as dependências com versões compatíveis
pip install FreeSimpleGUI==5.1.0
pip install googletrans==4.0.0-rc1
pip install ibm-watson
pip install ibm-cloud-sdk-core