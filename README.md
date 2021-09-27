# django-dynamic-admin

Add simple interactions to the otherwise static django admin.

![Demo Animation](docs/demo.gif "Demo")

## Installation

- Install the package via pip:
  
    ```pip install django-dynamic-admin```
    
    or via pipenv:

    ```pipenv install django-dynamic-admin```
- Add the module to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = (
        ...,
        'dynamic_admin',
        'django.contrib.admin'
        ...
    )    
    ```
    Ensure that the `dynamic_admin` comes before the 
    default `django.contrib.admin` in the list of installed apps,
    because otherwise the templates, which are overwritten by `dynamic_admin`
    won't be found.
- Ensure that the `dynamic_admin` templates are found via using `APP_DIRS` setting:
  ```python
  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'APP_DIRS': True,
          ...
      },
  ]
  ```
- Run `python manage.py collectstatic` to include this apps Javascript code in your `settings.STATIC_ROOT` directory

## Usage
- Add the `dynamic_admin.DynamicModelAdminMixin` to your admin classes
- In addition to the standard `fields` declaration, specify a list of `dynamic_fields`
- For each dynamic field, add a method `get_dynamic_{field_name}_field` to the admin
  - Input: `data: Dict[str, Any]` - the cleaned form data
  - Output:
    - `queryset: Optional[Queryset]` - The values to select from
    - `value: Any` - The value, the field should have (must be compatible to the field type)
    - `hidden: Bool` - True, if field should be hidden
  
- A rather non-sensical example:
  ```python
  from django.contrib import admin

  from .models import MyModel
  from dynamic_admin.admin import DynamicModelAdminMixin


  @admin.register(MyModel)
  class MyModelAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    fields = ("name", "city")
    dynamic_fields = ("city",)
  
    def get_dynamic_city_field(self, data):
      # automatically choose first city that matches first letter of name 
      name = data.get("name")
      if not name:
        queryset = City.objects.all()
        value = data.get("city")
      else:
        queryset = City.objects.filter(name__startswith=name[0])
        value = queryset.first()
      hidden = not queryset.exists()
      return queryset, value, hidden
  ```


## How it works
Whenever a dynamic form changes, an event handler makes a request to a special endpoint, which returns new HTML to swap 
into  the existing form. This new HTML is directly generated by `django.contrib.admin`, so we only have to set the 
outerHTML of the correct HTML elements to update the form. 

## Limitations
- does not work in conjunction with inlines
- does not validate that the selected value is really part of the original queryset
  - if anybody can modify your DOM, they could potentially inject invalid values
  - you have to write `Model.clean()` methods to guard against that
- only tested with Django 3.2

## Changelog
- 0.1.0: Initial release
