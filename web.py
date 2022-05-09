#!/usr/bin/env python3

import os, sys, time, random


def main():

	ipm = os.popen("hostname -I").read()
	user = os.popen("echo $USER").read()

	print(f'''

Very basic configuration, only master DNS will be configured here.


		 _       ____________ 
		| |     / / ____/ __ )
		| | /| / / __/ / __  |
		| |/ |/ / /___/ /_/ / 
		|__/|__/_____/_____/


Connected as : {user}
Your ip is : {ipm}

							Credit : LoKy


	Options :

		[+] 1 - Download requirements and basic configuration
		[+] 2 - Create DNS
		[+] 3 - Create RSA key for your websites
		[+] 4 - Create apache website with TLS (Option 3 recommended)

		[+] 5 - Tests (new console)
		[+] 6 - Delete a VHost and attached items
		[+] 7 - Remove a user from the .htpasswd file

		[-] 0 - Exit

		''')



def test():
	print('''

		  ______          __
		 /_  __/__  _____/ /______
		  / / / _ \/ ___/ __/ ___/
		 / / /  __(__  ) /_(__  ) 
		/_/  \___/____/\__/____/ 


		[+] 1 - dig ns + dns
		[+] 2 - dig a  + website
		[+] 3 - Check logs after restart bind9
		[-] 0 - Exit
''')

	numero2 = int(input("Choose an option : "))

	if numero2 == 1:

		os.system("ls /etc/bind | grep db.*")
		dnstest = input("\nWhat DNS would you like to test : ")
		response = os.system(f"dig ns {dnstest} | grep ns1.*")
		print("\n")
		test()

	if numero2 == 2:
		print("\nSites in /home/sites/")
		os.system("ls -l /home/sites/")
		site = input("\nEnter <website>.<dns_name> (ex : intranet.mydomain.com) : ")
		os.system(f"dig a {site} @localhost")
		enter = input("Press Enter to continue : ")
		if not enter :
			test()
		else :
			test()


	if numero2 == 3:
		os.system("systemctl restart bind9 && tail -20 /var/log/syslog")
		test()

	if numero2 == 0:
		 return 0;


