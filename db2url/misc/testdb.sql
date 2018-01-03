USE test;

DROP TABLE IF EXISTS flintstones;
create table flintstones( `FirstName` varchar(20),  `LastName` varchar(20), `Age` mediumint);
insert into flintstones values ("fred", "flintstone", 41);
insert into flintstones values ("wilma", "flintstone", 36);
insert into flintstones values ("barney", "rubble", 38);
insert into flintstones values ("betty", "rubble", 34 );

DROP TABLE IF EXISTS lost;
create table lost( `FirstName` varchar(20),  `LastName` varchar(20), `Age` mediumint);
insert into lost values ("jack", "shepherd", 39);
insert into lost values ("kate", "austin", 28);
insert into lost values ("charlie", "pace", 27);
insert into lost values ("james", "sawyer", 37);
insert into lost values ("john", "locke", 52);
insert into lost values ("hugo", "reyes", 29);
insert into lost values ("desmond", "hume", 37);
insert into lost values ("ben", "linus", 46);