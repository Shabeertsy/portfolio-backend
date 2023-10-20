# build_files.sh
pip install --upgrade pip
pip install -r requirements.txt

# make migrations
python3.9 manage.py migrate 
python manage.py collectstatic --noinput

