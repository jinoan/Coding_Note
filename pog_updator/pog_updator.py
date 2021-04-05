from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import pandas as pd
import cipher
import models
import argparse

parser = argparse.ArgumentParser(prog="POG Updator")
parser.add_argument("-v", "--version", action='version', version="%(prog)s 0.0.1")
parser.add_argument("-e", "--engine", type=str, default="test", help="db engine. format: 'dbtype://user:password@host:port/db'")
parser.add_argument("-p", "--pog", type=str, default="pog.csv", help="""pog csv file. columns:
shelf_floor(int) | cell_column(int) | loadcell_column(int) | goods_id(str) | design_infer_label(str) |
stock_count_max(int) | stock_count_low_alert_limit(int) | inference_mode(str) | load_cell_mode(str) |
model_name(str) | model_address(str)
""") 
parser.add_argument("-c", "--company_id", type=str, help="company_id")
parser.add_argument("-s", "--store_id", type=str, help="store_id")
parser.add_argument("-d", "--device_id", type=str, help="""device_id. If device is workin type, the first letter is 'w',
else if device is single type, the first letter is 's'.""")
parser.add_argument("-o", "--operation", action="store_true", help="operation. If this arg is used, device would be set operating.")
args = parser.parse_args()

def update_pog(session, company_id, store_id, device_id, df, operation=False):
    company_pkey = session.query(models.Company.company_pkey).filter_by(company_id=company_id).first()
    assert company_pkey, f'company_id: {company_id}, 해당 정보가 존재하지 않습니다.'
    company_pkey = company_pkey.company_pkey

    store_pkey = session.query(models.Store.store_pkey).filter_by(company_pkey=company_pkey, store_id=store_id).first()
    assert store_pkey, f'company_id: {company_id}, store_id: {store_id}, 해당 정보가 존재하지 않습니다.'
    store_pkey = store_pkey.store_pkey

    try:
        # insert device
        device = session.query(models.Device).filter_by(store_pkey=store_pkey, device_id=device_id)
        if device.first() is None:
            print(f'company_id: {company_id}, store_id: {store_id}, device_id: {device_id}, 해당 정보가 존재하지 않습니다.')
            print(f'company_id: {company_id}, store_id: {store_id}, device_id: {device_id}, 해당 정보를 추가합니다.')
            if device_id[0] == 's':
                device_install_type = 'S'
            elif device_id[0] == 'w':
                device_install_type = 'W'
            else:
                raise ValueError('device_id의 첫 글자는 "s" 또는 "w" 이어야 합니다.')
            session.add(models.Device(device_id=device_id, store_pkey=store_pkey, device_install_type=device_install_type, operation=operation))
            # session.commit()
        
        # get device_pkey
        device_pkey = device.first().device_pkey

        # insert model
        model_pkeys = []
        change = False
        for d in df[['model_name', 'model_address']].itertuples():
            model = session.query(models.Model).filter_by(model_name=d.model_name).first()
            if model is None:
                print(f'model {d.model_name} 이 존재하지 않습니다. model 정보를 추가합니다.')
                model = models.Model(model_name=d.model_name, model_address=None if np.isnan(d.model_address) else d.model_address)
                session.add(model)
                change = True
            model_pkeys.append(model.model_pkey)
        df['model_pkey'] = model_pkeys

        # insert or update shelves
        for shelf_floor in set(df.shelf_floor):
            shelf = session.query(models.Shelf).filter_by(device_pkey=device_pkey, shelf_floor=shelf_floor)
            sub_df = df[df['shelf_floor'] == shelf_floor]
            model_pkey = sub_df['model_pkey'].iloc[0]
            if shelf.first() is None:
                print('shelf_floor가 존재하지 않습니다. shelf 정보를 추가합니다.')
                session.add(models.Shelf(device_pkey=int(device_pkey),
                                         shelf_floor=int(shelf_floor),
                                         model_pkey=int(model_pkey)))
            else:
                if shelf.first().model_pkey != model_pkey:
                    print(f'경고! shelf_floor: {shelf_floor} 자리의 model_pkey가 {shelf.first().model_pkey} 에서 {model_pkey} 로 변경됩니다.')
                    shelf.update({'model_pkey': int(model_pkey)})

        # get shelf_pkeys
        shelf_pkeys = []
        df2 = df.drop(['loadcell_column'], axis=1).drop_duplicates()
        for d in df2.itertuples():
            shelf_pkey = session.query(models.Shelf.shelf_pkey)\
                .select_from(models.Shelf)\
                .join(models.Device, models.Device.device_pkey == models.Shelf.device_pkey)\
                .filter(models.Device.store_pkey == store_pkey,
                        models.Device.device_id == device_id,
                        models.Shelf.shelf_floor == d.shelf_floor)\
                .first().shelf_pkey
            shelf_pkeys.append(shelf_pkey)

        # cells
        for d, shelf_pkey in zip(df2.itertuples(), shelf_pkeys):
            try:
                # get design_pkey
                design_pkey = session.query(models.Design.design_pkey).filter_by(design_infer_label=d.design_infer_label).all()[-1].design_pkey
            except IndexError as index_error:
                print(f'goods_id({d.goods_id})에 해당하는 데이터가 존재하지 않습니다.')
                raise index_error

            # get cells
            cell = session.query(models.Cell).filter_by(shelf_pkey=shelf_pkey, cell_column=d.cell_column)
            if cell.first() is None:
                # if the cell isn't exist, insert the cell
                print(f'floor: {d.shelf_floor}, column: {d.cell_column} 에 해당하는 데이터가 존재하지 않습니다. 해당 cell을 추가합니다.')
                session.add(models.Cell(
                    shelf_pkey=int(shelf_pkey),
                    design_pkey_master=int(design_pkey),
                    cell_column=int(d.cell_column),
                    stock_count_max=int(d.stock_count_max),
                    stock_count_low_alert_limit= None if np.isnan(d.stock_count_low_alert_limit) else int(d.stock_count_low_alert_limit),
                    inference_mode=d.inference_mode,
                    load_cell_mode=d.load_cell_mode
                ))
            else:
                # else, update the cell
                cell.update({
                    'design_pkey_master': int(design_pkey),
                    'stock_count_max': int(d.stock_count_max),
                    'stock_count_low_alert_limit': None if np.isnan(d.stock_count_low_alert_limit) else int(d.stock_count_low_alert_limit),
                    'inference_mode': d.inference_mode,
                    'load_cell_mode': d.load_cell_mode
                })

            # insert init stock
            stock = session.query(models.Stock).filter_by(cell_pkey=cell.first().cell_pkey)
            if stock.first() is None:
                print(f'stock 추가 (floor: {d.shelf_floor}, column: {d.cell_column}, goods_id: {d.goods_id}, stock_count: 0')
                session.add(models.Stock(
                    cell_pkey=cell.first().cell_pkey,
                    design_pkey=int(design_pkey),
                    stock_count=0
                ))
            
        # insert (or update) loadcell
        for d in df.itertuples():
            shelf_pkey = session.query(models.Shelf.shelf_pkey)\
                .select_from(models.Shelf)\
                .join(models.Device, models.Device.device_pkey == models.Shelf.device_pkey)\
                .filter(models.Device.store_pkey == store_pkey,
                        models.Device.device_id == device_id,
                        models.Shelf.shelf_floor == d.shelf_floor)\
                .first().shelf_pkey

            cell_pkey = session.query(models.Cell.cell_pkey).filter_by(shelf_pkey=shelf_pkey, cell_column=d.cell_column).first().cell_pkey

            # get loadcells
            loadcells = session.query(models.Loadcell).filter_by(shelf_pkey=shelf_pkey, loadcell_column=d.loadcell_column).first()

            if loadcells is None:
                # insert loadcell
                session.add(models.Loadcell(shelf_pkey=int(shelf_pkey), cell_pkey=int(cell_pkey), loadcell_column=d.loadcell_column))
            else:
                # update loadcell
                loadcells.cell_pkey = cell_pkey

        session.commit()
        
    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()



if __name__ == '__main__':
    print('Start pog updator')

    if args.engine == "main":
        engine = create_engine(f"postgresql://postgres:{cipher.get('postgres_key')}@{cipher.get('main_db_endpoint')}:5432/emart24")
    elif args.engine == "test":
        engine = create_engine(f"postgresql://postgres:{cipher.get('postgres_key')}@{cipher.get('test_db_endpoint')}:5432/emart24")
    else:
        engine = create_engine(args.engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    pog = pd.read_csv(
        args.pog,
        dtype={
            'goods_id': 'str',
            'design_infer_label': 'str',
            'inference_mode': 'str',
            'load_cell_mode': 'str',
            'model_name': 'str',
            'model_address': 'str'
        }
    )
    
    update_pog(session, args.company_id, args.store_id, args.device_id, pog, operation=args.operation)
    print('Done')
