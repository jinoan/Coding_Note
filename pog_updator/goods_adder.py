from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import cipher
import models
import argparse

parser = argparse.ArgumentParser(prog="Goods Adder")
parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.0.1")
parser.add_argument("-e", "--engine", type=str, default="test", help="db engine. format: 'dbtype://user:password@host:port/db'")
parser.add_argument("-f", "--file", type=str, help="""pog csv file. columns:
goods_id(str) | goods_name(str) | design_infer_label(str) | design_mean_weight(float) | design_std_weight(float)
""") 
parser.add_argument("-b", "--barcode", type=str, help="goods barcode using as 'goods_id' in db")
parser.add_argument("-n", "--name", type=str, help="goods name")
parser.add_argument("-l", "--label", type=str, help="goods label for training vision model")
parser.add_argument("-m", "--mean", type=float, help="goods mean weight")
parser.add_argument("-s", "--std", type=float, help="goods standard deviation weight")
args = parser.parse_args()


class GoodsAdder:
    def __init__(self, engine, file=None, barcode=None, name=None, label=None, mean=None, std=None):
        self.session = sessionmaker(bind=engine)()
        self.file = file
        self.barcode = barcode
        self.name = name
        self.label = label
        self.mean = mean
        self.std = std

    def run(self):
        assert self.file or (self.barcode and self.name and self.label and self.mean and self.std), "인자 입력 오류"
        if self.file:
            print(f"{self.file}의 데이터 입력")
            self.file_process()
        else:
            print(f"barcode: {self.barcode}, name: {self.name}, label: {self.label}, mean weight: {self.mean}, std weight: {self.std} 입력")
            self.arg_process()
        print("done")

    def file_process(self):
        try:
            df = pd.read_csv(
                self.file,
                dtype={
                    "goods_id": "str",
                    "goods_name": "str",
                    "design_infer_label": "str"
                }
            )
            for d in df.itertuples():
                self.ins_goods_designs(d.goods_id, d.goods_name, d.design_infer_label, d.design_mean_weight, d.design_std_weight)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
    
    def arg_process(self):
        try:
            self.ins_goods_designs(self.barcode, self.name, self.label, self.mean, self.std)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def ins_goods_designs(self, goods_id, goods_name, design_infer_label, design_mean_weight, design_std_weight, ):
        if self.session.query(models.Good).filter_by(goods_id=str(goods_id)).first() is None:
            self.session.add(models.Good(goods_id=goods_id, goods_name=goods_name))
        if self.session.query(models.Design).filter_by(design_infer_label=design_infer_label).first() is None:
            self.session.add(models.Design(
                goods_id=goods_id,
                design_mean_weight=design_mean_weight,
                design_std_weight=design_std_weight,
                design_infer_label=design_infer_label
            ))
        else:
            raise LabelError(message=f"design_infer_label: {design_infer_label} 값이 이미 존재합니다.")


class LabelError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


if __name__ == '__main__':
    if args.engine == "main":
        engine = create_engine(f"postgresql://postgres:{cipher.get('postgres_key')}@{cipher.get('main_db_endpoint')}:5432/emart24")
    elif args.engine == "test":
        engine = create_engine(f"postgresql://postgres:{cipher.get('postgres_key')}@{cipher.get('test_db_endpoint')}:5432/emart24")
    else:
        engine = create_engine(args.engine)

    goods_adder = GoodsAdder(engine, args.file, args.barcode, args.name, args.label, args.mean, args.std)
    goods_adder.run()
