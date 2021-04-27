        keys = ', '.join(position.keys())
        values = ', '.join(['%s'] * len(position))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table,
                                                                     keys=keys, values=values)
        print(sql)
        try:
            cursor.execute(sql, tuple(position.values()))
            db.commit()
        except Exception as e:
            print('´íÎóÐÅÏ¢Îª', e)
            db.rollback()
            db.close()
