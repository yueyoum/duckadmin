# -*- coding: utf-8 -*-
"""
Author:         Wang Chao <yueyoum@gmail.com>
Filename:       forms
Date Created:   2015-12-12 21:11
Description:

"""

from django import forms
from duckadmin import DuckForm

from redis import StrictRedis

redis_client = StrictRedis(decode_responses=True)

class MyRedisForm(DuckForm):
    app_label = 'redisapp'
    model_name = 'Person'
    verbose_name = 'Person'
    pk_name = 'id'

    GENDER = (
        (1, 'male'),
        (2, 'female'),
    )

    id = forms.IntegerField()
    name = forms.CharField(max_length=32)
    gender = forms.ChoiceField(choices=GENDER)
    age = forms.IntegerField()


    @classmethod
    def get_data(cls):
        ids = redis_client.lrange('person_ids', 0, -1)
        with redis_client.pipeline() as pipe:
            for i in ids:
                pipe.hgetall('person:{0}'.format(i))

            data = pipe.execute()
            return data

    @classmethod
    def get_data_by_pk(cls, pk):
        data = redis_client.hgetall('person:{0}'.format(pk))
        if not data:
            raise cls.DoesNotExist()
        return data

    @classmethod
    def create_data(cls, data):
        pk = data['id']
        redis_client.rpush('person_ids', pk)
        redis_client.hmset('person:{0}'.format(pk), data)

    @classmethod
    def update_data(cls, data):
        pk = data['id']
        redis_client.hmset('person:{0}'.format(pk), data)
