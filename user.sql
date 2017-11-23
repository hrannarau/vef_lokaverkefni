create database 1612002390_veflokaverkefni;

use 1612002390_veflokaverkefni;

drop table users;
create table if not exists users(
	username varchar(155) primary key,
    passwd varchar(20)
);

create table if not exists bilar(
	id int primary key,
	name varchar(155),
    yearmodel int,
    mora varchar(20),
    uorn varchar(20),
    price int
);

insert into bilar
values
(
	1,
	'VW Golf',
    2000,
    'Manual',
    'Used',
    100000
),
(
	2,
    'Ford Escape Limited',
    2006,
    'Auto',
    'Used',
    130000
),
(
	3,
    'Toyota Corolla',
    1994,
    'Manual',
    'Used',
    60000
),
(
	4,
    'Toyota Rav',
    2001,
    'Auto',
    'Used',
    280000
),
(
	5,
    'Mazda 6',
    2004,
    'Auto',
    'Used',
    290000
),
(
	6,
    'Chevrolet Cruze',
    2011,
    'Manual',
    'Used',
    370000
),
(
	7,
    'Renault Mégane',
    2004,
    'Manual',
    'Used',
    150000
),
(
	8,
    'Honda Accord',
    2004,
    'Auto',
    'Used',
    170000
);