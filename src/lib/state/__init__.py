class Global:
    _debug: bool = True
    _on_pause: bool = False

    @property
    def on_pause(self) -> bool:
        if Global._debug:
            print("getter of on_pause called")
        return Global._on_pause

    @on_pause.setter
    def on_pause(self, value: bool) -> None:
        if Global._debug:
            print("setter of on_pause called. New value: %s" % value)
        Global._on_pause = value
