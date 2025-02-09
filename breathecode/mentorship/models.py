import re, hashlib
from django.utils import timezone
from breathecode.admissions.models import Academy, Syllabus
from django.contrib.auth.models import User
from django.db import models
from .signals import mentorship_session_status
from slugify import slugify

DRAFT = 'DRAFT'
ACTIVE = 'ACTIVE'
INNACTIVE = 'INNACTIVE'
MENTORSHIP_STATUS = (
    (DRAFT, 'Draft'),
    (ACTIVE, 'Active'),
    (INNACTIVE, 'Innactive'),
)


class MentorshipService(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500, default=None, blank=True, null=True)

    status = models.CharField(max_length=15, choices=MENTORSHIP_STATUS, default=DRAFT)

    language = models.CharField(max_length=2, default='en')

    academy = models.ForeignKey(Academy, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.name} ({self.id})'


INVITED = 'INVITED'
MENTOR_STATUS = (
    (INVITED, 'Invited'),
    (ACTIVE, 'Active'),
    (INNACTIVE, 'Innactive'),
)


class MentorProfile(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, default=None)
    slug = models.SlugField(
        max_length=150,
        unique=True,
        help_text=
        'Will be used as unique public booking URL with the students, for example: 4geeks.com/meet/bob')

    price_per_hour = models.FloatField()

    bio = models.TextField(max_length=500, default=None, blank=True, null=True)

    service = models.ForeignKey(MentorshipService, on_delete=models.CASCADE)

    timezone = models.CharField(max_length=50,
                                null=True,
                                default=None,
                                help_text='Knowing the mentor\'s timezone helps with more accurrate booking')

    online_meeting_url = models.URLField(
        blank=True,
        null=True,
        default=None,
        help_text="If set, it will be default for all session's unless the session.online_meeting_url is set")

    token = models.CharField(max_length=255,
                             unique=True,
                             help_text='Used for inviting the user to become a mentor')

    booking_url = models.URLField(
        blank=True,
        null=True,
        default=None,
        help_text='URL where this mentor profile can be booked, E.g: calendly.com/my_username')

    syllabus = models.ManyToManyField(to=Syllabus,
                                      blank=True,
                                      null=True,
                                      default=None,
                                      help_text='What syllabis is this mentor going to be menting to?')

    status = models.CharField(max_length=15,
                              choices=MENTOR_STATUS,
                              default=INVITED,
                              help_text=f'Options are: {"".join([key for key,label in MENTOR_STATUS])}')

    email = models.CharField(blank=True,
                             max_length=150,
                             null=True,
                             default=None,
                             help_text='Only use this if the user does not exist on breathecode already')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             help_text='If the user does not exist, you can use the email field instead')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):

        utc_now = timezone.now()
        if self.token is None or self.token == '':
            self.token = hashlib.sha1((str(self.user.id) + str(utc_now)).encode('UTF-8')).hexdigest()

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        name = self.name
        if self.user is not None and self.user.first_name is not None and self.user.first_name != '':
            name = self.user.first_name + ' ' + self.user.last_name

        return f'{name} ({self.id}) from {self.service.name}, {self.service.academy.name}'


PENDING = 'PENDING'
STARTED = 'STARTED'
COMPLETED = 'COMPLETED'
FAILED = 'FAILED'
MENTORSHIP_STATUS = (
    (PENDING, 'Pending'),
    (STARTED, 'Started'),
    (COMPLETED, 'Completed'),
    (FAILED, 'Failed'),
)


class MentorshipSession(models.Model):
    def __init__(self, *args, **kwargs):
        super(MentorshipSession, self).__init__(*args, **kwargs)
        self.__old_status = self.status

    is_online = models.BooleanField()
    latitude = models.FloatField(blank=True, null=True, default=None)
    longitude = models.FloatField(blank=True, null=True, default=None)

    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, on_delete=models.CASCADE)

    online_meeting_url = models.URLField(blank=True,
                                         null=True,
                                         default=None,
                                         help_text='Overrides the mentor.online_meeting_url if set')
    online_recording_url = models.URLField(
        blank=True,
        null=True,
        default=None,
        help_text='We encourace the mentors to record the session and share them with the students')

    status = models.CharField(max_length=15,
                              choices=MENTORSHIP_STATUS,
                              default=PENDING,
                              help_text=f'Options are: {", ".join([key for key,label in MENTORSHIP_STATUS])}')

    agenda = models.TextField(blank=True,
                              null=True,
                              default=None,
                              help_text='What will this mentorship be about')
    summary = models.TextField(blank=True,
                               null=True,
                               default=None,
                               help_text='Describe briefly what happened at the mentorship session')

    starts_at = models.DateTimeField(blank=True, null=True, default=None, help_text='Scheduled start date')
    ends_at = models.DateTimeField(blank=True, null=True, default=None, help_text='Scheduled end date')

    started_at = models.DateTimeField(blank=True,
                                      null=True,
                                      default=None,
                                      help_text='Real start date (only if it started)')
    ended_at = models.DateTimeField(blank=True,
                                    null=True,
                                    default=None,
                                    help_text='Real start date (only if it started)')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'(Session {self.id} with {str(self.mentor)} and {str(self.mentee)})'

    def save(self, *args, **kwargs):

        if self.__old_status != self.status:
            mentorship_session_status.send(instance=self, sender=MentorshipSession)

        super().save(*args, **kwargs)  # Call the "real" save() method.
