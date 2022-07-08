echo "Flask migrate message: "
read message

FLASK_APP=theatre python -m flask db migrate --message "$message"
FLASK_APP=theatre python -m flask db upgrade
