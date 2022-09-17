from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    sort_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['sort_order']


class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    sticker_max = models.PositiveSmallIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams')
    sort_order = models.PositiveSmallIntegerField(default=0)
    starting_number = models.PositiveSmallIntegerField(default=1)


    @property
    def sticker_range(self):
        return range(self.starting_number , self.starting_number + self.sticker_max)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order']


class Sticker(models.Model):
    number = models.PositiveSmallIntegerField()
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='stickers')

    @property
    def tag(self):
        return f'{self.team.pk}_{self.number}'

    def __str__(self):
        return f'{self.team.code.upper()} {self.number}'

    class Meta:
        ordering = ['number']
        unique_together = ['number', 'team']
