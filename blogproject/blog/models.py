from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

class Category(models.Model):
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        Django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
     """
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self): return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self): return self.name

class Post(models.Model):
    title = models.CharField('标题',max_length=70)  # 标题
    body = models.TextField('正文')  # 文章正文
    created_time = models.DateTimeField('创建时间',default=timezone.now())  # 文章创建时间
    modified_time = models.DateTimeField('修改时间')  # 文章修改时间
    excerpt = models.CharField('摘要',max_length=200,blank=True)  # 摘要
    """
    这是分类与标签，分类与标签的模型我们已经定义在上面。
    我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    """
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self): return self.title
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})


