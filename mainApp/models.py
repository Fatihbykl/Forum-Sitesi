from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.contrib.auth.models import User
from django.utils.timezone import now


def upload_to_directory(instance, filename):
    return 'category_images/%s' % filename


class SubCategory(models.Model):
    name = models.CharField(default=1, max_length=50)
    slug = models.SlugField(max_length=50, editable=False)
    image = models.ImageField(blank=False, upload_to=upload_to_directory, default='logo/bestanaliz.png')

    class Meta:
        verbose_name_plural = "Alt Kategoriler"

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(unidecode(self.name))
        new_slug = slug
        num = 0
        while Post.objects.filter(slug=new_slug).exists():
            num += 1
            new_slug = '%s-%s' % (slug, num)
        return new_slug

    def set_slug(self):
        if self.id is None:
            self.slug = self.get_slug()
        else:
            cur_slug = Post.objects.filter(slug=self.slug)
            if cur_slug != self.slug:
                self.slug = self.get_slug()

    def save(self, *args, **kwargs):
        self.set_slug()
        super(SubCategory, self).save(*args, **kwargs)

    def get_last_post(self):
        return Post.objects.filter(category=self).order_by('-created_time').first()

    def get_post_count(self):
        return Post.objects.filter(category=self).count()

    def get_comment_count(self):
        return Comments.objects.filter(which_post__category=self).count()


class Category(models.Model):
    name = models.CharField(default=1, max_length=50)
    slug = models.SlugField(max_length=50, editable=False)
    sub_category = models.ManyToManyField(SubCategory, related_name='sub_category')
    image = models.ImageField(blank=False, upload_to=upload_to_directory, default='logo/bestanaliz.png')

    class Meta:
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(unidecode(self.name))
        new_slug = slug
        num = 0
        while Post.objects.filter(slug=new_slug).exists():
            num += 1
            new_slug = '%s-%s' % (slug, num)
        return new_slug

    def set_slug(self):
        if self.id is None:
            self.slug = self.get_slug()
        else:
            cur_slug = Post.objects.filter(slug=self.slug)
            if cur_slug != self.slug:
                self.slug = self.get_slug()

    def save(self, *args, **kwargs):
        self.set_slug()
        super(Category, self).save(*args, **kwargs)

    def get_subcategories(self):
        return self.sub_category.all()


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(max_length=5000, blank=False)
    created_time = models.DateTimeField(default=now())
    slug = models.SlugField(max_length=150, editable=False)
    category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='subcategory')
    publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_fixed = models.BooleanField(default=0)
    is_locked = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = "Gönderiler"

    def __str__(self):
        return self.title

    def get_slug(self):
        slug = slugify(unidecode(self.title))
        new_slug = slug
        num = 0
        while Post.objects.filter(slug=new_slug).exists():
            num += 1
            new_slug = '%s-%s' % (slug, num)
        return new_slug

    def set_slug(self):
        if self.id is None:
            self.slug = self.get_slug()
        else:
            cur_slug = Post.objects.filter(slug=self.slug)
            if cur_slug != self.slug:
                self.slug = self.get_slug()

    def get_comments(self):
        return self.which_post.all()

    def get_last_comment(self):
        return self.which_post.all().order_by('created_time').first()

    def get_like_count(self):
        return self.post.all().count()


class Comments(models.Model):
    who_comment = models.ForeignKey(User, related_name='who_comment', on_delete=models.CASCADE)
    which_post = models.ForeignKey(Post, related_name='which_post', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(max_length=2000, blank=False)
    reply = models.ForeignKey('self', related_name='reply_quote', on_delete=models.SET_NULL, null=True)
    embed_code = models.CharField(max_length=1000, null=True)

    class Meta:
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return '%s -> %s' % (self.who_comment.username, self.which_post.title)

    def get_like_count(self):
        return self.comment.all().count()


class LikePost(models.Model):
    who_like = models.ForeignKey(User, related_name='who_like', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    time = models.DateTimeField(default=now())

    class Meta:
        verbose_name_plural = 'Gönderi Beğenileri'

    def __str__(self):
        return '%s - %s - %s' % (self.who_like.username, self.post.title, self.time)


class LikeComment(models.Model):
    who_like = models.ForeignKey(User, related_name='who_like_com', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, related_name='comment', on_delete=models.CASCADE)
    time = models.DateTimeField(default=now())

    class Meta:
        verbose_name_plural = 'Yorum Beğenileri'

    def __str__(self):
        return '%s - %s - %s' % (self.who_like.username, self.comment.id, self.time)


class Contact(models.Model):
    email = models.CharField(max_length=75, blank=False)
    name = models.CharField(max_length=70, blank=False, null=True)
    topic = models.CharField(max_length=120, blank=False)
    text = models.TextField(max_length=3000, blank=False)

    class Meta:
        verbose_name_plural = 'İletişim'

    def __str__(self):
        return '%s - %s' % (self.email, self.topic)


class ForumRules(models.Model):
    text = models.TextField(max_length=10000, blank=False)
    update_time = models.DateTimeField(default=now(), editable=False)

    class Meta:
        verbose_name_plural = 'Forum Kuralları'

    def __str__(self):
        return 'Kurallar'

    def save(self, *args, **kwargs):
        self.update_time = now()
        super(ForumRules, self).save(*args, **kwargs)
