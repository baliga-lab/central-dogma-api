/* Allow unauthorized users for the retreat */
alter table users modify hash varchar(512);
alter table users modify salt varchar(100);
