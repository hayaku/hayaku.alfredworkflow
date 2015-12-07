# encoding: utf-8
from __future__ import print_function

import sys

from alfred_hayaku import get_expanded_hayaku_snippet
from workflow import Workflow

def main(wf):
  if len(wf.args):
      query = wf.args[0]
  else:
      query = None

  result = None

  if query:
    result = get_expanded_hayaku_snippet(query)

  if result:
    print(result, end="")


if __name__ == u"__main__":
  wf = Workflow()
  sys.exit(wf.run(main))
