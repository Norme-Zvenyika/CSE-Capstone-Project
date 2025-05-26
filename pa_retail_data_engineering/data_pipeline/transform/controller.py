from .transform_1999_2014 import Transform1999To2014
from .transform_2015_2016 import Transform2015To2016
from .transform_2017_2021 import Transform2017To2021
from .transform_default_providers_only import TransformDefaultProvidersOnly

class Transform:
    """dispatches to the correct year-range transform logic"""

    def __init__(self, data, year):
        self.data = data
        self.year = year
        self._impl = self._select_transform()

    def _select_transform(self):
        if 1999 <= self.year <= 2014:
            return Transform1999To2014()
        elif 2015 <= self.year <= 2016:
            return Transform2015To2016()
        elif 2017 <= self.year <= 2021:
            return Transform2017To2021()
        elif self.year == 0:
            return TransformDefaultProvidersOnly()
        raise ValueError(f"no transform available for year {self.year}")

    def run(self):
        return self._impl.transform(self.data)
