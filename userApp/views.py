from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import SignUpForm, LoginForm, UploadImageForm, EditEmailForm, ChangePasswordForm, MessagesForm
from .models import UserProfile, Ranks, Messages, Channel
from mainApp.models import Post, Comments
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from notifications.signals import notify


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    if request.method == "POST":
        form = SignUpForm(data=request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            birth_day = form.cleaned_data['birth_day']

            user.email = email
            user.set_password(password)
            user.save()
            rank, created = Ranks.objects.get_or_create(rank=1)
            UserProfile.objects.create(user=user, birth_day=birth_day, user_rank=rank)

            auth = authenticate(username=username, password=password)
            if auth and auth.is_active:
                login(request, auth)
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = SignUpForm()
    return render(request, template_name='other/page-signup.html', context={'forms': form})


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    if request.method == 'POST':
        form = LoginForm(data=request.POST or None)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if request.POST.get('checkbox-rememberme', None):
                request.session.set_expiry(604800)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.add_message(request, messages.ERROR, 'Böyle bir hesap bulunamadı.', extra_tags='note--error')
            return render(request, template_name='other/page-login.html', context={'form': form})
    else:
        form = LoginForm()
    return render(request, template_name='other/page-login.html', context={'form': form})


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def view_profile(request, username):
    profile = get_object_or_404(User, username=username)
    return render(request, template_name='profile/page-single-user.html',
                  context={'username': username, 'profile': profile})


def view_profile_topics(request, username):
    post_list = Post.objects.filter(publisher__username=username)
    profile = get_object_or_404(User, username=username)
    ### Pagination ###
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, template_name='profile/page-single_threads.html',
                  context={'username': username, 'posts': posts, 'profile': profile})


def view_profile_replies(request, username):
    profile = get_object_or_404(User, username=username)
    comment_list = Comments.objects.filter(who_comment__username=username)
    ### Pagination ###
    page = request.GET.get('page', 1)
    paginator = Paginator(comment_list, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, template_name='profile/page-single_replies.html',
                  context={'username': username, 'comments': comments, 'profile': profile})


