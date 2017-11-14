create database 1612002390_veflokaverkefni;

use 1612002390_veflokaverkefni;

drop table users;
create table if not exists users(
	username varchar(155),
    passwd varchar(20)
);

select * from users;