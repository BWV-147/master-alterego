import sys

_version = sys.version_info
if _version.major == 3 and _version.minor <= 7 and False:
    # goto-statement only support Python <=3.7
    from goto import with_goto  # noqa
else:
    # if goto is not supported, avoid errors when using these names
    def with_goto(func):
        return func

    # only support goto .x/label .x
    class _GotoKeyword:
        def __getattr__(self, item):
            return None


    goto = _GotoKeyword()
    label = _GotoKeyword()
