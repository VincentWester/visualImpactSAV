sudo apt install python3

sudo apt install python-pip

sudo apt install postgresql postgresql-contrib
#A partir de cette ligne, veuillez créer un user mot de passe et une database dont 
#vous reporterez les valeurs dans le fichiers settings.py de l'application.

sudo apt install virtualenv

pip install virtualenvwrapper

export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
source ~/.local/bin/virtualenvwrapper.sh

echo "" >> ~/.bashrc
echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
echo "~/.local/bin/virtualenvwrapper.sh" >> ~/.bashrc

mkvirtualenv visualImpactSAV

workon visualImpactSAV

pip install django
pip install psycopg2 psycopg2-binary
pip install django-widget-tweaks
pip install pillow
pip install reportlab


