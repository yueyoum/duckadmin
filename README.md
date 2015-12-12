# Duck Admin
A Django reusable app for show and operate custom forms in admin.

## Purpose

The Django Admin is great!
But it is highly depends on it's orm.

Data source not supported by Django's orm (e.g, redis, mongodb) can not show
in Django's admin site.

This app help you make your data (in redis, mongodb, file...) show in Django's Admin site.
Even you can operate with your data. (Add, Modify, Delete)


## Install

```
pip install duckadmin
```

## Usage

1.  add `'duckadmin'` in `INSTALLED_APPS`
2.  define your form. (you can place it in `forms.py`, `models.py`, anything you like)

    Example:
    ```python
    from duckadmin import DuckForm
    
    class MyRedisForm(DuckForm):
        app_label = 'redisapp'              # your app name
        model_name = 'Person'               # link url 
        verbose_name = 'Person'             # name displayed in admin site
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
            # get all data to display in change list page
            ids = redis_client.lrange('person_ids', 0, -1)
            with redis_client.pipeline() as pipe:
                for i in ids:
                    pipe.hgetall('person:{0}'.format(i))
    
                data = pipe.execute()
                return data
    
        @classmethod
        def get_data_by_pk(cls, pk):
            # change form view
            data = redis_client.hgetall('person:{0}'.format(pk))
            if not data:
                raise cls.DoesNotExist()
            return data
    
        @classmethod
        def create_data(cls, data):
            # when create new data
            pk = data['id']
            redis_client.rpush('person_ids', pk)
            redis_client.hmset('person:{0}'.format(pk), data)
    
        @classmethod
        def update_data(cls, data):
            # when update an exist data
            pk = data['id']
            redis_client.hmset('person:{0}'.format(pk), data)
    ```

3.  define admin. (in file `admin.py`)

    ```python
    from django.contrib import admin
    from duckadmin import DuckAdmin
    from redisapp.forms import MyRedisForm
    
    @admin.register(MyRedisForm)
    class MyRedisAdmin(DuckAdmin):
        duck_form = MyRedisForm

    ```

After this settings. you will see `Person` in admin site.