def choix():

	numero = int(input("Choose an option : "))


	if numero == 0:
		sys.exit()


	if numero == 1:
		os.system("apt install -y bind9 openssl bind9utils dnsutils apache2")
		os.system("a2enmod ssl")
		os.system("a2enmod userdir")
		print("\n")

		print('Writing "servername localhost" in /etc/apache2/apache2.conf')
		with open("/etc/apache2/apache2.conf", "a") as apconf :
			apconf.write("\nservername localhost\n")
			apconf.close()

		ipaddr = os.popen("hostname -I").read()
		print("Adding your ip to the /etc/resolv.conf : " + ipaddr )
		time.sleep(0.5)
		with open("/etc/resolv.conf","a") as file:
			file.write(f"nameserver {ipaddr}")
			file.close()
			print("Done.\n\n")
			print("""
==== /etc/resolv.conf ====
""")
			os.system("cat /etc/resolv.conf")
			print("\n\nMake sure there is no two 'nameserver X.X.X.X'\nComment with a '#' the previous one if this is the case.\n")

			time.sleep(2)

		case = str(input("Is it the case : y/n "))
		if case == 'y':
			os.system("nano /etc/resolv.conf")
			return 0;

		elif case == 'n' :
			return 0;




	if numero == 2:

		name1 = str(input("Enter your future DNS complete  name (example : local.org) : "))
		symb1 = input("Write '{' : ")
		symb2 = input("Write '}' : ")
		with open('/etc/bind/named.conf.local','a') as file1:
			file1.write(f'''
zone "{name1}" IN {symb1}
        type master;
        file "/etc/bind/db.{name1}";
{symb2};
''')
		file1.close()
		print("\nWriting named.conf.local file.")
		time.sleep(0.5)
		print("Done.\n")
		print("Writing /etc/bind/named.conf.options...")
		time.sleep(1)
		with open("/etc/bind/named.conf.options","w") as file2:
			file2.write('''options {
        directory "/var/cache/bind";

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0's placeholder.

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation no;

        //listen-on-v6 { any; };

        allow-query { any; };
        recursion yes;
        forwarders { 8.8.8.8; 8.8.4.4; };
        forward only;

};
''')
			file2.close()
		print("Done.\n")



		print("Configuration of your main config file.\n")
		ipaddr2 = os.popen("hostname -I").read()
		numb = random.randint(10000000, 99999999)
		print("\n")
		with open(f"/etc/bind/db.{name1}","a") as dnsmain :
			print(f"Writing db.{name1}")
			dnsmain.write(f'''$TTL 604800 ;
$ORIGIN {name1}.

@ IN SOA ns1.{name1}. root.{name1}. (
{numb} ;
3600 ;
600 ;
2419200 ;
604800 ) ;

@ IN A {ipaddr2}
@ IN NS ns1
ns1 IN A {ipaddr2}


www IN A {ipaddr2}
''')
			dnsmain.close()
			time.sleep(0.5)
			print("Done.")


	if numero == 3:

		print("You are going to create a TLS for the HTTPS connection.")
		if os.path.isdir("/etc/ssl/localcerts") == False :
			print("Creating /etc/ssl/localcerts to store the keys...")
			os.system("mkdir /etc/ssl/localcerts &> /dev/null")
			print("Done.\n")
		else :
			print("/etc/ssl/localcerts already exists.\n")

		os.system("openssl req -new -x509 -sha256 -days 365 -nodes -out /etc/ssl/localcerts/local1.crt -keyout /etc/ssl/localcerts/local1.key.org")
		return 0;

	if numero == 4:

		print("\nPreparing a VHost...\nCreating a root directory for the websites...\nChecking if path : /home/sites exists...")
		time.sleep(1)
		if os.path.isdir("/home/sites") == False :
			os.system("mkdir /home/sites")
			print("Creating /home/sites.\nAll your sites will be stored in /home/sites.")
		elif os.path.isdir("/home/sites") == True :
			print("Path /home/sites already exists.")

		print("\n\nCreating VHost in /etc/apache2/sites-available")
		website = str(input("Enter a name for your website : "))
		if os.path.isdir(f"/home/sites/{website}") == False :
			os.system(f"mkdir /home/sites/{website}")
			print(f"/home/sites/{website} created successfully.")
			os.system(f"chown -R www-data:www-data /home/sites/{website} && touch /home/sites/{website}/index.html")
			with open(f"/home/sites/{website}/index.html","w") as index:
				index.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Title</title>
  <link rel="stylesheet" href="style.css">
  <script src="script.js"></script>
</head>
<body>
  ...
<br>
This is your website hehe
  <!-- Write the rest of the index here. Good Luck. -->
<br>
  ...
