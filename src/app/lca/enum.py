import enum


class UnitEnum(enum.Enum):

    @property
    def unit_name(self):
        return self.value[0]

    @property
    def symbol(self):
        return self.value[1]


class MaterialUnitEnum(UnitEnum):
    KILOGRAM = ("kilogram", "kg")


class ElectricityUnitEnum(UnitEnum):
    KILOWATT_HOUR = ("kilowatt hour", "kWh")
