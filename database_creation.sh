#!/bin/sh


echo "Enter your mysql user:"
read mysql_user

echo "Enter your mysql passwd:"
read mysql_passwd

echo "How do you want to name your database? (default: swgoh)"
read database_name
if [ -z "$database_name" ]
then
	database_name="swgoh"
fi


# create swgoh database
mysqladmin -u${mysql_user} --password=${mysql_passwd} create ${database_name}

# insert table inside of the database
mysql -u${mysql_user} --password=${mysql_passwd} ${database_name} < swgoh.sql