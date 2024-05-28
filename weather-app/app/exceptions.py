class LocationError(Exception):
    def __init__(self):
        super().__init__("Failed to fetch location")


class DataError(Exception):
    def __init__(self):
        super().__init__("Failed to fetch data")
