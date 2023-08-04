class Formatter:
    def __init__(self, config, strategy):
        self.config = config
        self.strategy = strategy
        
    def format_data(self, *args):
        return self.strategy.format(self.config, *args)
