#!/usr/bin/env python3

import sys
import re
import pybtex
from pybtex.style.sorting.author_year_title import SortingStyle
from pybtex.plugin import register_plugin


class YearSortingStyle(SortingStyle):

    def sorting_key(self, entry):
        if entry.type in ('book', 'inbook'):
            author_key = self.author_editor_key(entry)
        elif 'author' in entry.persons:
            author_key = self.persons_key(entry.persons['author'])
        else:
            author_key = ''
        return (-int(entry.fields.get('year', '')), author_key, entry.fields.get('title', ''))


register_plugin('pybtex.style.sorting', 'year_author_title', YearSortingStyle)
markdown = pybtex.format_from_file(sys.argv[1], style='plain', output_backend='markdown',
sorting_style='year_author_title', abbreviate_names=True)

markdown = re.sub('(\[\d+\])', '\n\\1', markdown)
# markdown, _ = re.subn(r'\\textbf \\underline N\\., Sonnenschein', '**<u>N., Sonnenschein</u>**', markdown)
markdown, _ = re.subn(r'\\\\textbf.*underline.*Sonnenschein', '**<u>N. Sonnenschein</u>**', markdown)
markdown, _ = re.subn(r'\\\\textbf.*Sonnenschein', '**N. Sonnenschein**', markdown)

print(markdown)

# print(re.sub(r'\\textbf \\underline N\., Sonnenschein\.', '!@#$', markdown))