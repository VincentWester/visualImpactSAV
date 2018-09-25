# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.utils.translation import ugettext as _

DEFAULT_FILE_AS_STATUS_ID = 1
DEFAULT_USERS_ID = 1

#: File AS status choices
FILE_AS_STATUS_TYPE_OPENED = 'O'
FILE_AS_STATUS_TYPE_IN_PROGRESS = 'IP'
FILE_AS_STATUS_TYPE_PROBLEM = 'P'
FILE_AS_STATUS_TYPE_CLOSED = 'C'
FILE_AS_STATUS_CHOICES = (
    (FILE_AS_STATUS_TYPE_OPENED, _("Opened")),
    (FILE_AS_STATUS_TYPE_IN_PROGRESS, _("In progress")),
    (FILE_AS_STATUS_TYPE_PROBLEM, _("Problem")),
    (FILE_AS_STATUS_TYPE_CLOSED, _("Closed"))
)

FONT_STYLE_BOLD = "Helvetica-Bold"
FONT_STYLE = "Helvetica"
FONT_TITLE_SIZE = 20
FONT_NORMAL_SIZE = 12
FONT_SMALLER_SIZE = 10
FONT_SMALL_SIZE = 7
FONT_VERY_SMALL_SIZE = 5
FIELD_SEPARATOR = " : "
NORMAL_SEPARATOR = " - "
COMA_SEPARATOR = ", "

TAX_RATE = Decimal(1.2)

DEFAULT_FILE_AS_LIST_VIEW_PAGINATION_BY = 40
DEFAULT_WARANTY_LIST_VIEW_PAGINATION_BY = 40
DEFAULT_FURNISHER_LIST_VIEW_PAGINATION_BY = 40