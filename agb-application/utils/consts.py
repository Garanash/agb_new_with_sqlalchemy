from enum import StrEnum, Enum

# ----------------------------------------------------------------
# Metiz types
# ----------------------------------------------------------------


class MetizType(StrEnum):
    Болт = 'Болт'
    Винт = 'Винт'
    Гайка = 'Гайка'
    Шайба = 'Шайба'
    Заглушка = 'Заглушка'
    Заклепка = 'Заклепка'
    Заклепка_вытяжная = 'Заклепка вытяжная'
    Заклепка_резьбовая = 'Заклепка резьбовая'
    Саморез = 'Саморез'
    Шпилька = 'Шпилька'
    Болт_доработанный = 'Болт доработанный'
    Винт_с_шестигранной_головкой = 'Винт с шестигранной головкой'
    Винт_установочный = 'Винт установочный'
    Втулка = 'Втулка'
    Кольцо = 'Кольцо'
    Ось = 'Ось'


# ----------------------------------------------------------------
# Types
# ----------------------------------------------------------------


class MetizTypes(Enum):
    Болт = ['с шестигранной головкой', 'шестигранный с фланцем']
    Винт = ['установочный', 'с потайной головкой и с внутренним шестигранником',
              'с внутренним шестигранником', 'с потайной головкой и крестообразным шлицем',
              'невыпадающий', 'с полукруглой головкой', 'стопорный', 'потайной со шлицем PH',
              'потайной со шлицем PZ', 'H']
    Гайка = ['шестигранная', 'самоконтрящаяся низкая', 'самоконтрящаяся',
              'приварная шестигранная', 'самоконтрящаяся с нейлоновым кольцом',
              'шестигранная с фланцем']
    Шайба = ['плоская увеличенная', 'плоская', 'пружинная', 'Nord-Lock', 'Пружина (шайба) тарельчатая',
              'Шайба упорная быстросъемная']
    Заглушка = ['вытяжная', 'полупустотелая с полукруглой головкой']
    Заклепка = ['рифленная', 'Type A']
    Заклепка_вытяжная = ['цилиндрическая с насечкой', 'шестигранная потайная', 'цилиндрическая с насечкой глухая',
              'цилиндрическая с насечкой', 'Заклепка с внутренней резьбой',
              'цилиндрическая с фланцем и насечками', 'цилиндрическая с уменьшенным бортом и насечками']
    Заклепка_резьбовая = []
    Саморез = ['С шестигранной головкой сверлоконечный ', 'с потайной головкой и крестообразным шлицем',
              'с полукруглой головкой и крестообразным шлицем', 'с пресшайбой и полукруглой головкой']
    Шпилька = []


# ----------------------------------------------------------------
# Standards
# ----------------------------------------------------------------


class MetizStandards(Enum):
    Болт = ["ASME B18.2.1", "DIN931", "DIN933", "DIN6921", "ГОСТ7805-70"]
    Винт = ['ASME B18.3', 'DIN965', 'DIN965A', 'DIN912', 'DIN7985',
              'DIN85', 'DIN913', 'DIN7991', 'ISO 4027', 'DIN7380',
              'DIN84', 'DIN916', 'DIN915']
    Гайка = ['ASME B18.2.2', 'DIN985', 'DIN934', 'DIN982', 'DIN929', 'DIN928', 'DIN6923']
    Шайба = ['DIN9021', 'DIN125', 'DIN127-B', 'DIN25201', 'ГОСТ 3057-90', 'DIN6799']
    Заглушка = ['DIN7337', 'DIN7338', 'DIN660', 'ГОСТ Р ИСО 15973-2005', 'ГОСТ 12641']
    Заклепка = ['DIN7337']
    Заклепка_вытяжная = []
    Заклепка_резьбовая = []
    Саморез = ['DIN7504-N', 'DIN7981', 'DIN7982', 'DIN968', 'DIN969', 'DIN7504-K']
    Шпилька = ['DIN975']


# ----------------------------------------------------------------
# Diameters
# ----------------------------------------------------------------

class MetizDiameter(StrEnum):
    diameter_1 = '2'
    diameter_2 = '2.4'
    diameter_3 = '2.5'
    diameter_4 = '3'
    diameter_5 = '3.2'
    diameter_6 = '3.5'
    diameter_7 = '3.9'
    diameter_8 = '4'
    diameter_9 = '4.2'
    diameter_10 = '4.5'
    diameter_11 = '4.8'
    diameter_12 = '5'
    diameter_13 = '6'
    diameter_14 = '7'
    diameter_15 = '8'
    diameter_16 = '9'
    diameter_17 = '10'

# ----------------------------------------------------------------
# Profiles
# ----------------------------------------------------------------


class MetizProfile(StrEnum):
    profile_1 = 'UNC'
    profile_2 = 'ST'
    profile_3 = 'M'


dict_one = {
    'Болт':["ASME B18.2.1", "DIN931", "DIN933", "DIN6921", "ГОСТ7805-70"],
    'Винт': ['ASME B18.3', 'DIN965', 'DIN965A', 'DIN912', 'DIN7985',
              'DIN85', 'DIN913', 'DIN7991', 'ISO 4027', 'DIN7380',
              'DIN84', 'DIN916', 'DIN915'],
    'Гайка':['ASME B18.2.2', 'DIN985', 'DIN934', 'DIN982', 'DIN929', 'DIN928', 'DIN6923'],
    'Шайба':['DIN9021', 'DIN125', 'DIN127-B', 'DIN25201', 'ГОСТ 3057-90', 'DIN6799'],
    'Заглушка': ['DIN7337', 'DIN7338', 'DIN660', 'ГОСТ Р ИСО 15973-2005', 'ГОСТ 12641'],
    'Заклепка': ['DIN7337'],
    'Заклепка вытяжная':  [],
    'Заклепка резьбовая': [],
    'Саморез': ['DIN7504-N', 'DIN7981', 'DIN7982', 'DIN968', 'DIN969', 'DIN7504-K'],
    'Шпилька':  ['DIN975']
}