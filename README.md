# TELEGRAM_CALENDAR ALCAROHTAR ![Python_logo_mini](https://user-images.githubusercontent.com/89790994/132233323-31f21542-912d-4422-a8ae-3f0cd2d11c8a.jpg)


Telegram_Calendar is a script that use a python-telegram-bot library to communicate wih the server and the mariadb library to store data in SQL database.
It allows to store/remove event on calendar database and show them with te right command.


## What do you need?
1.  - Install with pip3 the appropriate libraries: python-telegram-bot, reponses
    - Install with apt mariadb-server
2.  - Check mariadb-server is in status "running" : sudo systemctl status mariadb.service
3.  - Log in mariadb database: sudo mariadb -u root -p
4.  - Create a new user with the command: CREATE USER 'user'@localhost IDENTIFIED BY 'password';
5.  - Select your new user with the command: SELECT user FROM mysql.user;
6.  - Give privileges to your new user with the command: GRANT ALL PRVILEGES ON *.* TO 'user'@localhost IDENTIFIED BY 'password';
7.  - Exit from mariadb with command quit and enter again with new user: sudo mariadb -u user -p (where user is the one chosen before)
8.  - Create new Database with command: CREATE DATABASE databasename;
9.  - Use that new database: USE databasename;
10. - Create new table with the command:  
	CREATE TABLE calendario_famiglia (  
    		id int NOT NULL AUTO_INCREMENT,  
    		data date NOT NULL,  
    		descrizione varchar(1000) NOT NULL,  
    		ora_inizio time,  
    		ora_fine time  
		);  
11. - ***I created a table named "calendario_famiglia". If you want to use another name for you table 
     you need to modify file Calendario_Main.py and substitute all calendario_famiglia occurences with your table name.  
     Same for all field of table (id, data, descrizione, ora_inizio, ora_fine). If you need to change those name you have to
     modify the Calendario_Main.py file. Those name have no impact on what you are going to read on telegram, they have impact only on code***
12. - Modify all fields in Calendario_privateInfo.py with your personal information 
13. - Go on Telegram app, check BotFather and create a new bot with command /newbot
     ***The reply message will contain a TOKEN you have to use in your script Calendatio_privateInfo.py***


## How to modify Calendario_privateInfo.py
user 	 = "" (Insert the name of new user created on point 4)  
password = "" (Insert the password for your user created on point 4)   
host	 = "" (Insert "localhost")  
port	 = "" (Insert "3306")  
database = "" (Insert the name of database created on point 8)  
user	 = "" (Insert name and surname of user enable to access to that database)  
	      (For example if you want to use that bot and share it to your wife, you have to add  
		user1=[(youName,yourSurname)] and user2=[(yourWifeName, yourWifeSurname)])  
		Modify users variable in CalendarioTelegram_main.py if you want to add other users  

 ***All files have to be in same directory***

  
## File Explanation
- Calendario-Main.py contains all function to manage the database.
- CalendarioTelegram_main.py contains the main function to handle in an infinite loop the telegram receiving message.
- Calendario_privateInfo.py contains all personal information of database and enable users on telegram.
  

## HOW IT WORKS
On telegram bot you can use these commands:
- show: it returns the entire table with all events saved
- A: means "add". To add the event you have to write in telegram A date .description. time_start time_end (Ex: A 22-12-2022 .buy something. 13:00 14:00)
  I used for date the format %d-%m-%Y, You can change it in CalendarioTelegram_main.py file. ***Remember to use dot to enclose the description***
  Time start and time end are optional
- R: means "remove". To remove an instance from calendar you can write R id (EX: R 5). You can also write more than one event to remove (EX: R 2 5 19)
  It is possible to remove all calendar with R all command



***Please let me know if something is not clear, if some bugs happen or if you think it could be improved***  
***It has been tested on linux os and MacOs. New tests on will be done soon.***

