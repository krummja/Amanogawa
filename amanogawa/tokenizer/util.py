KATAKANA = (
    'ァアィイゥウェエォオ'
    'ヵカガキギクグヶケゲコゴ'
    'サザシジスズセゼソゾ'
    'タダチヂッツヅテデトド'
    'ナニヌネノ'
    'ハバパヒビピフブプヘベペホボポ'
    'マミムメモ'
    'ャヤュユョヨ'
    'ラリルレロ'
    'ヮワヰヱヲ'
    'ン'
    'ヴ'
    'ヽヾ'
)

HIRAGANA = (
    'ぁあぃいぅうぇえぉお'
    'ゕかがきぎくぐゖけげこご'
    'さざしじすずせぜそぞ'
    'ただちぢっつづてでとど'
    'なにぬねの'
    'はばぱひびぴふぶぷへべぺほぼぽま'
    'みむめもゃやゅゆょよ'
    'らりるれろ'
    'ゎわゐゑを'
    'ん'
    'ゔ'
    'ゝゞ'
)


KATAKANA_TO_HIRAGANA_TRANSLATION_TABLE = str.maketrans(KATAKANA, HIRAGANA)


def katakana_to_hiragana(string: str) -> str:
    """
    Returns a converted string where all katakana have been replaced with their hiragana
    counterparts.
    """
    return string.translate(KATAKANA_TO_HIRAGANA_TRANSLATION_TABLE)
