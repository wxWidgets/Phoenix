# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Name:        sphinxtools/stc_doc_postprocess.py
# Author:      Matthias (neofelis2X)
#
# Created:     27-Jan-2025
# Copyright:   (c) 2010-2025
# License:     wxWindows License
#---------------------------------------------------------------------------
"""
This script postprocesses the ReST documentation file of the
wx.stc.StyledTextCtrl class. This class has more than 760 methods,
so the 'Method Summary' is sorted into categories.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

from buildtools.config import msg
from sphinxtools.constants import XMLSRC, SPHINXROOT

STC_CLASS_XML = Path(XMLSRC, "classwx_styled_text_ctrl.xml")
STC_RST = Path(SPHINXROOT, "wx.stc.StyledTextCtrl.txt")
TBL_SEP = "======================================================" + \
          "========================== ===========================" + \
          "=====================================================\n"

def _parse_method_categories(xml_file):
    """
    Parses values from an xml file containing categories, method
    names and occasional additional category descriptions.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    method_mapping = {}
    current_category = "empty"
    current_pretty = "Empty"
    description = ''
    new_header = False

    for elem in root.iter():
        if elem.tag == 'listofallmembers':
            break

        if elem.tag == "header" and isinstance(elem.text, str):
            if "Raw variants" in elem.text:
                current_category = "Raw Variants"
                current_pretty = "Raw Variants"
            else:
                current_category = elem.text
                current_pretty = _clean_category_title(current_category)

            description = ''
            new_header = True

        elif elem.tag == "description" and new_header:
            para = elem.findall("para")
            description = _parse_description(para)

            new_header = False

        elif elem.tag == "name":
            method_mapping[elem.text] = (current_pretty, description)

    return method_mapping

def _parse_description(para):
    """
    Goes through some extra steps to parse method descriptions from references.
    """
    description = ''

    if len(para) > 1:
        txt = para[1].itertext()
        sect = para[1].findall("simplesect")

        if len(sect):
            description = "".join(txt).split('(', maxsplit=1)[0].strip()
            description = f".. seealso:: :meth:`~wx.stc.StyledTextCtrl.{description}`"
        else:
            description = "".join(txt).strip()

    return description

def _parse_stcdoc_segments(file):
    """
    Read the reStructuredText file and split relevant parts into textblocks.
    """

    m_count = 0  # Count the collected methods
    pretext = ''  # All text before the 'Method Summary'
    parse_pretext = True
    links = []  #
    index_links_done = False
    methods = {}
    current_method = ''
    parse_methods = False
    posttext = ''  # All text after the 'Method Summary'
    parse_posttext = False

    with open(file, 'r', encoding="utf-8") as f:
        for line in f:

            if parse_posttext:
                posttext += line

            elif not index_links_done and line.startswith("- `"):
                # Rewrite index links
                new_link = line.split('<')[0].strip("-_ `")
                new_link = _clean_category_title(new_link)
                pretext += f"- `{new_link}`_\n"
                links.append(new_link)

                if "Constructors" in line:
                    awm = "Additional wxPython Methods"
                    pretext += f"- `{awm}`_\n"
                    links.append(awm)

                elif "Text area methods" in line:
                    index_links_done = True

            elif line.startswith(":meth:`~wx.stc.StyledTextCtrl."):
                # Collect all methods from 'Method Summary'
                m_count += 1
                parse_pretext = False
                parse_methods = True

                current_method = line[30:].split('`')[0].strip()

                if not current_method:
                    print("stc_doc_postprocess:: WARNING: Invalid method name")
                else:
                    methods[current_method] = line

            elif parse_methods and line.strip() == '|':
                parse_methods = False
                parse_posttext = True
                posttext = '\n' + line

            elif parse_pretext:
                if not TBL_SEP.strip() in line:
                    pretext += line

        # print(f"Debug: Read {m_count} methods from file.")
        return (pretext, methods, posttext, links)

def _methods_to_categories(methods, mapping):
    """
    Find the right category for each method. Around 20 methods are
    unique in wxPython and will be put into their own group.
    """
    grouped_methods = {}

    for name, text in methods.items():

        if name in ("__init__", "Create"):
            category = "Constructors and Related Methods"
            description = ''
            text = text.replace("Ctor.", '')

        elif name in mapping:
            category = mapping[name][0]
            description = mapping[name][1]

        else:
            category = "Additional wxPython Methods"
            description = "In addition to the standard Scintilla " + \
                          "functions, wxPython includes the following " + \
                          "methods to better integrate better with other features."

        if category in grouped_methods:
            grouped_methods[category][0].append(text)
            grouped_methods[category][1] = description
        else:
            grouped_methods[category] = [[text, ], '']

        if description:
            grouped_methods[category][1] = description

    return grouped_methods

def _clean_category_title(raw_title):
    """
    Applies proper title case to category titles.
    """
    category_title = raw_title.strip().title().replace("And", "and")
    category_title = category_title.replace("Wxstyledtextctrl", "wxStyledTextCtrl")
    category_title = category_title.replace("Wxpython", "wxPython")

    return category_title

def _assemble_method_category(category, cat_methods, cc):
    """
    Assembles all method ReST directives that go into one category.
    """
    group = ''

    dashline = '-' * len(category)
    group = f"\n{category}\n{dashline}\n\n"

    if cat_methods[1]:
        group += '\n' + cat_methods[1] + '\n\n'

    group += TBL_SEP

    for method in cat_methods[0]:
        cc += 1
        group += method

    group += TBL_SEP + '\n'

    return group, cc

def _output_reordered_doc(pretext, posttext, grouped_methods):
    """
    Writes the formatted ReST to a file. Overwrites the original file.
    """
    m_count = 0  # count the written methods
    doc = pretext

    for category, methods in grouped_methods.items():
        cat, m_count = _assemble_method_category(category, methods, m_count)
        doc += cat

    doc += posttext

    STC_RST.write_text(doc, encoding="utf-8")

    # print(f"Debug: Wrote {m_count} methods to new file.")

def stc_categorise_methods():
    """
    Loads the ReST file, categorises the method summary and saves a new file. 
    Thr original file is overwritten.
    """
    if not STC_CLASS_XML.is_file():
        return msg(f"Warning: StyledTextCtrl post-processing failed: {STC_CLASS_XML.name} not available.")

    mapping = _parse_method_categories(STC_CLASS_XML)

    if not STC_RST.is_file():
        return msg(f"Warning: StyledTextCtrl post-processing failed: {STC_RST.name} not available.")

    pre, methods, post, links = _parse_stcdoc_segments(STC_RST)
    grouped_methods = _methods_to_categories(methods, mapping)
    sorted_methods = {key: grouped_methods[key] for key in links}
    _output_reordered_doc(pre, post, sorted_methods)

    return msg("StyledTextCtrl post-processing completed successfully.")


if __name__ == "__main__":
    stc_categorise_methods()

