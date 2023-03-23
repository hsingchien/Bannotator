from typing import Callable, List, Union
import inspect


class GuiState(object):
    def __init__(self) -> None:
        self._state_vars = dict()
        self._call_backs = dict()

    def __getitem__(self, key: str):
        return self.get(key)

    def get(self, key: str):
        return self._state_vars.get(key)

    def __setitem__(self, key: str, value):
        old_val = self.get(key)
        self._state_vars[key] = value
        # If state is changed, emit signal and execute callbacks
        if old_val != value:
            self.emit(key)

    def set(self, key: str, value):
        self[key] = value

    def toggle(self, key: str):
        self[key] = not self.get(key)

    def connect(self, key: str, callbacks: Union[Callable, List[Callable]]):
        if callable(callbacks):
            self._connect_callback(key, callbacks)
        else:
            for callback in callbacks:
                self._connect_callback(key, callback)

    def _connect_callback(self, key: str, callback: Callable):
        if not callable(callback):
            raise ValueError("callback must be callable")
        if key not in self._call_backs:
            self._call_backs[key] = []
        self._call_backs[key].append(callback)

    def emit(self, key: str):
        if key in self._state_vars and key in self._call_backs:
            val = self.get(key)
            for i, callback in enumerate(self._call_backs[key]):
                try:
                    if not inspect.signature(callback).parameters:
                        callback()
                    else:
                        callback(val)
                except Exception as e:
                    print(f"Error occured during callback {i} for {key}!")
                    print(self._call_backs[key])
                    print(e)
