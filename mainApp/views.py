from .forms import PostForm, CommentForm, ContactForm
from .models import Category, Post, SubCategory, Comments, LikePost, LikeComment, ForumRules
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.core.mail import BadHeaderError
from notifications.signals import notify
from notifications.models import Notification
from notifications.utils import slug2id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string

LIKE_POINT = 4
GET_LIKE_POINT = 10
COMMENT_POINT = 1


def homepage(request):
    category = Category.objects.all()
    subcategories = SubCategory.objects.all()
    posts = Post.objects.all()
    comments = Comments.objects.all().count()
    users = User.objects.all()
    last_user = users.order_by('-date_joined').first()
    return render(request, template_name='other/index.html',
                  context={'categories': category, 'posts': posts, 'subcategories': subcategories,
                           'all_posts': posts.count(), 'all_comments': comments, 'all_users': users.count(),
                           'last_user': last_user})


@login_required(login_url='/kullanici/giris-yap/')
def create_post(request, category_slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signup'))
    form = PostForm(data=request.POST or None)
    category = get_object_or_404(SubCategory, slug=category_slug)
    if form.is_valid():
        pk = form.save(commit=False)
        pk.title = form.cleaned_data['title']
        pk.body = form.cleaned_data['body']
        pk.publisher = request.user
        pk.category = category
        pk.set_slug()

        pk.save()
        return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': pk.slug}))
    return render(request, template_name='post-temps/page-create-topic.html',
                  context={'form': form, 'category': category})


def sub_category(request, slug):
    category = get_object_or_404(SubCategory, slug=slug)
    post_list = Post.objects.filter(category=category, is_fixed=False).order_by('-id')
    fixed_posts = Post.objects.filter(is_fixed=True, category=category)
    ### Pagination ###
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, template_name='post-temps/page-categories-single.html',
                  context={'posts': posts, 'category': category, 'fixed_posts': fixed_posts})


def search(request, slug):
    category = get_object_or_404(SubCategory, slug=slug)
    word = request.GET.get('search')
    posts = Post.objects.filter(Q(title__icontains=word) | Q(body__icontains=word))
    return render(request, template_name='post-temps/page-search.html',
                  context={'posts': posts, 'category': category, 'word': word})


def single_topic(request, slug):
    topic = get_object_or_404(Post, slug=slug)
    comment_form = CommentForm()
    hit_count = HitCount.objects.get_for_object(topic)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    print(hit_count_response)
    ### Pagination ###
    page = request.GET.get('page', 1)
    paginator = Paginator(topic.get_comments(), 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, template_name='post-temps/page-single-topic.html',
                  context={'post': topic, 'commentForm': comment_form, 'posts': comments})


@login_required(login_url='/kullanici/giris-yap/')
def make_comment(request, slug):
    if request.method == 'POST':
        form = CommentForm(data=request.POST or None)
        post = get_object_or_404(Post, slug=slug)
        if form.is_valid():
            if not post.is_locked:
                embed = request.POST.get('embed-input')
                print(embed)
                pk = form.save(commit=False)
                if embed:
                    pk.embed_code = embed
                pk.who_comment = request.user
                pk.which_post = post
                pk.save()
                request.user.user.point += COMMENT_POINT
                request.user.user.save()
                if request.user != post.publisher:
                    msg = '%s gönderinize yorum yaptı.' % request.user.username
                    notify.send(request.user, recipient=post.publisher, verb=msg, post_slug=post.slug, comment_id=pk.id,
                                extra_tag='comment')
                return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': slug}))
            else:
                messages.add_message(request, messages.ERROR, 'Kilitli bir gönderiye yorum yapamazsın!',
                                     extra_tags='note--error')
                return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.add_message(request, messages.ERROR, 'Yorum yaparken bir hata oluştu.', extra_tags='note--error')
            return HttpResponseRedirect(reverse('homepage'))
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/kullanici/giris-yap/')
def edit_comment(request, id):
    comment = get_object_or_404(Comments, id=id)
    if not request.user.user.user_rank.edit_comments_perm and request.user != comment.who_comment:
        return HttpResponseForbidden()
    form = CommentForm(instance=comment, data=request.POST or None)
    if request.user.user.user_rank.edit_post_perm:
        comment.admin_edit = True
        comment.which_admin_edit = request.user.username
        comment.save()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Yorum başarıyla düzenlendi.', extra_tags='note--success')
            return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': comment.which_post.slug}))
        else:
            messages.add_message(request, messages.ERROR, 'Lütfen formu kontrol et.', extra_tags='note--error')
            return render(request, template_name='post-temps/edit-comment.html',
                          context={'form': form, 'comment': comment})
    else:
        return render(request, template_name='post-temps/edit-comment.html',
                      context={'commentForm': form, 'comment': comment, 'id': id})


