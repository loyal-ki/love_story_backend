source ~/.bash_profile
cd source/love_story_backend
cd ./migrations

if [ "$1" = "init" ]; then
  python manage.py version_control
fi

if [ "$1" = "" ]; then
  python manage.py upgrade
fi