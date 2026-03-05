#!/usr/bin/env python3
"""
Bulgarian dictionary word list generator for ABCx3.

Source: bgOffice Bulgarian dictionary (https://bgoffice.sourceforge.net),
        distributed via wooorm/dictionaries (https://github.com/wooorm/dictionaries)
License: GPL-2.0 OR LGPL-2.1 OR MPL-1.1 (using MPL-1.1)
Copyright: © 2001 Radostin Radnev <radnev@gmail.com> and contributors

Usage:
    1. Download dictionary files:
         curl -o index.aff https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/bg/index.aff
         curl -o index.dic https://raw.githubusercontent.com/wooorm/dictionaries/main/dictionaries/bg/index.dic
    2. Run: python3 process_words.py
    3. Output: words_bg-BG.txt

Requirements:
    pip install spylls

What this script does:
    - Expands all hunspell affix rules (SFX) from the bgOffice dictionary
    - Keeps only lowercase words using the Bulgarian Cyrillic alphabet
    - Filters out proper nouns (uppercase entries → their expanded forms
      always start uppercase and fail the alphabet check)
    - Deduplicates and sorts alphabetically
    - Result: ~839k inflected Bulgarian word forms (nouns: definite/indefinite/
      singular/plural, verbs: present/past/aspect forms, adjectives: all forms)
"""

import sys
from spylls.hunspell import Dictionary

MAX_WORD_LEN = 15
MIN_WORD_LEN = 2

# Bulgarian Cyrillic alphabet (all 30 lowercase letters)
BG_ALPHABET = set('абвгдежзийклмнопрстуфхцчшщъьюя')

# Bulgarian vowels (for filtering consonant-only abbreviations)
BG_VOWELS = set('аеиоуъюя')


def is_valid_bulgarian(word: str) -> bool:
    return all(c in BG_ALPHABET for c in word)


def has_vowel(word: str) -> bool:
    return any(c in BG_VOWELS for c in word)


def expand_dictionary(aff_dic_prefix: str, output_file: str) -> None:
    print(f"Loading dictionary from {aff_dic_prefix}...", file=sys.stderr)
    d = Dictionary.from_files(aff_dic_prefix)
    aff = d.lookuper.aff
    dic = d.lookuper.dic

    total_stems = 0
    written = 0
    results: set[str] = set()

    print("Expanding word forms...", file=sys.stderr)
    for word_entry in dic.words:
        stem = word_entry.stem
        total_stems += 1

        if total_stems % 10000 == 0:
            print(f"  {total_stems} stems → {len(results)} forms so far...", file=sys.stderr)

        # Emit the stem itself if valid
        if (MIN_WORD_LEN <= len(stem) <= MAX_WORD_LEN
                and is_valid_bulgarian(stem)
                and has_vowel(stem)):
            results.add(stem)

        flags = list(word_entry.flags)
        if not flags:
            continue

        # Apply SFX (suffix) rules — Bulgarian has no PFX rules
        for flag in flags:
            for rule in aff.SFX.get(flag, []):
                try:
                    if rule.cond_regexp and not rule.cond_regexp.search(stem):
                        continue
                except Exception:
                    continue

                base = stem
                if rule.strip:
                    if stem.endswith(rule.strip):
                        base = stem[:-len(rule.strip)]
                    else:
                        continue

                new_word = base + (rule.add or '')

                if (MIN_WORD_LEN <= len(new_word) <= MAX_WORD_LEN
                        and is_valid_bulgarian(new_word)
                        and has_vowel(new_word)):
                    results.add(new_word)

    print(f"\nExpansion done: {total_stems} stems → {len(results)} unique forms", file=sys.stderr)

    sorted_words = sorted(results)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted_words) + '\n')

    print(f"Output written to: {output_file}", file=sys.stderr)
    print(f"Final word count: {len(sorted_words):,}", file=sys.stderr)


if __name__ == '__main__':
    expand_dictionary('index', 'words_bg-BG.txt')