@login_required(login_url='/kullanici/giris-yap/')
def reply_to_comment(request, slug, id):
    form = CommentForm(data=request.POST or None)
    post = get_object_or_404(Post, slug=slug)
    reply = get_object_or_404(Comments, id=id)
    if form.is_valid():
        pk = form.save(commit=False)
        pk.who_comment = request.user
        pk.which_post = post
        pk.reply = reply
        pk.save()
        request.user.user.point += COMMENT_POINT
        request.user.user.save()
        if request.user != reply.who_comment:
            msg = '%s bir yorumda sizden bahsetti.' % request.user.username
            notify.send(request.user, recipient=reply.who_comment, verb=msg, post_slug=post.slug, comment_id=pk.id,
                        extra_tag='reply')
        return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': slug}))
    else:
        return render(request, 'post-temps/reply_comments.html',
                      context={'id': id, 'commentForm': form, 'reply': reply})


def pin_post(request, slug, post_slug):
    if not request.user.user.user_rank.pin_perm:
        return HttpResponseForbidden()
    post = get_object_or_404(Post, slug=post_slug)
    if post.is_fixed:
        post.is_fixed = False
        messages.add_message(request, messages.SUCCESS, 'Konu sabit konulardan kaldırıldı.',
                             extra_tags='note--success')
    else:
        post.is_fixed = True
        messages.add_message(request, messages.SUCCESS, 'Konu sabitlendi.', extra_tags='note--success')
    post.save()
    return HttpResponseRedirect(reverse('sub_category', kwargs={'slug': slug}))


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    slug_category = post.category.slug
    if request.user == post.publisher or request.user.user.user_rank.delete_post_perm:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Konu başarıyla silindi.', extra_tags='note--success')
        return HttpResponseRedirect(reverse('sub_category', kwargs={'slug': slug_category}))
    else:
        return HttpResponseForbidden()


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post, data=request.POST or None)
    if not request.user.user.user_rank.edit_post_perm and request.user != post.publisher:
        return HttpResponseForbidden()
    if request.user.user.user_rank.edit_post_perm:
        post.admin_edit = True
        post.which_admin_edit = request.user.username
        post.save()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Konu başarıyla düzenlendi.', extra_tags='note--success')
            return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': slug}))
        else:
            messages.add_message(request, messages.ERROR, 'Lütfen formları kontrol ediniz.', extra_tags='note--error')
            return render(request, template_name='post-temps/page-edit-post.html', context={'form': form, 'post': post})
    else:
        return render(request, template_name='post-temps/page-edit-post.html', context={'form': form, 'post': post})


def delete_comment(request, id):
    comment = get_object_or_404(Comments, id=id)
    post_slug = comment.which_post.slug
    if request.user == comment.who_comment or request.user.user.user_rank.del_comments_perm:
        comment.delete()
        comment.who_comment.user.point -= COMMENT_POINT
        comment.who_comment.user.save()
        messages.add_message(request, messages.SUCCESS, 'Yorum başarıyla silindi.', extra_tags='note--success')
        return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': post_slug}))
    else:
        return HttpResponseForbidden()


