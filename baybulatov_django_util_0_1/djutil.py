from django.core import validators
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.shortcuts import _get_queryset
from django.utils import timezone
from pprint import pprint, pformat
import datetime
#import natsort
import pydash as _


def get_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_related_or_none(obj, attr):
    try:
        rel = getattr(obj, attr)
    except ObjectDoesNotExist:
        rel = None

    return rel


def has_related(obj, attr):
    try:
        return bool(getattr(obj, attr))
    except ObjectDoesNotExist:
        return False


def get_attr_or_none(klass, *args, attr=None, **kwargs):
    object = get_or_none(klass, *args, **kwargs)

    if object and attr and isinstance(attr, str):
        return getattr(object, attr, None)


def model_fields(model, width=200):
    #fields = natsort.natsorted(model._meta.get_fields(), key=lambda f: f.name)
    fields = model._meta.get_fields()

    pprint([(
        f.name,
        'Relation? %s' % f.is_relation,
        'Null? %s' % getattr(f, 'null', None),
        'Blank? %s' % getattr(f, 'blank', None),
    ) for f in fields], width=width)


def validate_phone(text):
    text = text.replace(' ', '').replace('-', '')

    validate = validators.RegexValidator(
        regex=r'^((\+7|8)(\(\d{3}\)|(\d{3}))\d{7})$',
        message='Неверный номер телефона. Формат: +71112223344',
    )

    validate(text)


def to_local_datetime(obj):
    if not isinstance(obj, datetime.date):
        raise TypeError('Date expected')

    if not isinstance(obj, datetime.datetime):
        obj = datetime.datetime.combine(obj, datetime.time.min)

    if not getattr(obj, 'tzinfo', None):
        obj = timezone.utc.localize(obj)

    return obj
