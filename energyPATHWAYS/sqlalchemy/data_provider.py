import sqlalchemy
import sqlalchemy.orm
import pandas as pd
import ipdb

# sandbox is just a copy of my pathways us_model_example database so I don't have to muck around
engine = sqlalchemy.create_engine('postgresql://michael@localhost:5432/sandbox')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

frames = {}

def load(table, id_):
    if table not in frames:
        refresh(table)

    # FIXME: this makes the assumption that the id column is always the first index;
    # we should discuss whether we want to guarantee this in the database or if there's something we should do
    # in refresh() to guarantee it
    return frames[table].loc[id_]

# table here is assumed to be an instance of sqlalchemy.Table
def refresh(table):
    # column.key is the column name; any column that doesn't contain the value for the row is an index
    indexes = [column.key for column in table.columns if column.key != 'value']
    #query = session.query(table)
    frames[table] = pd.read_sql_table(table.name, engine, index_col=indexes).sort_index()
    #ipdb.set_trace()

def save(table, id_, df, refresh_after=True):
    # FIXME: need to add id column!
    del_rows = session.query(table).filter(table.c.id == id_)
    # I think synchronize_session= is only necessary here because the data table is a full-fledged Model;
    # if we represent it as a Table instead we should be able to get rid of that
    del_rows.delete(synchronize_session=False)
    write_df = df.copy()
    write_df['id'] = id_
    write_df.to_sql(table.name, engine, if_exists='append')

    if refresh_after:
        refresh(table)
