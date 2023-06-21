from __future__ import unicode_literals

from djsms import send_text


frm = '+201120414067'
to = '+201022919313'
text = 'Please remember to pick up the bread before coming'
message = send_text(text, frm, to)
print(message)