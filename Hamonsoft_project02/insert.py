class Insert:
    def __init__(self, save_name, engine, to_table, values, columns, tb):
        self.save_name = save_name
        self.engine = engine
        self.to_table = to_table
        self.values = values
        self.columns = columns
        self.tb = tb

    def same_result_have_query(self, from_table):
        if 4 in [len(v.split('.')) for v in self.values]:  # 그 중에 query문이 있는지 query문이 있다면 길이가 4이므로
            if str(type(self.save_name[from_table])) == "<class 'list'>":  # 해당 객체의 타입이 list 일 때
                for l in self.save_name[from_table]:
                    real = dict()  # 결과를 coulms와 values를 매핑시켜서 dictionary로 저장 후 insert
                    for i in range(0, len(self.values)):
                        if len(self.values[i].split('.')) == 2:  # 단순 list의 값일 때
                            real[self.columns[i]] = l[self.values[i].split('.')[1]]
                        else:  # query 문일 때
                            sql = self.values[i].split('.')[3][2:].lstrip('[').rstrip(']')
                            conn = self.engine.engine.raw_connection()
                            cur = conn.cursor()
                            cur.execute(sql, l[self.values[i].split('.')[1]])

                            recs = cur.fetchone()
                            real[self.columns[i]] = recs[0]

                    new = self.tb.insert()
                    new.execute(real)

    def same_result_only_list(self, from_table):
        for l in self.save_name[from_table]:
            real = dict()
            for i in range(0, len(self.values)):
                real[self.columns[i]] = l[self.values[i].split('.')[1]]

            new = self.tb.insert()
            new.execute(real)

    def same_result_only_table(self, from_table, DBSession):
        total_list = DBSession.query(self.save_name[from_table]).all()

        real = []
        for row in total_list:
            real.append(row._asdict())

        for a in real:
            for r in list(a.keys()):
                if r not in self.columns:
                    del (a[r])
        for t in real:
            new = self.tb.insert()
            new.execute(t)

    def different_result(self, DBSession):
        real = dict()  # 결과를 coulms와 values를 매핑시켜서 dictionary로 저장 후 insert
        for i in range(0, len(self.columns)):
            if str(type(self.save_name[self.values[i].split('.')[0]])) == "<class 'list'>":
                for l in self.save_name[self.values[i].split('.')[0]]:
                    real[self.columns[i]] = l[self.values[i].split('.')[1]]
            elif str(type(self.save_name[self.values[i].split('.')[0]])) == "<class 'sqlalchemy.sql.schema.Table'>":
                total_list = DBSession.query(self.save_name[self.values[i].split('.')[0]]).all()

                new = []
                for row in total_list:
                    new.append(row._asdict())

                for l in new:
                    real[self.columns[i]] = l[self.values[i].split('.')[1]]

        new = self.tb.insert()
        new.execute(real)