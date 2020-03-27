class Query:
    def __init__(self, save_name, example, engine):
        self.save_name = save_name
        self.example = example
        self.engine = engine

    def query_to_save_name(self):
        sql = self.example.split('<-')[1].split('SQL')[1].lstrip('[').rstrip(']')
        conn = self.engine.raw_connection()
        cur = conn.cursor()
        cur.execute(sql)

        recs = cur.fetchall()

        # query문 실행 후 각 row를 column명 기준 dictionary로 저장 전체 결과를 list형태로 저장
        real_rows = []
        for rec in recs:
            row = dict(zip([d[0] for d in cur.description], rec))
            real_rows.append(row)
        self.save_name[self.example.split('<-')[0]] = real_rows  # 결과 list 전체 결과 dictionary에 저장