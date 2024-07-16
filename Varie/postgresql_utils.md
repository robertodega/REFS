
postgres:
	cambiare owner di <DB_NAME> a <NEW_USER>

		postgres=# ALTER DATABASE <DB_NAME> OWNER TO <NEW_USER>;

assegnare ruolo per <NEW_USER> a utente <USER>

		postgres=# GRANT CONNECT ON DATABASE <DB_NAME> TO <USER>;
		postgres=# GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO <USER>;

da terminale ubuntu
	ip address												#	indirizzo ip macchina remota ( <IP_ADDRESS> )
	
inserire alias per ip address in C:\Windows\System32\drivers\etc\hosts
	
	es.
	<IP_ADDRESS> <ALIAS_NAME>
	
	
da cmd win

	ssh <USER>@<ALIAS_NAME>										#	collegamento a macchina remota virtuale ubuntu ( ssh <IP_ADDRESS> )
	ctrl d	( o exit o x )										#	uscita da collegamento a macchina remota virtuale ubuntu
	sudo systemctl status postgresql							#	postgresql status
	sudo systemctl restart postgresql							#	postgresql service restart

	sudo nano /etc/postgresql/14/main/postgresql.conf			#	postgresql conf file
	sudo nano /etc/postgresql/14/main/pg_hba.conf				# 	host-based authentication file
	sudo nano /etc/postgresql/14/main/pg_ident.conf    			#	ident configuration file

	sudo -i -u postgres											#	collegamento a postgres@<USER>-Virtual-Machine
	psql														#	postgres terminal connection
	\l															#	list of db
	\du															#	list of roles
	create user <USER> with encrypted password '<PASSWORD>';	#	user create
	

Parametri DBeaver:

	-	Connected by: 	Host
	-	Host:			ip address macchina remota
	-	Port:			5432
	-	Database:		<DB_NAME>
	-	Username:		<USER>		( o Owner from "sudo -i -u postgres" | "psql" | "\l" )
	-	Password:		<PASSWORD>

