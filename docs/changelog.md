# Changelog

**New in version 0.8.0**: Add `raise_on_error` support if context parsing fails. This release also introduces the `ixbrlError` class if an error is found, instead of a dict - this is a minor breaking change compared to how errors were stored before. Add provisional support for python 3.12.

**New in version 0.7.1**: Allow for case-insensitive schema tags

**New in version 0.7.0**: Add plugin support. Add documentation

**New in version 0.6.0**: Switch to use the [hatch](https://hatch.pypa.io/latest/) build and development system.

**New in version 0.5.4**: Added backreferences to BeautifulSoup objects - thanks to @avyfain for PR.

**New in version 0.5.3**: Support for `exclude` and `continuation` elements within XBRL documents. Thanks to @wcollinscw for adding support for exclude elements.

**New in version 0.5**: Support for Python 3.11 has been added. I've had some problems with Python 3.11 and Windows as lxml binaries aren't yet available. Also new in version 0.5 is type checking - the whole library now has types added. 

**New in version 0.4**: I've added initial support for pure XBRL files as well as tagged HTML iXBRL files. Feedback on this feature is welcome - particularly around getting values out of numeric items.