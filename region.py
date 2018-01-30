
class RegionClimate:

    def __init__(self, name):
        self.name=name
        self.climate_conditions={}

    def get_climate_conditions(self, condition_name):
        return self.climate_conditions[condition_name]

    def add_condition(self, condition_set):
        pass