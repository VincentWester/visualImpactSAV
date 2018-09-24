sudo apt install python3

sudo apt install python-pip

sudo apt install postgresql postgresql-contrib
# A partir de cette ligne, veuillez créer un user mot de passe et une database dont
# vous reporterez les valeurs dans le fichiers settings.py de l'application.

sudo apt install python-virtualenv

pip install virtualenvwrapper

export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME

filepath="~/.local/bin/virtualenvwrapper.sh"

if ! [ -f "$filepath" ]
then
    filepath="/usr/local/bin/virtualenvwrapper.sh"
fi

source $filepath

echo "" >> ~/.bashrc
echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
echo "$filepath" >> ~/.bashrc

mkvirtualenv visualImpactSAV

workon visualImpactSAV

pip install django
pip install psycopg2 psycopg2-binary
pip install django-widget-tweaks
pip install pillow
pip install reportlab
pip install django-environ
pip install flake8


