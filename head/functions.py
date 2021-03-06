# -*- coding: utf-8 -*-
import hashlib
import smtplib
import sys

from django.conf import settings
from django.template.loader import render_to_string

from email.header import Header
from email.mime.text import MIMEText


def hashPass(raw_password):
    return hashlib.sha1(raw_password).hexdigest()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, 'avatar.png')


def parcel_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/parcel_<id>/<filename>
    return 'parcel_{0}/{1}'.format(instance.item.id, 'picture.png')


def bring_parcel_email(parcel, bringer):
    msg_plain = render_to_string('bring_parcel_email.txt',
                {'parcel': parcel, 'sender': parcel.profile_a, 'bringer': bringer})
    # msg_html = render_to_string('templates/email.html', {'some_params': some_params})

    # Define to/from
    sender = 'admin@coposto.com'
    recipient = parcel.profile_a.email

    # Create message
    msg = MIMEText(msg_plain.encode('utf-8'), 'plain', 'UTF-8')
    msg['Subject'] = Header('COPOSTO: Нашелся Доставщик вашей посылки', 'utf-8')
    msg['From'] = sender
    msg['To'] = recipient

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

    # Perform operations via server
    server.login('admin@coposto.com', 'tentechunist')
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()


def notice_admin(model_name):
    msg_plain = render_to_string('notice_admin.txt',
                                 {'model_name': model_name,
                                  'model_admin_address':
                                  'http://coposto.com/admin/head/' + model_name
                                  })

    # Define to/from
    sender = 'admin@coposto.com'
    recipients = settings.ADMIN_EMAIL_LIST

    # Create message
    msg = MIMEText(msg_plain.encode('utf-8'), 'plain', 'UTF-8')
    msg['Subject'] = Header('COPOSTO: New' + model_name, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(recipients)

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

    # Perform operations via server
    server.login('admin@coposto.com', 'tentechunist')
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()


def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

home_context = {'title': 'COPOSTO',
                'description': 'Из рук в руки',
                'send_form_title': 'Заполните форму:',
                'success_text_send_form': '<strong>Успешно отправлен!</strong> Вам будет выслан, как только кто-то готов помочь. Перезагрузка страницы ...',
                'submit_text': 'Готово',
                'send_text': 'Отправить',
                'bring_text': 'Доставить',
                'from_dest': 'Откуда [кириллица]',
                'to_dest': 'Куда [кириллица]',
                'from_date': 'От',
                'to_date': 'До',
                'date': 'Дата',
                'signup': 'Регистрация',
                'login': 'Войти',
                'logout': 'Выйти',
                'help': 'Помощь',
                'weight': 'Вес',
                'price': 'Назначаемая цена доставки посылки ($)',
                'parcel_picture': 'Рисунок [опциональный]',
                'parcel_name': 'Наименование посылки',
                'parcel_description': 'Описание',

                'bring_form_result': 'Результаты:',
                'author': 'Автор',
                'no_records': 'К сожалению, пока записи отсутствуют.',
                'earn_money_text': 'Вы можете заработать <strong id="total_price"></strong> (долларлов), доставив <strong id="total_weight"></strong> (киллограм)',
                'success_text_bring_form': '<strong>Успешно отправлен!</strong> Скоро Вы будете уведомлены. Перезагрузка страницы...',

                'signup_title': 'Регистрация',
                'first_name': 'Имя',
                'last_name': 'Фамилия',
                'email': 'Эл. адрес',
                'password': 'Пароль',
                'password_confirmation': 'Подтвердите пароль',
                'profile_picture': 'Фото',
                'terms_of_use': 'Пользовательского соглашения',
                'agree_text': 'соглашаться',
                'cancel': 'Отмена',
                'register': 'Зарегистрироваться',
                'success_text_reg_form': '<strong>Поздравляем!</strong> Вы успешно зарегистрировались. Перезагрузка страницы...</div>',

                'forgot_password': 'Забыли пароль?',
                'fail_text_login_form': 'Вы ввели неверный логин или пароль. Пожалуйста, попробуйте еще раз.',
                'success_text_login_form': '<strong>Вошли успешно!</strong> Перезагрузка страницы...',

                'just_regged': False,
                'just_regged_text': 'Congratulations! You have successfully registered.',
                'just_logged_out_text': 'Вы успешно вышли.'
                }