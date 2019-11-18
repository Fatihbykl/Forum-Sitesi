from django.urls import path
from .views import homepage, create_post, sub_category, single_topic, make_comment, pin_post, delete_post, \
    delete_comment, lock_post, like_post, contact, send_contact, like_comment, delete_notification, reply_to_comment, \
    edit_post, edit_comment, search, mark_as_read, forum_rules

urlpatterns = [
    path('', homepage, name='homepage'),
    path('iletisim/', contact, name='contact'),
    path('iletisim/gonder/', send_contact, name='send_contact'),
    path('gonderi-olustur/<category_slug>', create_post, name='create_post'),
    path('gonderi/<slug>', single_topic, name='single_topic'),
    path('gonderi/<slug>/yorum-yap/', make_comment, name='make_comment'),
    path('gonderi/<slug>/duzenle/', edit_post, name='edit_post'),
    path('gonderi/<slug>/cevapla/<id>', reply_to_comment, name='reply_to_comment'),
    path('alt-kategori/<slug>', sub_category, name='sub_category'),
    path('alt-kategori/<slug>/<post_slug>/sabitle/', pin_post, name='pin_post'),
    path('gonderi/<slug>/sil/', delete_post, name='delete_post'),
    path('yorum/<id>/sil/', delete_comment, name='delete_comment'),
    path('gonderi/<slug>/kilitle/', lock_post, name='lock_post'),
    path('gonderi/<slug>/begen/', like_post, name='like_post'),
    path('yorum/<id>/begen/', like_comment, name='like_comment'),
    path('yorum/<id>/duzenle/', edit_comment, name='edit_comment'),
    path('bildirim/<slug>/sil/', delete_notification, name='delete_notification'),
    path('gonderi/ara/<slug>', search, name='search'),
    path('bildirim-okundu/', mark_as_read, name='mark_as_read'),
    path('kurallar/', forum_rules, name='forum_rules'),
]
