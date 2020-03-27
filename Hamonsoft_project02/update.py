class Update:
    def __init__(self, save_name, to_table, set_condition, where, tb, session):
        self.save_name = save_name
        self.to_table = to_table
        self.set_condition = set_condition
        self.where = where
        self.tb = tb
        self.session = session

    def int_to_int_update(self):
        self.session.query(self.tb).filter(self.tb.columns[self.where[0]] == int(self.where[1].split('/')[1])).update(
            {self.tb.columns[self.set_condition[0]]: int(self.set_condition[1].split('/')[1])}, synchronize_session=False)
        self.session.commit()

    def int_to_str_update(self):
        self.session.query(self.tb).filter(self.tb.columns[self.where[0]] == int(self.where[1].split('/')[1])).update(
            {self.tb.columns[self.set_condition[0]]: self.set_condition[1].split('/')[1]}, synchronize_session=False)
        self.session.commit()

    def str_to_int_update(self):
        self.session.query(self.tb).filter(self.tb.columns[self.where[0]] == self.where[1].split('/')[1]).update(
            {self.tb.columns[self.set_condition[0]]: int(self.set_condition[1].split('/')[1])}, synchronize_session=False)
        self.session.commit()

    def str_to_str_update(self):
        self.session.query(self.tb).filter(self.tb.columns[self.where[0]] == self.where[1].split('/')[1]).update(
            {self.tb.columns[self.set_condition[0]]: self.set_condition[1].split('/')[1]}, synchronize_session=False)
        self.session.commit()
