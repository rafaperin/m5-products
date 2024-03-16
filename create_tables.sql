create table if not exists products (
	product_id uuid primary key,
	name varchar(30) not null,
    description varchar(150) not null,
    category varchar(30) not null,
    price decimal(7,2) not null,
    image_url varchar(150)
);
