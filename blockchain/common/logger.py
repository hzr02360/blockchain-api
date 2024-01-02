from datetime import datetime
from logging import getLogger, config
import yaml

# logger.ymlを読み込んでloggingライブラリに設定する
with open("logger.yml") as f:
    log_conf = yaml.safe_load(f.read())
    # TODO ログをファイル出力する場合
    # log_conf["handlers"]["fileHandler"]["filename"] = \
    #     '{}.logs'.format(datetime.utcnow().strftime("%Y%m%d%H%M%S"))
    config.dictConfig(log_conf)

# ロガーを生成し返却する
def getAppLogger(name):
    return getLogger(name)
