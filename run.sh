mkdir -p static staticroot
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --verbosity=0
echo "========================================="
python3 manage.py runserver
