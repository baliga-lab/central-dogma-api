create table hyperlink_log (
  id integer primary key auto_increment,
  user_id integer not null,
  url varchar(1000) not null,
  visited_on timestamp not null default current_timestamp
) ENGINE=InnoDB default charset=utf8;

alter table hyperlink_log add constraint fk_link_visitor foreign key (user_id) references users (id);

