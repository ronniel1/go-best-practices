#! /usr/bin/env python

import glob

files = [f for f in glob.glob('*.md') if f != 'README.md']
files.sort()

names = [
    name[3:-3].replace('_', ' ').capitalize()
    for name in files
]

with open('README.md', 'w') as readme:
    toc = [
        '# Stratoscale Go Best Practices\n\n',
        'Here is a link to the [discussion video](https://stratoscale.zoom.us/recording/play/142yuukXBZ3hXGKyZG6dHLe6iovcQpQZE7TtM1CsgqTFyTo4aqY_oBa5mJmepq7N?autoplay=true).\n\n',
        '# TOC\n\n',
    ]
    for name in names:
        toc.append('* [{name}](#{link})\n'.format(link=name.lower().replace(' ', '-'), name=name))
    toc.append('\n\n')
    readme.writelines(toc)

    for name, file in zip(names, files):

        readme.writelines(['\n\n# {}\n\n'.format(name)])

        with open(file) as content:
            readme.writelines(content)
