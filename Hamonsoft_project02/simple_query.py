from sqlalchemy import func


class Simple_Query:
    def __init__(self, save_name, from_table_name, condition, to_column_name, from_table_list, DBSession):
        self.save_name = save_name
        self.from_table_name = from_table_name
        self.condition = condition
        self.to_column_name = to_column_name
        self.from_table_list = from_table_list
        self.DBSession = DBSession

    def one_condition_int_smaller_same(self):
        op = self.condition[0].split('<')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] <= int(op_2[1])).all()
        return total_list

    def one_condition_int_smaller(self):
        op = self.condition[0].split('<')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] < int(op_2[1])).all()
        return total_list

    def one_condition_int_bigger_same(self):
        op = self.condition[0].split('>')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] >= int(op_2[1])).all()
        return total_list

    def one_condition_int_bigger(self):
        op = self.condition[0].split('>')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] > int(op_2[1])).all()
        return total_list

    def one_condition_int_same(self):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] == int(op_2[1])).all()
        return total_list

    def one_conditon_str_same(self):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] == op_2[1]).all()
        return total_list

    def one_condition_join(self):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(self.from_table_list[op_1[0]], self.from_table_list[op_2[0]]).filter(
            self.from_table_list[op_1[0]].columns[op_1[1]] ==
            self.from_table_list[op_2[0]].columns[op_2[1]]).all()
        return total_list

    def two_condition_group_by_count(self, group_by_list):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(
            self.from_table_list[group_by_list[1]].columns[group_by_list[2]],
            func.count(
                self.from_table_list[op_1[0]].columns[group_by_list[5]]).label(
                self.to_column_name[1])) \
            .join(self.from_table_list[op_1[0]],
                  self.from_table_list[op_1[0]].columns[op_1[1]] ==
                  self.from_table_list[op_2[0]].columns[
                      op_2[1]]) \
            .group_by(self.from_table_list[group_by_list[1]].columns[group_by_list[2]]).all()

        return total_list

    def two_condition_group_by_sum(self, group_by_list):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(
            self.from_table_list[group_by_list[1]].columns[group_by_list[2]],
            func.sum(
                self.from_table_list[op_1[0]].columns[group_by_list[5]]).label(
                self.to_column_name[1])) \
            .join(self.from_table_list[op_1[0]],
                  self.from_table_list[op_1[0]].columns[op_1[1]] ==
                  self.from_table_list[op_2[0]].columns[
                      op_2[1]]) \
            .group_by(self.from_table_list[group_by_list[1]].columns[group_by_list[2]]).all()

        return total_list

    def two_condition_group_by_avg(self, group_by_list):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(
            self.from_table_list[group_by_list[1]].columns[group_by_list[2]],
            func.avg(
                self.from_table_list[op_1[0]].columns[group_by_list[5]]).label(
                self.to_column_name[1])) \
            .join(self.from_table_list[op_1[0]],
                  self.from_table_list[op_1[0]].columns[op_1[1]] ==
                  self.from_table_list[op_2[0]].columns[
                      op_2[1]]) \
            .group_by(self.from_table_list[group_by_list[1]].columns[group_by_list[2]]).all()

        return total_list

    def two_condition_group_by_max(self, group_by_list):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(
            self.from_table_list[group_by_list[1]].columns[group_by_list[2]],
            func.max(
                self.from_table_list[op_1[0]].columns[group_by_list[5]]).label(
                self.to_column_name[1])) \
            .join(self.from_table_list[op_1[0]],
                  self.from_table_list[op_1[0]].columns[op_1[1]] ==
                  self.from_table_list[op_2[0]].columns[
                      op_2[1]]) \
            .group_by(self.from_table_list[group_by_list[1]].columns[group_by_list[2]]).all()

        return total_list

    def two_condition_group_by_min(self, group_by_list):
        op = self.condition[0].split('=')
        op_1 = op[0].split('.')
        op_2 = op[1].split('.')

        total_list = self.DBSession.query(
            self.from_table_list[group_by_list[1]].columns[group_by_list[2]],
            func.min(
                self.from_table_list[op_1[0]].columns[group_by_list[5]]).label(
                self.to_column_name[1])) \
            .join(self.from_table_list[op_1[0]],
                  self.from_table_list[op_1[0]].columns[op_1[1]] ==
                  self.from_table_list[op_2[0]].columns[
                      op_2[1]]) \
            .group_by(self.from_table_list[group_by_list[1]].columns[group_by_list[2]]).all()

        return total_list