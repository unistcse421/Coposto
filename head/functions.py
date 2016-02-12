# -*- coding: utf-8 -*-
import hashlib, sys
from django.core.mail import send_mail
from django.template.loader import render_to_string

def hashPass(raw_password):
	return hashlib.sha1(raw_password).hexdigest()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, 'avatar.png')

def parcel_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/parcel_<id>/<filename>
    return 'parcel_{0}/{1}'.format(instance.item.id, 'picture.png')

def bring_parcel_email(parcel, bringer):
	msg_plain = render_to_string('bring_parcel_email.txt', {'parcel': parcel, 'sender': parcel.profile_a, 'bringer': bringer})
	# msg_html = render_to_string('templates/email.html', {'some_params': some_params})

	send_mail(
	    'COPOSTO: We found a person to bring your parcel',
	    msg_plain,
	    'info@coposto.com',
	    [parcel.profile_a.email],
	    html_message='',
	)

home_context = {'title': 'COPOSTO',
    			'description': 'Из рук в руки',
    			'send_title': 'Fill the form:',
    			'just_regged': False,
    			'just_regged_text': 'Congratulations! You have successfully registered.',
    			'just_logged_out_text': 'You have just logged out.'
    			}