# Filename: auto_setup.sh
# Auteur: Chao
# But: pour deployer automatiquement l'application de upload 
echo auto deployement de l\'application Django de upload

# installation pytz
sudo easy_install pytz-2015.4-py2.4.egg
 
mkdir -p ~/ENV/tutorial/
cp -avr ../mysite ~/ENV/tutorial/
install_dir=$(pwd)

# installation pip, pour faciliter l'installation suivant
echo "*************"
echo installer pip
echo "*************"
sudo apt-get install python-pip
echo "*************"
echo pip fin
echo "*************"


# installation virtualenv
echo "********************"
echo installer virtualenv
echo "********************"
pip install virtualenv
echo "********************"
echo virtualenv fin
echo "********************"


# installation ngnix
echo "********************"
echo installer ngnix
echo "********************"
sudo apt-get install nginx
echo "********************"
echo ngnix fin
echo "********************"


# configuration sur ngnix
sudo mkdir -p /etc/nginx/sites-available/tmp
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/tmp
sudo cp $install_dir/default /etc/nginx/sites-available/


# installation gunicorn
virtualenv ~/ENV/tutorial/
echo "********************"
echo virtualenv fini
echo "********************"
cd ~/ENV/tutorial/
cdir=$(pwd)


pwd
source bin/activate
echo "********************"
echo activate fini
echo "********************"

echo "installation de Django"
pip install Django==1.8.3
echo "installation de gunicorn"
pip install gunicorn
echo First /test
cd mysite 


# Installation de supervisor
sudo apt-get install supervisor
sudo rm /etc/supervisor/conf.d/django_upload_application.conf
sudo cp $install_dir/django_upload_application.conf /etc/supervisor/conf.d/ 

# test 
cat /tmp/django_upload_application.conf

sudo supervisorctl update
sudo supervisorctl status
sudo /etc/init.d/nginx restart









