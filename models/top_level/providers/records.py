from enum import Enum


class ProviderTypes(Enum):
    FEATURE = "feature"
    MAP = "map"
    TILE = "tile"


class Languages(Enum):
    NONE = ""
    EN_US = "en-US"
    EN_GB = "en-GB"
    FR_CA = "fr-CA"
    FR_FR = "fr-FR"
    PT_PT = "pt-PT"


class TrsAuthorities(Enum):
    ISO8601 = "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"


class CrsAuthorities(Enum):
    OGC13 = "OGC/1.3"
    OGC0 = "OGC/0"
    AUTO = "AUTO/1.3"
    EPSG0 = "EPSG/0"
    EPSG85 = "EPSG/8.5"
    EPSG892 = "EPSG/8.9.2"
    EPSG942 = "EPSG/9.4.2"
    EPSG953 = "EPSG/9.5.3"
    EPSG954 = "EPSG/9.5.4"
    EPSG96 = "EPSG/9.6"
    EPSG961 = "EPSG/9.6.1"
    EPSG963 = "EPSG/9.6.3"
    EPSG965 = "EPSG/9.6.5"
    EPSG981 = "EPSG/9.8.1"
    EPSG982 = "EPSG/9.8.2"
    EPSG983 = "EPSG/9.8.3"
    EPSG984 = "EPSG/9.8.4"
    EPSG986 = "EPSG/9.8.6"
    EPSG987 = "EPSG/9.8.7"
    EPSG9811 = "EPSG/9.8.11"
    EPSG9813 = "EPSG/9.8.13"
    EPSG9814 = "EPSG/9.8.14"
    EPSG9815 = "EPSG/9.8.15"
    EPSG99 = "EPSG/9.9"
    EPSG991 = "EPSG/9.9.1"
    IAU0 = "IAU/0"
    IAU2015 = "IAU/2015"
