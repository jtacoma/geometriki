import codecs
import os

"""Model types and functions for correspondences between tables.
"""
import formencode
from pylons import config

class CorrespondForm (formencode.Schema):
    """Form accepting parameters for correpondence dictionary requests.
    """
    allow_extra_fields = True
    filter_extra_fields = False
    pages = formencode.foreach.ForEach(formencode.validators.UnicodeString())
    input_keys = formencode.foreach.ForEach(formencode.validators.UnicodeString())
    output_keys = formencode.foreach.ForEach(formencode.validators.UnicodeString())
