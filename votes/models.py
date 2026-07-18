from django.db import models
from django.conf import settings
from posts.models import Post
from comments.models import Comment


class BaseVote(models.Model):
    value = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
    )
    class Meta:
        abstract = True


class PostVote(BaseVote):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    class Meta:                             # type: ignore
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_post_vote",
            ),
        ]


class CommentVote(BaseVote):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    class Meta:                             # type: ignore
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_comment_vote",
            ),
        ]
