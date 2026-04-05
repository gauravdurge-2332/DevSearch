import uuid
from users.models import Userprofile
from django.db import models
from uuid import UUID


# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(
        Userprofile, null=True, blank=True, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tags", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_total']
        '''This is use to order the data according to the created object in the table and if we use "-created"  the data will show newest first'''

    @property
    def imageUrl(self):
        try:
            url = self.featured_image.url
        except:
            url = "/static/images/profiles/default.jpg"
        return url

    @property
    def vote_ratio(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value="up").count()
        total_votes = reviews.count()
        
        if total_votes > 0:
            ratio = (up_votes / total_votes) * 100
        else:
            ratio = 0
            
        return int(ratio)

    @property
    def getcountvote(self):
        reviews = self.review_set.all()
        upvote = reviews.filter(value="up")
        totalupVote = upvote.count()
        self.vote_total = totalupVote
        return self.vote_total


class Review(models.Model):
    owner = models.ForeignKey(Userprofile , on_delete=models.CASCADE ,null = True )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    vote_type = (("up", "up vote"), ("down", "down vote"))
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=vote_type)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [['owner' , 'project']]

    def __str__(self):
        return self.value


class Tags(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
