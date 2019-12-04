alter table user_question_log add answered_at timestamp not null default current_timestamp;
alter table user_game_log add sent_at timestamp not null default current_timestamp;
alter table user_question_log modify session_id integer;

