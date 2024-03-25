class StoreFront:
    __stores = {}
    
    def load(configuration):
      pass
      
      
    @classmethod  
    def get(cls, store):
      if store in cls.__stores:
        return cls.__stores[store]
      
      return None
        