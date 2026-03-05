# dict-bg-bg — Bulgarian (Български) Dictionary

Word list for use in the [ABCx3](https://abcx3.com) crossword game.

## Source

**bgOffice Bulgarian Dictionary**
© 2001 Radostin Radnev \<radnev@gmail.com\> and contributors
Website: https://bgoffice.sourceforge.net
Distributed via: https://github.com/wooorm/dictionaries (dict `bg`)

## License

**GPL-2.0 OR LGPL-2.1 OR MPL-1.1** (triple-licensed)
This project uses it under **MPL-1.1** (Mozilla Public License 1.1).
The word list is kept in this public repository to satisfy MPL requirements.
Your surrounding application code remains private.

## Word List

**File:** `words_bg-BG.txt`
**Words:** 839,108 inflected Bulgarian word forms
**Length:** 2–15 characters
**Encoding:** UTF-8, sorted alphabetically

### Bulgarian alphabet

`а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ь ю я`

(30 letters of the Bulgarian Cyrillic alphabet)

### What's included

- Nouns: indefinite singular/plural and definite (members) forms
  (e.g. маса, маси, масата, масите)
- Verbs: present/imperfect/past tense, aspect pairs, gerunds, participles
- Adjectives: all gender/definiteness/number inflections
- All other word classes with their full paradigms

### What's excluded

- Proper nouns (uppercased entries — automatically filtered since Bulgarian
  Cyrillic uppercase chars fail the all-lowercase alphabet check)
- Words containing non-Bulgarian characters (digits, hyphens, Latin letters)
- Words shorter than 2 or longer than 15 characters
- Consonant-only sequences (no vowels)

## Word quality

- ✅ Comprehensive inflections (~839k forms from ~72k lowercase stems)
- ✅ No proper nouns (all filtered by lowercase-only constraint)
- ✅ No abbreviations or acronyms (no vowel filter catches them)
- ✅ Pure Bulgarian Cyrillic — no Latin, digits, or punctuation
- ✅ No hyphens, apostrophes, or special characters in any entry

## Regenerating

```bash
pip install spylls
curl -o index.aff https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/bg/index.aff
curl -o index.dic https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/bg/index.dic
python3 process_words.py
```

## Usage in ABCx3

The processed file `words_bg-BG.txt` is imported into the `dict_bg_bg`
database table. The bag configuration uses the standard Bulgarian Cyrillic
alphabet (all 30 letters).
