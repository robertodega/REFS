
#       General 
#       -------
alias note='xdg-open '
alias rootDir='clear && cd ~'
alias aliases='nano ~/.bash_aliases'
alias x='exit'
alias bashmem='source ~/.bashrc'
alias lsla='clear && pwd && ls -la'

#       GIT
#       ---
alias gitBranch='clear && git branch'
alias gitStatus='gitBranch && git status'
alias gitAdd='clear && git add .'
alias gitCommit='clear && git commit -m'
alias gitPush='clear && git push'
alias gitLog='clear && git log'
alias gitNewBranch='clear && git checkout -b '

#       LAMPP
#       -----
alias lamppUp='clear && apacheStop && sudo /opt/lampp/lampp start'
alias lamppDown='clear && sudo /opt/lampp/lampp stop'
alias lamppRestart='clear && sudo /opt/lampp/lampp restart'
alias lamppReload='clear && sudo /opt/lampp/lampp reload'
alias lamppStatus='clear && sudo /opt/lampp/lampp status'
alias apacheStop='clear && sudo systemctl stop apache2'

#	LARAVEL
#	-------
alias laravel='clear && composer create-project laravel/laravel '

#	PYTHON
#	------
alias python='clear && source venv/bin/activate && python3 app.py'

#	POSTMAN
#	-------
alias postman='clear && /opt/lampp/htdocs/WWW/Postman/Postman'

#	MYSQL
#	-----
alias mysql='clear && mysql -h 127.0.0.1 -u root -p'

#       POSTGRESQL
#       ---------
alias posgresConf='clear && sudo nano /etc/postgresql/14/main/postgresql.conf'
alias postgresConnect='clear && sudo -i -u postgres'
alias postgresStatus='clear && sudo systemctl status postgresql'
alias postgresRestart='clear && sudo systemctl restart postgresql'

