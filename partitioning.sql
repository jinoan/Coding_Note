create table partition_test(
	c1 varchar(20),
	c2 varchar(20),
	lee_date date) with (oids=false);

--function 생성
create or replace function create_partition_and_insert() returns trigger as
	$body$
		declare
			partition_date text;
			partition text;
		begin
			partition_date := to_char(new.lee_date, 'yyyy_mm');
			partition := tg_relname || '_' || partition_date;
			if not exists(select relname from pg_class where relname=partition) then
				raise notice 'a partition has been created %', partition;
				execute 'create table ' || partition || ' (check (to_char(lee_date, ''yyyy_mm'') = ''' || partition_date || ''')) inherits ('|| tg_relname ||');';
			end if;
			execute 'insert into ' || partition || ' select ('|| tg_relname || '' || quote_literal(new) ||').* returning *;';
			return null;
		end;
	$body$
language plpgsql volatile
cost 100;

--데이터 입력시 만든 function을 호출하는 trigger 생성
create trigger partition_test_insert_trigger
before insert on partition_test
for each row execute procedure create_partition_and_insert();

--파티션 테이블 파티션 정보 확인
create or replace view show_partition as
select nmsp_parent.nspname as parent_schema,
	parent.relname as parent,
	nmsp_child.nspname as child_schema,
	child.relname as child
from pg_inherits
join pg_class parent on pg_inherits.inhparent = parent.oid
join pg_class child on pg_inherits.inhrelid = child.oid
join pg_namespace nmsp_parent on nmsp_parent.oid = parent.relnamespace
join pg_namespace nmsp_child on nmsp_child.oid = child.relnamespace
-- where parent.relname='partition_test'

insert into partition_test values ('33333', '33333', '2020-12-14');

select * from show_partition;
select * from partition_test;
select * from partition_test_2020_12;
