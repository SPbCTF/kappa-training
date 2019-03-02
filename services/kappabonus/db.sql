create database `kappabonus`;

create table `user`(
	`username` varchar(40) not null,
	`password` char(82) not null,
	`balance` int default 0,
	`vip` tinyint default 0,
	`posted_flags` int default 0,
	primary key(`username`)
	);

create table `kappa`(
  `id` int not null auto_increment,
	`flag` char(32) not null,
	`cost` int not null,
	primary key(`id`)
	);

create table `lcbc`(
  `id` int not null auto_increment,
	`flag` char(32) not null,
	`cost` int not null,
	primary key(`id`)
	);