def view_profile_settings(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    user = get_object_or_404(User, username=username)
    email_form = EditEmailForm(instance=user)
    image_form = UploadImageForm()
    password_form = ChangePasswordForm(user=request.user)
    return render(request, template_name='profile/page-single_settings.html',
                  context={'username': username, 'email_form': email_form, 'image_form': image_form,
                           'password_form': password_form, 'profile': user})


def view_profile_admin(request, username):
    return render(request, template_name='profile/page-admin.html', context={'username': username})


def set_user_inactive(request):
    if not request.user.user.user_rank.delete_user_perm:
        return HttpResponseForbidden()
    if request.method == 'POST':
        username = request.POST.get('username-inactive')
        user = User.objects.filter(username=username).first()
        if user:
            if user.is_active:
                user.is_active = False
                user.save()
                msg = '%s adlı kullanıcının hesabı askıya alındı.' % username
                messages.add_message(request, messages.SUCCESS, msg, extra_tags='note--success')
                return HttpResponseRedirect(reverse('view_profile_admin', kwargs={'username': request.user.username}))
            else:
                msg = '%s adlı kullanıcının hesabı zaten askıda.' % username
                messages.add_message(request, messages.WARNING, msg, extra_tags='note--warning')
                return HttpResponseRedirect(reverse('view_profile_admin', kwargs={'username': request.user.username}))
        else:
            msg = '%s adlı kullanıcı mevcut değil.' % username
            messages.add_message(request, messages.ERROR, msg, extra_tags='note--error')
            return HttpResponseRedirect(reverse('view_profile_admin', kwargs={'username': request.user.username}))
    else:
        return HttpResponseBadRequest()


def set_user_active(request):
    if not request.user.user.user_rank.delete_user_perm:
        return HttpResponseForbidden()
    if request.method == 'POST':
        username = request.POST.get('username-active')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.is_active:
                user.is_active = True
                user.save()
                msg = '%s adlı kullanıcı artık hesabına erişebilir.' % username
                messages.add_message(request, messages.SUCCESS, msg, extra_tags='note--success')
                return HttpResponseRedirect(reverse('view_profile_admin', kwargs={'username': request.user.username}))
            else:
                msg = '%s adlı kullanıcının hesabı zaten aktif.' % username
                messages.add_message(request, messages.WARNING, msg, extra_tags='note--warning')
                return HttpResponseRedirect(reverse('view_profile_admin', kwargs={'username': request.user.username}))
        else:
            msg = '%s adlı kullanıcı mevcut değil.' % username
            messages.add_message(request, messages.ERROR, msg, extra_tags='note--error')
            return HttpResponseRedirect(reverse('view_profile_admin', kwargs={'username': request.user.username}))
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/kullanici/giris-yap/')
def change_profile_photo(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    if request.method == 'POST':
        user = get_object_or_404(UserProfile, user=request.user)
        form = UploadImageForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            user.photo = photo
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Profil fotoğrafı başarıyla değiştirildi.',
                                 extra_tags='note--success')
            return HttpResponseRedirect(reverse('view_profile_settings', kwargs={'username': username}))
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/kullanici/giris-yap/')
def change_email(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        form = EditEmailForm(data=request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            user.email = email
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Email başarıyla güncellendi.', extra_tags='note--success')
            return HttpResponseRedirect(reverse('view_profile_settings', kwargs={'username': username}))
        else:
            messages.add_message(request, messages.ERROR, 'Bu email sistemde mevcut!', extra_tags='note--error')
            return HttpResponseRedirect(reverse('view_profile_settings', kwargs={'username': username}))
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/kullanici/giris-yap/')
def change_password(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Şifre başarıyla değiştirildi.', extra_tags='note--success')
            return HttpResponseRedirect(reverse('view_profile_settings', kwargs={'username': username}))
        else:
            messages.add_message(request, messages.ERROR, 'Lütfen girdiğiniz bilgileri kontrol edin.',
                                 extra_tags='note--error')
            return HttpResponseRedirect(reverse('view_profile_settings', kwargs={'username': username}))
    else:
        return HttpResponseBadRequest()


def message_inbox(request, username):
    channels = Channel.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
    return render(request, template_name='messages/messages-page-inbox.html', context={'channels': channels})


def message_detail_inbox(request, id):
    form = MessagesForm()
    channel = get_object_or_404(Channel, id=id)
    channels = Channel.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
    messages = Messages.objects.filter(channel_id=id)
    if messages.last().sender != request.user and channel.new_message:
        channel.new_message = False
        channel.save()
    return render(request, template_name='messages/message-detail-inbox.html',
                  context={'Messages': messages, 'channels': channels, 'form': form, 'id': id})


@login_required(login_url='/kullanici/giris-yap/')
def send_message(request, id):
    if request.method == 'POST':
        form = MessagesForm(data=request.POST or None)
        channel = get_object_or_404(Channel, id=id)
        if request.user != channel.first_user:
            user = channel.first_user
        else:
            user = channel.second_user
        if form.is_valid():
            message = form.cleaned_data['message']
            pk = Messages.objects.create(message=message, channel=channel, sender=request.user, receiver=user)
            if not channel.new_message:
                channel.new_message = True
                channel.save()
            msg = 'Yeni bir mesajın var.'
            notify.send(request.user, recipient=pk.receiver, verb=msg, post_slug='', comment_id='', extra_tag='message')
            return HttpResponseRedirect(reverse('message_detail_inbox', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, message='Form hatalı.')
            return HttpResponseRedirect(reverse('message_detail_inbox', kwargs={'id': id}))
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/kullanici/giris-yap/')
def create_channel(request, username):
    if request.user.username == username:
        return HttpResponseBadRequest()
    channels = Channel.objects.filter((Q(first_user=request.user) and Q(first_user__username=username)) | (
            Q(second_user=request.user) and Q(first_user__username=username)))
    if channels.exists():
        return HttpResponseRedirect(reverse('message_detail_inbox', kwargs={'id': channels.first().id}))
    else:
        user = get_object_or_404(User, username=username)
        pk = Channel.objects.create(first_user=request.user, second_user=user)
        return HttpResponseRedirect(reverse('message_detail_inbox', kwargs={'id': pk.id}))