def lock_post(request, slug):
    if not request.user.user.user_rank.post_lock_perm:
        return HttpResponseForbidden()
    post = get_object_or_404(Post, slug=slug)
    post.is_locked = True
    post.save()
    messages.add_message(request, messages.SUCCESS, 'Konu kilitlendi.', extra_tags='note--success')
    return HttpResponseRedirect(reverse('single_topic', kwargs={'slug': slug}))


def like_post(request, slug):
    if not request.user.is_authenticated:
        return HttpResponse('f')
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    if user == post.publisher:
        return HttpResponse('liked')
    like = LikePost.objects.filter(post=post, who_like=user)
    if not like.exists():
        LikePost.objects.create(post=post, who_like=user)
        user.user.point += LIKE_POINT
        user.user.save()
        post.publisher.user.point += GET_LIKE_POINT
        post.publisher.user.save()
        msg = '%s gönderini beğendi.' % request.user.username
        notify.send(request.user, recipient=post.publisher, verb=msg, post_slug=post.slug, comment_id='',
                    extra_tag='like')
        return HttpResponse(post.get_like_count())
    else:
        return HttpResponse('liked')


def like_comment(request, id):
    if not request.user.is_authenticated:
        return HttpResponse('f')
    comment = get_object_or_404(Comments, id=id)
    user = request.user
    if user == comment.who_comment:
        return HttpResponse('liked')
    like = LikeComment.objects.filter(comment=comment, who_like=user)
    if not like.exists():
        LikeComment.objects.create(comment=comment, who_like=user)
        user.user.point += LIKE_POINT
        user.user.save()
        comment.who_comment.user.point += GET_LIKE_POINT
        comment.who_comment.user.save()
        msg = '%s yorumunu beğendi.' % request.user.username
        notify.send(request.user, recipient=comment.who_comment, verb=msg, post_slug=comment.which_post.slug,
                    comment_id=comment.id, extra_tag='like')
        return HttpResponse(comment.get_like_count())
    else:
        return HttpResponse('liked')


def contact(request):
    form = ContactForm()
    return render(request, template_name='other/page-contact.html', context={'form': form})


def send_contact(request):
    form = ContactForm(data=request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        topic = "BestAnaliz İletişim | " + form.cleaned_data['topic']
        text = form.cleaned_data['text']
        name = form.cleaned_data['name']
        form.save()

        d = {'name': name, 'email': email, 'content': text}

        plaintext = render_to_string('contact_mail/subject.txt')
        htmly = render_to_string('contact_mail/content.html', d)

        try:
            msg = EmailMultiAlternatives(topic, 'info@bestanaliz.com', plaintext, ['Bestanaliz@outlook.com'])
            msg.attach_alternative(htmly, 'text/html')
            msg.send()
        except BadHeaderError:
            messages.add_message(request, messages.ERROR, 'Geçersiz header bulundu.', extra_tags='note--error')
            return HttpResponseRedirect(reverse('contact'))

        messages.add_message(request, messages.SUCCESS, 'Bizimle iletişime geçtiğin için teşekkürler!',
                             extra_tags='note--success')
        return HttpResponseRedirect(reverse('homepage'))
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen girdiğiniz bilgileri kontrol edin.',
                             extra_tags='note--error')
        return HttpResponseRedirect(reverse('contact'))


@login_required(login_url='/kullanici/giris-yap/')
def delete_notification(request, slug):
    notif_id = slug2id(slug)
    notif = get_object_or_404(Notification, recipient=request.user, id=notif_id)
    notif.delete()
    return HttpResponse('Bildirim Silindi.')


def mark_as_read(request):
    request.user.notifications.mark_all_as_read()
    return HttpResponse('okundu')


def forum_rules(request):
    rules = ForumRules.objects.all().first()
    return render(request, template_name='other/page-rules.html', context={'rules': rules})
