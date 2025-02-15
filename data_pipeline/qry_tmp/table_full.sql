select * from table_train limit 10
select * from table_item limit 10

select
	a.*,
	b.*
into table_full
from table_train as a
left join table_item as b
	on a.history = b.page

select * from table_full 
where page is not null
limit 100