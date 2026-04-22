class Teapot:

    VALID_TYPES = frozenset({'h', 's', 'a', 'f'})

    _BASE_WATER_EFFECTS = {
        'h': {'happiness': 30},
        's': {'sadness':   30},
        'a': {'anger':     30},
        'f': {'fear':      30},
    }

    _TEABAG_EFFECTS = {
        'h': {'happiness': 20},
        's': {'sadness':   20},
        'a': {'anger':     20},
        'f': {'fear':      20},
    }

    _TOPPING_EFFECTS = {
        'h': {'happiness': 10, 'fear':      5},
        's': {'sadness':   10, 'happiness': 5},
        'a': {'anger':     10, 'sadness':   5},
        'f': {'fear':      10, 'anger':     5},
    }

    def __init__(self):
        self.basewater: str = 'Not'
        self.teabag:    str = 'Not'
        self.topping:   str = 'Not'

        self.happiness: int = 0
        self.sadness:   int = 0
        self.fear:      int = 0
        self.anger:     int = 0

        self.path_picture: str = "Game_png/Kettle/k.PNG"

    @property
    def is_complete(self) -> bool:
        return (self.basewater != 'Not'
                and self.teabag  != 'Not'
                and self.topping  != 'Not')

    @property
    def stats(self) -> dict:
        return {
            'happiness': self.happiness,
            'sadness':   self.sadness,
            'anger':     self.anger,
            'fear':      self.fear,
        }

    def add_basewater(self, water_type: str) -> bool:
        if water_type not in self.VALID_TYPES:
            return False
        if self.basewater != 'Not':
            return False
        self.basewater = water_type
        self._apply_effects(self._BASE_WATER_EFFECTS[water_type])
        self._update_path()
        return True

    def add_teabag(self, bag_type: str) -> bool:
        if bag_type not in self.VALID_TYPES:
            return False
        if self.basewater == 'Not' or self.teabag != 'Not':
            return False
        self.teabag = bag_type
        self._apply_effects(self._TEABAG_EFFECTS[bag_type])
        self._update_path()
        return True

    def add_topping(self, topping_type: str) -> bool:
        if topping_type not in self.VALID_TYPES:
            return False
        if self.basewater == 'Not' or self.teabag == 'Not' or self.topping != 'Not':
            return False
        self.topping = topping_type
        self._apply_effects(self._TOPPING_EFFECTS[topping_type])
        self._update_path()
        return True

    def _apply_effects(self, effects: dict):
        for emotion, delta in effects.items():
            setattr(self, emotion, getattr(self, emotion) + delta)

    def _update_path(self):
        parts = 'k'
        if self.basewater != 'Not':
            parts += self.basewater
        if self.teabag != 'Not':
            parts += self.teabag
        if self.topping != 'Not':
            parts += self.topping
        self.path_picture = f"Game_png/Kettle/{parts}.PNG"

    def __repr__(self):
        return (f"Teapot(water={self.basewater}, bag={self.teabag}, "
                f"topping={self.topping} | "
                f"hp={self.happiness}, sd={self.sadness}, "
                f"an={self.anger}, fr={self.fear})")