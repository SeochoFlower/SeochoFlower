# SeochoFlower

### add folder
add /datasets/images/train<br>
add /datasets/images/val<br>
add /ml<br>
add /labels<br>

### table query
create table realtime_flower(
id bigint auto_increment not null,
poomname varchar(100) not null,
goodname varchar(100) not null,
lvname varchar(100) not null,
qty int not null,
cost int not null,
dateinfo date not null default (curdate())
primary key (id)
);

create table target(
id bigint auto_increment not null,
fl_item varchar(256) not null,
fl_type varchar(256) not null,
primary key (id)
);

create table post(
id bigint auto_increment not null,
author varchar(256) not null,
content text not null,
likeit bigint default 0,
imagename varchar(256) not null,
created_at datetime default curdate(),
primary key (id)
);

create table user(
id bigint auto_increment not null,
user_id varchar(100) unique not null,
user_pw varchar(100) not null,
primary key (id)
);
