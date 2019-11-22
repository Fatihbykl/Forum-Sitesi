from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from mainApp.models import Comments, LikePost, LikeComment


def upload_to_directory(instance, filename):
    return 'user_uploaded_images/%s/%s' % (instance.user.username, filename)


class Ranks(models.Model):
    ROLES = (
        (1, 'Yeni Üye'),
        (2, 'Kıdemli Üye'),
        (3, 'Özel Üye'),
        (4, 'Moderatör'),
        (5, 'Büro Destek'),
        (6, 'Admin'),
    )
    rank                = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    delete_user_perm    = models.BooleanField(default=0, verbose_name='Üye Silme')
    delete_post_perm    = models.BooleanField(default=0, verbose_name='Konu Silme')
    post_lock_perm      = models.BooleanField(default=0, verbose_name='Konu Kilitleme/Açma')
    pin_perm            = models.BooleanField(default=0, verbose_name='Konu Sabitleme')
    edit_post_perm      = models.BooleanField(default=0, verbose_name='Konu Düzenleme (Başkasının)')
    edit_comments_perm  = models.BooleanField(default=0, verbose_name='Mesaj Düzenleme (Başkasının)')
    del_comments_perm   = models.BooleanField(default=0, verbose_name='Mesaj Silme (Başkasının)')

    class Meta:
        verbose_name_plural = 'Rütbeler'

    def __str__(self):
        return '%s' % self.get_rank_display()


class UserProfile(models.Model):
    user        = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo       = models.ImageField(upload_to=upload_to_directory, default='default-pp.png')
    birth_day   = models.DateField(default=datetime.now())
    user_rank   = models.ForeignKey(Ranks, on_delete=models.SET_NULL, null=True, related_name='user_rank')
    point       = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Kullanıcı Profilleri'

    def __str__(self):
        return self.user.username

    def get_age(self):
        today = datetime.today()
        age = today.year - self.birth_day.year - ((today.month, today.day) < (self.birth_day.month, self.birth_day.day))
        return age

    def get_comment_count(self):
        return Comments.objects.filter(who_comment__username=self.user.username).count()

    def get_total_likes(self):
        post = LikePost.objects.filter(post__publisher=self.user).count()
        comment = LikeComment.objects.filter(comment__who_comment=self.user).count()
        return post + comment

    def check_rank(self):
        if self.point >= 5:
            if self.user_rank.rank == 1:
                obj = Ranks.objects.get(rank=2)
                self.user_rank = obj

    def save(self, *args, **kwargs):
        self.check_rank()
        super(UserProfile, self).save(*args, **kwargs)


class Channel(models.Model):
    first_user      = models.ForeignKey(User, related_name='first_user', on_delete=models.CASCADE)
    second_user     = models.ForeignKey(User, related_name='second_user', on_delete=models.CASCADE)
    new_message     = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = 'Mesaj Kanalları'

    def __str__(self):
        return '%s ile %s arasında' % (self.first_user.username, self.second_user.username)

    def get_last_message(self):
        message = Messages.objects.filter(channel_id=self.id).order_by('-timestamp')
        if message.exists():
            return message.first()
        else:
            return None


class Messages(models.Model):
    sender      = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver    = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    message     = models.TextField(max_length=1000, blank=False)
    channel     = models.ForeignKey(Channel, related_name='channel', on_delete=models.CASCADE, null=True)
    is_read     = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = 'Mesajlar'

    def __str__(self):
        return 'Gönderen: %s - Alan: %s - %s' % (self.sender.username, self.receiver.username, self.timestamp)
