#! /usr/bin/env python

import glob

files = [f for f in glob.glob('*.md') if f != 'README.md']
files.sort()

names = [
    name[3:-3].replace('_', ' ').capitalize()
    for name in files
]

with open('README.md', 'w') as readme:
    toc = ['# TOC\n\n']
    for name in names:
        toc.append('* [{name}](#{link})\n'.format(link=name.lower().replace(' ', '-'), name=name))
    toc.append('\n\n')
    readme.writelines(toc)

    for name, file in zip(names, files):

        readme.writelines(['\n\n# {}\n\n'.format(name)])

        with open(file) as content:
            readme.writelines(content)
