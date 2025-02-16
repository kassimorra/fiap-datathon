select * from table_train limit 10
select * from table_item limit 10

drop table if exists table_full
select
	a.*,
	b.*
into table_full
from table_train as a
left join table_item as b
	on a.history = b.page

select * from table_full limit 15

select a.* from table_item as a where a.page = 'c8aab885-433d-4e46-8066-479f40ba7fb2'