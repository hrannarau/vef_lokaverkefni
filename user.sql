create database 1612002390_veflokaverkefni;

use 1612002390_veflokaverkefni;

create table if not exists users(
	username varchar(155),
    email varchar(155),
    passwd varchar(20)
);

insert into users
values
(
	'hrannarau',
    'hrannsi@hotmail.com',
    'hrannsipannsi'
),
(
	'haraldur93',
    'halli@yahoo.com',
    'haraldur12345'
);
