class Delete:
    def __init__(self, save_name, conn, to_table, example, session, tb):
        self.save_name = save_name
        self.conn = conn
        self.to_table = to_table
        self.example = example
        self.session = session
        self.tb = tb

    def int_biggerorsame_delete(self):
        where = self.example.split('where')[1].lstrip('(').rstrip(')').split('>=')  # >= 기준으로 where 조건 구분
        self.session.query(self.tb).filter(self.tb.columns[where[0]] >= int(where[1].split('/')[1])).delete(
            synchronize_session=False)
        self.session.commit()

    def int_bigger_delete(self):
        where = self.example.split('where')[1].lstrip('(').rstrip(')').split('>')  # > 기준으로 where 조건 구분
        self.session.query(self.tb).filter(self.tb.columns[where[0]] > int(where[1].split('/')[1])).delete(
            synchronize_session=False)
        self.session.commit()

    def int_smallerorsame_delete(self):
        where = self.example.split('where')[1].lstrip('(').rstrip(')').split('<=')  # <= 기준으로 where 조건 구분
        self.session.query(self.tb).filter(self.tb.columns[where[0]] <= int(where[1].split('/')[1])).delete(
            synchronize_session=False)
        self.session.commit()

    def int_smaller_delete(self):
        where = self.example.split('where')[1].lstrip('(').rstrip(')').split('<')  # < 기준으로 where 조건 구분
        self.session.query(self.tb).filter(self.tb.columns[where[0]] < int(where[1].split('/')[1])).delete(
            synchronize_session=False)
        self.session.commit()

    def int_same_delete(self):
        where = self.example.split('where')[1].lstrip('(').rstrip(')').split('=')  # = 기준으로 where 조건 구분
        self.session.query(self.tb).filter(self.tb.columns[where[0]] == int(where[1].split('/')[1])).delete(
            synchronize_session=False)
        self.session.commit()

    def str_same_delete(self):
        where = self.example.split('where')[1].lstrip('(').rstrip(')').split('=')  # = 기준으로 where 조건 구분
        self.session.query(self.tb).filter(self.tb.columns[where[0]] == where[1].split('/')[1]).delete(
            synchronize_session=False)
        self.session.commit()

    def all_delete(self):
        del_st = self.tb.delete()
        self.conn.execute(del_st)