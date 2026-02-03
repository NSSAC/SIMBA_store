#!/usr/bin/env python3

from simbastore.simbamodule import SimbaModuleWithStore


class Application(SimbaModuleWithStore):
    def init(self):
        pass

    def start(self) -> bool:
        return True

    def step(self) -> bool:
        return True

    def end(self) -> bool:
        return True


app = Application()
app.execute()
