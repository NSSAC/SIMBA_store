from simbadriver.simbamodule import SimbaModule
from simbastore.simbastores import SimbaStores


class SimbaModuleWithStore(SimbaModule):
    def __init__(self):
        super().__init__()
        self.storefronts = SimbaStores(self.configuration)
