from django.db import models
from django.contrib.auth.models import User

def uploadMug(instance, filename):
    """
    Returns a directory structure like so:
    /<Candidate's Last Name>/<Filename>
    """
    return '%s/%s' % (instance.user.username, filename)

class Candidate(models.Model):
    """
    Model containing candidate information, including
    - Basic bio: Age, education, occupation, etc.
    - Political Info: What race, what party, campaign website
    - Several other models include this class as a Foreign Key.
    """
    user = models.OneToOneField(User)
    party = models.ForeignKey('Party')
    birthday = models.DateField('Birthday', blank=True, null=True)
    occupation = models.CharField(max_length=150, blank=True)
    education = models.CharField(max_length=200, blank=True)
    accolades = models.CharField(max_length=255, blank=True)
    genStatement = models.TextField(blank=True)
    race = models.ForeignKey('Race')
    website = models.URLField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    mugshot = models.ImageField(upload_to=uploadMug, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
    
class FamilyMember(models.Model):
    """
    Basic model that allows storage of family 
    information.
    This is kept separate to preserve modularity (i.e. Prevent having
    a GIGANTIC candidates model).
    """
    candidate = models.ForeignKey('Candidate')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    age = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "Family member"
        verbose_name_plural = "Family members"
    
class Party(models.Model):
    """
    Literally just a party name.
    This field IS required in the candidate field,
    though the party could be "None."
    """
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Parties"

class Answer(models.Model):
    """
    This model is linked to both the Candidate model and
    the Race model.
    """
    answer = models.CharField(max_length=255)
    candidate = models.ForeignKey('Candidate')
    question = models.ForeignKey('Question')
    edits = models.IntegerField('Number of edits',null=True)
    
    def __unicode__(self):
        return self.answer
        
class Question(models.Model):
    """
    Questions are tied to races, not candidates, to
    allow us to assign questions to an entire slate
    of candidates.
    """
    question = models.CharField(max_length=255)
    race = models.ManyToManyField('Race')
    
    def __unicode__(self):
        return self.question

class Race(models.Model):
    """
    This model is the link between several other models,
    including which questions are tied to each candidate.
    """
    race = models.CharField(max_length=255)
    election_date = models.DateField('Election Date', null=True)
    active = models.BooleanField()
    
    def __unicode__(self):
        return self.race
