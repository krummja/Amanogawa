# Amanogawa

## Acknowledgements

`Amanogawa` is built on several existing projects:

- dango
- sudachi.rs
- NLTK
- [JMdict data from Monash University](http://ftp.edrdg.org/pub/Nihongo/00INDEX.html)

## UniDic English Tag Set

| PoS(Ja)         |   PoS (En)   | PoS (En) - descriptions                  |
| --------------- |:------------:| ---------------------------------------- |
| 代名詞             |     Pron     | pronoun                                  |
| 副詞              |      Adv     | adverb                                   |
| 助動詞             |      Aux     | auxiliary_verb                           |
| 助詞-係助詞          |    P.bind    | particle(binding)                        |
| 助詞-副助詞          |     P.adv    | particle(adverbial)                      |
| 助詞-接続助詞         |    P.conj    | particle(conjunctive)                    |
| 助詞-格助詞          |    P.case    | particle(case)                           |
| 助詞-準体助詞         |     P.nom    | particle(nominal)                        |
| 助詞-終助詞          |     P.fin    | particle(phrase_final)                   |
| 動詞-一般           |      V.g     | verb(general)                            |
| 動詞-非自立可能        |     V.bnd    | verb(bound)                              |
| 名詞-助動詞語幹        |     N.aux    | noun(auxiliary)                          |
| 名詞-固有名詞-一般      |   N.prop.g   | noun(proper.general)                     |
| 名詞-固有名詞-人名-一般   |  N.prop.n.g  | noun(proper.name.general)                |
| 名詞-固有名詞-人名-名    |  N.prop.n.f  | noun(proper.name.firstname)              |
| 名詞-固有名詞-人名-姓    |  N.prop.n.s  | noun(proper.name.surname)                |
| 名詞-固有名詞-地名-一般   |  N.prop.p.g  | noun(proper.place.general)               |
| 名詞-固有名詞-地名-国    |  N.prop.p.c  | noun(proper.place.country)               |
| 名詞-数詞           |     N.num    | noun(numeral)                            |
| 名詞-普通名詞-サ変可能    |    N.c.vs    | noun(common.verbal_suru)                 |
| 名詞-普通名詞-サ変形状詞可能 |  N.c.vs.ana  | noun(common.verbal.adjectival)           |
| 名詞-普通名詞-一般      |     N.c.g    | noun(common.general)                     |
| 名詞-普通名詞-副詞可能    |    N.c.adv   | noun(common.adverbial)                   |
| 名詞-普通名詞-助数詞可能   |   N.c.count  | noun(common.counter)                     |
| 名詞-普通名詞-形状詞可能   |    N.c.ana   | noun(common.adjectival)                  |
| 形容詞-一般          |     Ai.g     | adjective_i(general)                     |
| 形容詞-非自立可能       |    Ai.bnd    | adjective_i(bound)                       |
| 形状詞-タリ          |   Ana.tari   | adjectival_noun(tari)                    |
| 形状詞-一般          |     Ana.g    | adjectival_noun(general)                 |
| 形状詞-助動詞語幹       |    Ana.aux   | adjectival_noun(auxiliary)               |
| 感動詞-フィラー        |  Interj.fill | interjection(filler)                     |
| 感動詞-一般          |   Interj.g   | interjection(general)                    |
| 接尾辞-動詞的         |    Suff.v    | suffix(verbal)                           |
| 接尾辞-名詞的-サ変可能    |   Suff.n.vs  | suffix(nominal.verbal_suru)              |
| 接尾辞-名詞的-一般      |   Suff.n.g   | suffix(nominal.general)                  |
| 接尾辞-名詞的-副詞可能    |  Suff.n.adv  | suffix(nominal.adverbial)                |
| 接尾辞-名詞的-助数詞     | Suff.n.count | suffix(nominal.counter)                  |
| 接尾辞-形容詞的        |    Suff.ai   | suffix(adjective_i)                      |
| 接尾辞-形状詞的        |   Suff.ana   | suffix(adjectival_noun)                  |
| 接続詞             |     Conj     | conjunction                              |
| 接頭辞             |     Pref     | prefix                                   |
| 空白              |      Ws      | whitespace                               |
| 補助記号-ＡＡ-一般      |  Supsym.aa.g | supplementary_symbol(ascii_art.general)  |
| 補助記号-ＡＡ-顔文字     |  Supsym.aa.e | supplementary_symbol(ascii_art.emoticon) |
| 補助記号-一般         |   Supsym.g   | supplementary_symbol(general)            |
| 補助記号-句点         |   Supsym.p   | supplementary_symbol(period)             |
| 補助記号-括弧閉        |   Supsym.bo  | supplementary_symbol(bracketopen)        |
| 補助記号-括弧開        |   Supsym.bc  | supplementary_symbol(bracketclose)       |
| 補助記号-読点         |   Supsym.c   | supplementary_symbol(comma)              |
| 記号-一般           |     Sym.g    | symbol(general)                          |
| 記号-文字           |    Sym.ch    | symbol(character)                        |
| 連体詞             |      Adn     | adnominal                                |
| 未知語             |    Unknown   | unknown_words                            |
| カタカナ文           |   Katakana   | katakana                                 |
| 漢文              |    Kanbun    | chinese_writing                          |
| 言いよどみ           |  Hesitation  | hesitation                               |
| web誤脱           |   ErrorOmit  | errors_omissions                         |
| 方言              |    Dialect   | dialect                                  |
| ローマ字文           |      Lat     | latin_alphabet                           |
| 新規未知語           |  NewUnknown  | new_unknown_words                        |
