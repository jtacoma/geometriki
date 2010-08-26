# This file is part of geometriki.
#
# geometriki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# geometriki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with geometriki, in a file named COPYING. If not,
# see <http://www.gnu.org/licenses/>.
import docutils.core
import docutils.parsers.rst
import json

def rst2html(txt):
    inliner = docutils.parsers.rst.states.Inliner()
    parser = docutils.parsers.rst.Parser(inliner=inliner)
    content = unicode(txt)
    settings = dict(file_insertion_enabled=0, raw_enabled=0, _disable_config=1)
    parts = docutils.core.publish_parts(content, writer_name='html', parser=parser,
            settings_overrides=settings)
    html = parts['html_body']
    return html

def rst2data(txt):
    parser = docutils.parsers.rst.Parser()
    document = docutils.utils.new_document('buffer')
    document.settings.tab_width = 4
    document.settings.pep_references = 1
    document.settings.rfc_references = 1
    document.settings.trim_footnote_reference_space = None
    parser.parse(txt, document)
    dom = document.asdom()
    queue = list(dom.childNodes)
    all_tables = []
    while queue:
        node = queue.pop()
        if not hasattr(node, 'tagName'):
            continue
        elif node.tagName == 'table':
            all_tables.append(node)
        else:
            queue.extend(node.childNodes)
    all_parsed = []
    records = []
    meta = {}
    for table in all_tables:
        meta = {}
        tgroup = table.childNodes[0]
        keys = [[] for n in tgroup.childNodes if n.localName == 'colspec']
        thead = tgroup.childNodes[len(keys)]
        # a grid of column headers:
        heads = [[None for row in thead.childNodes] for k in keys]
        for rowindex, row in enumerate(thead.childNodes):
            row_items = []
            coloffset = 0
            for colindex, th in enumerate(row.childNodes):
                while heads[colindex+coloffset][rowindex] is not None:
                    coloffset += 1
                if th.attributes.has_key('morecols'):
                    colspan = int(th.attributes['morecols'].value) + 1
                else:
                    colspan = 1
                if th.attributes.has_key('morerows'):
                    rowspan = int(th.attributes['morerows'].value) + 1
                else:
                    rowspan = 1
                name = th.childNodes[0].childNodes[0].nodeValue
                for ci in range(colindex+coloffset, colindex+coloffset+colspan):
                    heads[ci][rowindex] = name
                    for ri in range(rowindex+1, rowindex+rowspan):
                        heads[ci][ri] = ''
                thusfar = '.'.join(r for r in heads[colindex+coloffset] if r)
                meta[thusfar] = meta.get(thusfar, 0) + colspan
        names = ['.'.join(r for r in col if r) for col in heads]
        for name in list(meta.keys()):
            if name not in names:
                del meta[name]
        tbody = tgroup.childNodes[len(keys)+1]
        for row in tbody.childNodes:
            values = [td.childNodes[0].childNodes[0].nodeValue for td in row.childNodes]
            record = {}
            for name, value in zip(names, values):
                if value.isdigit(): value = int(value)
                if meta[name] > 1:
                    record[name] = record.get(name, []) + [value]
                else:
                    record[name] = value
            records.append(record)
    return dict(meta=meta, records=records)

def rst2json(txt):
    data = rst2data(txt)
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
