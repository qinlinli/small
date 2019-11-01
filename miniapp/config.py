'''
Config for dunkirk.

从环境变量中获取配置

export DEBUG=true
config.debug == True
'''
import os
import json


DEFAULT_CONFIGS = {
    'DEBUG': False,
    'TESTING': False,
    'NODE': '',

    # 密钥
    'SECRET_KEY': None,
    'SQLALCHEMY_DATABASE_URI': '',
    'SQLALCHEMY_POOL_SIZE': 10,
    'SQLALCHEMY_POOL_RECYCLE': 7200,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}


def _get_from_env(name, default=None):
    raw_value = os.environ.get(name, default)
    if raw_value is not None:
        try:
            return json.loads(raw_value)
        except (ValueError, TypeError):
            return raw_value


def load_configs(app):
    for name, value in config.items():
        app.config[name] = value


class Config(object):

    '''
    Dunkirk Config 类

    从系统环境变量中获取配置信息。
    '''

    def __init__(self, update=None):
        # copy
        self._default_configs = {k: v for k, v in DEFAULT_CONFIGS.items()}
        if update:
            self.update(update)

    def update(self, update):
        '''更新默认信息'''
        self._default_configs.update(update)

    def items(self):
        return [(k, self.__getattr__(k))
                for k, _ in self._default_configs.items()]

    def __getattr__(self, name):
        name = name.upper()
        default = self._default_configs.get(name, None)
        return _get_from_env(name, default=default)

config = Config()

