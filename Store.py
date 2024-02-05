class Store:
    def set(self, attr: str, val):
        setattr(self, attr, val)
        
    def get(self, attr: str):
        return getattr(self, attr)