from mimesis import Code
from mimesis import Generic
from mimesis.locales import Locale

generic = Generic(locale=Locale.ZH)
code = Code()

print(code.imei())

print(generic.person.username(), generic.datetime.date())

print(generic.address.address(), generic.address.city(), generic.address.province())
