Control Panel
=============

Currently development still in progress.

Available features:

* Users are assigned to sections and privileges groups


Lower group can:

* log in/logout from panel
* send vacation day request
* read announcements
* simple search through items
* send stocktaking form


Higher group can:

* log in/logout from panel
* create new user in a lower group; higher group users can be created by admin
* set vacation days
* query and accept/decline/delete vacation days requests
* read/write/edit announcements
* add new items and place them in sections
* simple and advanced search through added items
* send stocktaking form


Future features:

* Inventory section: browsing through sent stocktaking forms
* Inventory section: removing/editing items in sections

## Installation

* clone sources
* create database and db user, set as env vars, ex. DJANGO_DBNAME, DJANGO_DBUSER, DJANGO_DBPASS
* apply migrations: `python manage.py migrate`
* add superuser by calling `python manage.py createsuperuser`
* add two groups: `hi_user`, `low_user`: `g = Group(name='hi_user'); u = User.objects.first(); u.groups.add(g)`
* log in and start using the app!

