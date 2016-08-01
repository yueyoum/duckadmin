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
2.  define your form. (you can place it in `forms.py`, `models.py`, anywhere you like)

    Demonstration ( more details see [example](/example/redisapp/forms.py) )
    ```python
    from duckadmin import DuckForm
    
    # We define form (not model)
    class MyRedisForm(DuckForm):
        app_label = 'redisapp'              # your app name
        model_name = 'Person'               # link url 
        verbose_name = 'Person'             # name displayed in admin site
        pk_name = 'id'
    
        GENDER = (
            (1, 'male'),
            (2, 'female'),
        )
    
        # fields defined below will show in admin site
        id = forms.IntegerField()
        name = forms.CharField(max_length=32)
        gender = forms.ChoiceField(choices=GENDER)
        age = forms.IntegerField()

        # you should implement the api below:
        # `request` is django request instance

        @classmethod
        def get_count(cls, request):
            # get count of datasets
            # return integer
    
        @classmethod
        def get_data(cls, request, start, stop):
            # get all data to display in change list page
            # return list of data.
            # data is dict format, key is fields defined above
    
        @classmethod
        def get_data_by_pk(cls, request, pk):
            # change form view
    
        @classmethod
        def create_data(cls, request, data):
            # create new data
    
        @classmethod
        def update_data(cls, request, data):
            # update an exist data
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

![admin](/images/admin.png)

And the change list page

![change_list](/images/change_list.png)

You can add, modify record

![change_form](/images/change_form.png)


