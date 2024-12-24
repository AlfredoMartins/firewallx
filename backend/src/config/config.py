from config.dev_config import DevConfig

class Config:
    def __init__(self):
        self.dev_config = DevConfig()
        # self.prod_config = prod_config.ProdConfig()