</body>
</html>
''')
				index.close()

		else :
			print(f"/home/sites/{website} already exists.")

		print("\n")
		os.system("ls /etc/bind | grep db.*")
		name2 = input("\nEnter the name of your dns name (without the 'db.') : ")
		print("Checking if a conf file already exists : ")
		if os.path.isfile(f"/etc/apache2/sites-available/{website}.conf") == False :
			with open(f"/etc/apache2/sites-available/{website}.conf","w") as vhst :
				print("Writing your conf file...")
				vhst.write(f"""<VirtualHost *:80>
        ServerAdmin admin@local.com
        ServerName {website}.{name2}
        DocumentRoot /home/sites/{website}

        ErrorLog /var/log/apache2/{website}.log
        CustomLog /var/log/apache2/{website}.log combined

        <Directory /home/sites/{website}>
                Require all granted
                Satisfy Any
        </Directory>
</VirtualHost>

# HTTPS

<VirtualHost *:443>
        DocumentRoot /home/sites/{website}
        ServerName {website}.{name2}


        <Directory /home/sites/{website}>
		Require all granted
		Satisfy Any
        </Directory>

        ErrorLog /var/log/apache2/{website}-error.log
        CustomLog /var/log/apache2/{website}-access.log combined


        ServerAdmin admin@local.com

SSLCertificateFile /etc/ssl/localcerts/local1.crt
SSLCertificateKeyFile /etc/ssl/localcerts/local1.key.org

</VirtualHost>""")
				vhst.close()
				time.sleep(0.5)
				print("Done.")
		else:
			print("VHost already exists.")

		print("Adding your website to the dns file.")
		with open(f"/etc/bind/db.{name2}","a") as main1 :
			main1.write(f"\n{website} IN CNAME www\n")
			main1.close()
		os.system(f"systemctl restart bind9 && a2ensite {website}.conf")
		time.sleep(1)
		os.system("systemctl reload apache2 && echo Apache2 reloaded.")

		hta = str(input("Would you like to add .htaccess to your website ? y/n "))
		if hta == 'y':
			with open(f"/etc/apache2/sites-available/{website}.conf","w") as vhst :
                                print("Writing your conf file...")
                                vhst.write(f"""<VirtualHost *:80>
        ServerAdmin admin@local.com
        ServerName {website}.{name2}
        DocumentRoot /home/sites/{website}

        ErrorLog /var/log/apache2/{website}.log
        CustomLog /var/log/apache2/{website}.log combined

        <Directory /home/sites/{website}>
		AllowOverride All
        </Directory>
</VirtualHost>

# HTTPS

<VirtualHost *:443>
        DocumentRoot /home/sites/{website}
        ServerName {website}.{name2}


        <Directory /home/sites/{website}>
                AllowOverride All
        </Directory>

        ErrorLog /var/log/apache2/{website}-error.log
        CustomLog /var/log/apache2/{website}-access.log combined


        ServerAdmin admin@local.com

SSLCertificateFile /etc/ssl/localcerts/local1.crt
SSLCertificateKeyFile /etc/ssl/localcerts/local1.key.org

</VirtualHost>""")
			print("Creating directory /var/www/accounts...")
			os.system("mkdir /var/www/accounts")
			user = input("Enter a username : ")
			os.system(f"htpasswd /var/www/accounts/.htpasswd {user}")
			with open(f"/home/sites/{website}/.htaccess","w") as access:
				access.write("""AuthType Basic
AuthUserFile /var/www/accounts/.htpasswd
AuthName "Reserved Access"
require valid-user
""")
			time.sleep(1)
			print("Done.\n")
			print("""You have to change one thing in /etc/apache2/apache2.conf at line 172 :

<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>

Change 'Allow Override None' to 'AllowOverride All'.
""")
			rdy = str(input("Write 'go' when you are ready to modify the file or if you have already done that, write 'skip' : "))
			if rdy == 'go' :
				os.system("nano -c +172 /etc/apache2/apache2.conf")
				os.system("systemctl restart apache2")
			elif rdy == 'skip' :
				return 0;



	if numero == 5:
		test()

#try

	if numero == 6:

		print("You are going to delete a VHost and all it's attached items...")
		print("\n")
		os.system("echo Files in /home/sites : ")
		print("\n")
		os.system("ls -l /home/sites/")
		print("\n")

		delete = input("Enter the name of the VHost you want to delete, write 'exit' if empty : ")
		if delete == 'exit' :
			return 0;

		elif not delete :
			print("Empty string. Error.")
			time.sleep(2)

		else :
			os.system(f"rm -r /home/sites/{delete} && \necho /home/sites/{delete} deleted.\n")
			time.sleep(0.5)
			os.system(f"rm /etc/apache2/sites-available/{delete}.conf && echo /etc/apache2/sites-available/{delete}.conf deleted.\n")
			time.sleep(0.5)
			os.system(f"rm /etc/apache2/sites-enabled/{delete}.conf && echo /etc/apache2/sites-enabled/{delete}.conf deleted.\n")
			time.sleep(0.5)
			os.system(f"rm /var/log/apache2/{delete}* && echo logs deleted.")
			print("You should delete the entry in your dns conf /etc/bind/...")
			time.sleep(2)
			return 0;



	if numero == 7 :
		os.system("cat /var/www/accounts/.htpasswd")
		user = input("Choose a user : ")
		os.system(f"htpasswd -D /var/www/accounts/.htpasswd {user}")
		time.sleep(1)
		print("Done.")
		time.sleep(1)



if __name__ == '__main__':

#	if not 'SUDO_UID' in os.environ.keys():
#		print ("""
#=======================================================
#		Use this script as sudo.
#=======================================================
#
#""")
#		sys.exit(1)

	while 1:
		main()
		choix()
