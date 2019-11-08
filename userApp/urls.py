from django.urls import path
from .views import signup, signin, signout, view_profile, view_profile_topics, view_profile_replies, \
    view_profile_settings, change_profile_photo, change_email, change_password, message_inbox, message_detail_inbox, \
    send_message, create_channel, view_profile_admin, set_user_active, set_user_inactive

urlpatterns = [
    path('kayit-ol/', signup, name='signup2'),
    path('giris-yap/', signin, name='login2'),
    path('cikis-yap/', signout, name='signout2'),
    path('profil/<username>', view_profile, name='view_profile'),
    path('profil/<username>/konular', view_profile_topics, name='view_profile_topics'),
    path('profil/<username>/yanitlar', view_profile_replies, name='view_profile_replies'),
    path('profil/<username>/ayarlar', view_profile_settings, name='view_profile_settings'),
    path('profil/<username>/admin', view_profile_admin, name='view_profile_admin'),
    path('profil/<username>/ayarlar/fotograf-degistir', change_profile_photo, name='change_profile_photo'),
    path('profil/<username>/ayarlar/email-degistir', change_email, name='change_email'),
    path('profil/<username>/ayarlar/sifre-degistir', change_password, name='change_password'),
    path('kullanici/askiya-al', set_user_inactive, name='set_user_inactive'),
    path('kullanici/hesabi-ac', set_user_active, name='set_user_active'),
    path('<username>/gelen-kutusu/', message_inbox, name='message_inbox'),
    path('gelen-kutusu/mesaj/<id>', message_detail_inbox, name='message_detail_inbox'),
    path('mesaj-yolla/<id>', send_message, name='send_message'),
    path('mesaj-olustur/<username>', create_channel, name='create_channel'),
]
