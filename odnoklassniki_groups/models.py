# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from odnoklassniki_api.models import OdnoklassnikiManager, OdnoklassnikiPKModel
from odnoklassniki_api.decorators import fetch_all, atomic
import logging

log = logging.getLogger('odnoklassniki_group')


class GroupRemoteManager(OdnoklassnikiManager):

    fields = [
        'uid',
        'name',
        'description',
        'shortname',
        'pic_avatar',
        'photo_id',
        'shop_visible_admin',
        'shop_visible_public',
        'members_count',
        'premium',
        'private',
#        'admin_id', # with this field strange error
    ]

    @atomic
    def fetch(self, ids, **kwargs):
        kwargs['uids'] = ','.join(map(lambda i: str(i), ids))
        if 'fields' not in kwargs:
            kwargs['fields'] = ','.join(self.fields)
        return super(GroupRemoteManager, self).fetch(**kwargs)

    def update_members_count(self, instances, group, *args, **kwargs):
        group.members_count = len(instances)
        group.save()
        return instances

    @atomic
    @fetch_all(return_all=update_members_count, always_all=True)
    def get_members_ids(self, group, count=1000, **kwargs):
        kwargs['uid'] = group.pk
        kwargs['count'] = count
        response = self.api_call('get_members', **kwargs)
        ids = [m['userId'] for m in response['members']]
        return ids, response


class Group(OdnoklassnikiPKModel):
    class Meta:
        verbose_name = _('Odnoklassniki group')
        verbose_name_plural = _('Odnoklassniki groups')

#     resolve_screen_name_type = 'group'
    methods_namespace = 'group'
    remote_pk_field = 'uid'
    slug_prefix = 'group'

    name = models.CharField(max_length=800)
    description = models.TextField()
    shortname = models.CharField(max_length=50)

    members_count = models.PositiveIntegerField()

    photo_id = models.BigIntegerField(null=True)
    pic_avatar = models.URLField()

    premium = models.NullBooleanField()
    private = models.NullBooleanField()
    shop_visible_admin = models.NullBooleanField()
    shop_visible_public = models.NullBooleanField()

    remote = GroupRemoteManager(methods={
        'get': 'getInfo',
        'get_members': 'getMembers',
    })

    def __unicode__(self):
        return self.name

    @property
    def refresh_kwargs(self):
        return {'ids': [self.pk]}

    def parse(self, response):
        # avatar
        if 'picAvatar' in response:
            response['pic_avatar'] = response.pop('picAvatar')
        super(Group, self).parse(response)