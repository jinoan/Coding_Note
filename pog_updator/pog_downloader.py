from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import cipher
import models
import argparse
import os

dir_path = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser(prog="POG Downloader")
parser.add_argument("-V", "--version", action="version", version="%(prog)s 0.0.1")
parser.add_argument("-e", "--engine", type=str, default="test", help="db engine. format: 'dbtype://user:password@host:port/db'")
parser.add_argument("-f", "--filename", type=str, default=None, help="csv file name.")
parser.add_argument("-c", "--company_id", type=str, help="company id to querying in DB")
parser.add_argument("-s", "--store_id", type=str, help="store id to querying in DB")
parser.add_argument("-d", "--device_id", type=str, help="device id to querying in DB")
parser.add_argument("-v", "--verbose", type=int, default=0, help="if verbose is '1', the query results will be printed.")
args = parser.parse_args()

class POGDownloader:
    def __init__(self, engine, compnay_id, store_id, device_id):
        self.session = sessionmaker(bind=engine)()
        self.company_id = compnay_id
        self.store_id = store_id
        self.device_id = device_id
        self.pog = None
        
    def get_pog(self):
        try:
            query = self.session.query(
                models.Shelf.shelf_floor,
                models.Cell.cell_column,
                models.Loadcell.loadcell_column,
                models.Design.goods_id,
                models.Design.design_infer_label,
                models.Cell.stock_count_max,
                models.Cell.stock_count_low_alert_limit,
                models.Cell.inference_mode,
                models.Cell.load_cell_mode,
                models.Model.model_name,
                models.Model.model_address
            )\
                .select_from(models.Loadcell)\
                .join(models.Cell, models.Cell.cell_pkey == models.Loadcell.cell_pkey)\
                .join(models.Design, models.Design.design_pkey == models.Cell.design_pkey_master)\
                .join(models.Shelf, models.Shelf.shelf_pkey == models.Loadcell.shelf_pkey)\
                .join(models.Model, models.Model.model_pkey == models.Shelf.model_pkey)\
                .join(models.Device, models.Device.device_pkey == models.Shelf.device_pkey)\
                .join(models.Store, models.Store.store_pkey == models.Device.store_pkey)\
                .join(models.Company, models.Company.company_pkey == models.Store.company_pkey)\
                .filter(
                    models.Company.company_id == self.company_id,
                    models.Store.store_id == self.store_id,
                    models.Device.device_id == self.device_id
                )
            self.pog = pd.read_sql(query.statement, self.session.bind)
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def make_csv(self, filename=None):
        assert self.pog is not None, "pog is 'None'. run 'get_pog()' first."
        filename = self.company_id + '_' + self.store_id + '_' + self.device_id + '_' + 'pog.csv' if filename is None else filename
        self.pog.to_csv(filename, index=False)
        print(f"make '{filename}' in '{dir_path}'")


if __name__ == "__main__":
    if args.engine == "main":
        engine = create_engine(f"postgresql://postgres:{cipher.get('postgres_key')}@{cipher.get('main_db_endpoint')}:5432/emart24")
    elif args.engine == "test":
        engine = create_engine(f"postgresql://postgres:{cipher.get('postgres_key')}@{cipher.get('test_db_endpoint')}:5432/emart24")
    else:
        engine = create_engine(args.engine)

    pog_downloader = POGDownloader(engine, args.company_id, args.store_id, args.device_id)

    try:
        pog_downloader.get_pog()
    except Exception as e:
        raise e
    else:
        if args.verbose == 1:
            print(pog_downloader.pog)
        pog_downloader.make_csv(args.filename)
        