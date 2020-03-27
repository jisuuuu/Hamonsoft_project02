import sqlite3
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import inspect
import update
import delete
import insert
import query
import simple_query
import transaction
from zope.sqlalchemy import register

def moveDBServer(filename):
    f = open(filename, 'r')
    read = f.read()
    f.close()

    #텍스트 파일에서 줄바꿈과 맨 끝의 ; 표시를 제거 후 ;를 기준으로 구분
    input_list = read.replace('\n', '').rstrip(';').split(';')
    print(input_list)

    # <-표시로 대입시킬 객체의 이름과 결과를 Dictionary에 저장
    save_name = {}

    # 텍스트파일을 저장한 리스트를 한 줄씩 읽음
    for example in input_list:
        if '<-' in example:
            real = example.split('<-')[1]
            print(real)

            if '.' not in real:
                conn = sqlite3.connect('Test.db')
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                result = cur.execute("select * from db_list where name='%s'" % real)

                for r in result:
                    if r['db_type'] == 'oracle':
                        engine_url = 'oracle+cx_oracle://'+ r['id'] + ":" + r['password'] + '@' + r['host_port'] + '/' + r['database']
                        print(engine_url)
                    elif r['db_type'] == 'mysql':
                        engine_url = 'mysql+pymysql://' + r['id'] + ":" + r['password'] + '@' + r[
                            'host_port'] + '/' + r['database']
                        print(engine_url)
                    else:
                        engine_url = 'mssql+pymssql://' + r['id'] + ":" + r['password'] + '@' + r[
                            'host_port'] + '/' + r['database']
                        print(engine_url)

                engine = create_engine(engine_url, encoding='utf8', echo=True)

                conn.close()
                save_name[example.split('<-')[0]] = engine

            elif 'SQL' in real: #Source DB 중 query문
                engine = save_name[real.split('.')[0]]
                Base = declarative_base()
                Base.metadata.create_all(engine)

                source_query = query.Query(save_name, example, engine)

                source_query.query_to_save_name()

            elif 'simple' in real: #Source DB 중 간단한 join문
                engine = save_name[real.split('.simple.')[0]]
                from_table_name = real.split('.simple.')[1].split('?')[0].split('+') # + 기준으로 join, 연산할 테이블 저장
                condition = real.split('.simple.')[1].split('?')[1].split('->')[0].split(',') # ? 이후 조건 저장
                to_column_name = real.split('.simple.')[1].split('?')[1].split('->')[1].split(',') # 저장할 column명 지정

                inspector2 = inspect(engine)
                md2 = MetaData(bind=engine)

                DBSession = scoped_session(sessionmaker())
                DBSession.configure(bind=engine)

                from_table_list = dict()  # Source DB의 table을 저장할 dictionary
                #DB에서 table 이름 매핑 시켜 저장하는 과정
                for table_name in inspector2.get_table_names():
                    for name in from_table_name:
                        if table_name == name:
                            tb = Table(table_name, md2, autoload_with=engine, extend_existing=True)
                            from_table_list[name] = tb

                print(from_table_list)

                new_simple = simple_query.Simple_Query(save_name, from_table_name, condition, to_column_name,
                                                           from_table_list, DBSession)

                total_list = [] #query 결과를 담을 listpy
                real_list = [] #실제 전체 결과 dictionary 들어갈 list
                if len(condition) == 1: #조건이 간단한 연산과 비교 하나 뿐일 때
                    if '<' in condition[0]:
                        if 'INT' in condition[0].split('<')[1].split('.')[0]:#비교하는 것이 INT 일 때
                            if '=' in condition[0].split('<')[1].split('.')[0]:#<=
                                total_list = new_simple.one_condition_int_smaller_same()
                            else: #<
                                total_list = new_simple.one_condition_int_smaller()
                    elif '>' in condition[0]:
                        if 'INT' in condition[0].split('<')[1].split('.')[0]: #비교하는 것이 INT 일 때
                            if '=' in condition[0].split('<')[1].split('.')[0]: #>=
                                total_list = new_simple.one_condition_int_bigger_same()
                            else: #>
                                total_list = new_simple.one_condition_int_bigger()
                    elif '=' in condition[0]:
                        if condition[0].split('<')[1].split('.')[0] == 'INT':
                            total_list = new_simple.one_condition_int_same()
                        elif condition[0].split('<')[1].split('.')[0] == 'STR':
                            total_list = new_simple.one_conditon_str_same()
                        else: #비교 연산이 아닌 join 조건일 때
                            total_list = new_simple.one_condition_join()
                else: #조건이 간단한 사칙연산이 아닌 group by를 포함할 때
                    if 'GB' in condition[1]:
                        group_by_list = condition[1].split('.') # .을 기준으로  1. GB 표시 2. group by 기준 테이블 3. 기준 테이블의 기준 칼럼명 4. 간단한 함수(SUM, MIN..) 5. 계산할 테이블 6. 계산할 칼럼명

                        # count, sum, avg, min, max를 사용하여 group by 가능
                        if group_by_list[3] == 'COUNT':
                            total_list = new_simple.two_condition_group_by_count(group_by_list)
                        elif group_by_list[3] == 'SUM':
                             total_list = new_simple.two_condition_group_by_sum(group_by_list)
                        elif group_by_list[3] == 'AVG':
                            total_list = new_simple.two_condition_group_by_avg(group_by_list)
                        elif group_by_list[3] == 'MAX':
                            total_list = new_simple.two_condition_group_by_max(group_by_list)
                        elif group_by_list[3] == 'MIN':
                            total_list = new_simple.two_condition_group_by_min(group_by_list)

                #total_list 값을 dictionary로 변환하는 과정
                for row in total_list:
                    real_list.append(row._asdict())

                #real_list를 전체 결과 dictionary에 저장
                save_name[example.split('<-')[0]] = real_list
                print(save_name)
            else: #Source DB 중 매칭하는 테이블 저장
                engine = save_name[real.split('.')[0]]
                inspector2 = inspect(engine)
                md = MetaData(bind=engine)

                for table_name in inspector2.get_table_names():
                    if table_name == real.split('.')[1]:
                        tb = Table(table_name, md, autoload_with=engine, extend_existing=True)
                        save_name[example.split('<-')[0]] = tb #전체 결과 dicionary에 테이블 객체 저장'''
                print(save_name)

        else: #텍스트 파일 행 중 S, T 표시 없는 실제 실행하는 행
            if 'insert' in example: #insert
                values = example.split('values')[1].lstrip('(').rstrip(');').split('/ ') #values() 안에 / 으로 구분 value는 전체 결과 dictionary에 저장한 이름과 column명으로 구성
                to_table = example.split('values')[0].split('.')[1] #맨 앞에 insert 할 테이블 이름 .으로 구분
                columns = example.split('values')[0].split('.')[2].split('insert')[1].lstrip('(').rstrip(')').split(', ') #insert() 안에 대입할 column명 values와 순서대로 매핑함

                engine = save_name[example.split('values')[0].split('.')[0]]
                Base = declarative_base()
                Base.metadata.create_all(engine)
                md = MetaData(bind=engine)
                tb = Table(save_name[to_table], md, autoload_with=engine, extend_existing=True)

                print(values)
                print(to_table)
                print(columns)
                print(tb)

                new_insert = insert.Insert(save_name, engine, to_table, values, columns, tb)

                if len(set([v.split('.')[0] for v in values])) == 1: #values들이 하나의 객체일 때
                    from_table = values[0].split('.')[0]

                    if 4 in [len(v.split('.')) for v in values]: #그 중에 query문이 있는지 판단(query문이 있다면 길이가 4이므로)
                        new_insert.same_result_have_query(from_table)

                    else: #객체 타입이 전부 list 값이거나 Table 일 때
                        if str(type(save_name[from_table])) == "<class 'list'>":
                            new_insert.same_result_only_list(from_table)

                        elif str(type(save_name[from_table])) == "<class 'sqlalchemy.sql.schema.Table'>":
                            for s in save_name.values():
                                if str(s) == str(save_name[from_table].metadata).lstrip('MetaData(bind=')[:-1]:
                                    engine2 = s
                                    print(engine2)
                                    DBSession = scoped_session(sessionmaker())
                                    DBSession.configure(bind=engine2)

                                    new_insert.same_result_only_table(from_table, DBSession)

                else: #객체 타입이 하나가 아니고 여러개 일
                    DBSession = scoped_session(sessionmaker())
                    DBSession.configure(bind=engine)

                    new_insert.different_result(DBSession)

            elif 'delete' in example: #delete
                engine = save_name[example.split('.')[0]]
                Base = declarative_base()
                Base.metadata.create_all(engine)
                md = MetaData(bind=engine)

                conn = engine.connect()
                to_table = example.split('.')[1] #맨 앞에 delete 할 테이블 이름 .으로 구분

                tb = Table(save_name[to_table], md, autoload_with=engine, extend_existing=True)
                Session = sessionmaker(bind=engine)
                session = Session()

                new_delete = delete.Delete(save_name, conn, to_table, example, session, tb)
                if 'where' in example: #특정 row 삭제할 때
                    if '>' in example.split('where')[1]:
                        if 'INT' in example.split('where')[1]: #INT 비교
                            if '=' in example.split('where')[1]: #>=
                                new_delete.int_biggerorsame_delete()
                            else: #>
                                new_delete.int_bigger_delete()
                    elif '<' in example.split('where')[1]:
                        if 'INT' in example.split('where')[1]: #INT 비교
                            if '=' in example.split('where')[1]: #<=
                                new_delete.int_smallerorsame_delete()
                            else: #<
                                new_delete.int_smaller_delete()
                    else: # ==
                        if 'INT' in example.split('where')[1]: #INT 비교
                            new_delete.int_same_delete()
                        else: #STR 비교
                            new_delete.str_same_delete()

                else: #table 전부 삭제
                    new_delete.all_delete()

            elif 'update' in example: #update
                engine = save_name[example.split('.')[0]]
                Base = declarative_base()
                Base.metadata.create_all(engine)
                md = MetaData(bind=engine)

                to_table = example.split('.')[1] #맨 앞에 update 할 테이블 이름 .으로 구분
                set_condition = example.split('set')[1].lstrip('(').rstrip(')').split('=') #새로 업데이트 할 coulum과 value
                where = example.split('set')[0].split('where')[1].lstrip('(').rstrip(')').split('=') #업데이트할 row 찾을 조건

                tb = Table(save_name[to_table], md, autoload_with=engine, extend_existing=True)
                Session = sessionmaker(bind=engine)
                session = Session()

                new_update = update.Update(save_name, to_table, set_condition, where, tb, session)

                if 'INT' in where[1]: #where 조건에 INT 비교
                    if 'INT' in set_condition[1]: #업데이트 할 value 중 INT 포함
                        new_update.int_to_int_update()
                    elif 'STR' in set_condition[1]: #업데이트 할 value 중 STR 포함
                        new_update.int_to_str_update()
                elif 'STR' in where[1]: #where 조건에 STR 비교
                    if 'INT' in set_condition[1]: #업데이트 할 value 중 INT 포함
                        new_update.str_to_int_update()
                    elif 'STR' in set_condition[1]: #업데이트 할 value 중 STR 포함
                        new_update.str_to_str_update()

moveDBServer('run_copy.txt')