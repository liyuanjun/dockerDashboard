#! /bin/bash
#
# king-aric

start_server(){
  if [ ! -d ~/log ]
  then
    mkdir ~/log
  fi  
  sudo python manage.py runserver  0.0.0.0:10086 --insecure >~/log/dockerdashboard 2>&1&
}
start_server


