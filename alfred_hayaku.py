# encoding: utf-8

import json

from hayaku.hayaku_templates import make_template
from hayaku.hayaku_get_merged_dict import get_merged_dict

def get_expanded_hayaku_snippet(query):
  hayaku = {}

  hayaku['options'] = json.loads(open('settings.json').read())

  hayaku['options']['dict'], hayaku['options']['aliases'] = get_merged_dict(hayaku['options'])

  hayaku['abbr'] = query

  snippet = make_template(hayaku, 'plain-text')

  if snippet:
    return snippet
  else:
    return None
