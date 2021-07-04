## The Alpha Team

### Communication policy
- Discord for communication
- Request for code review in #code-review channel

### Code Style Guide:
- lower cammel case naming convention
- private vars have single underscore (_)
- indent with tabs
- Curly braces start on same line
- Classes start with uppercase (both file and class name)
- If variable name is not obvious, have comment on declaration with full name (ex. ct for current time)
- Function names must have comment docs if not self obvious

### Merging
- Make your own branch for every new feature
- Merge back into master
- 1 person code review before the merge
- The reviewer only comments on the code and decide to send it back, not change it

### Software version
- Django 3.0.3 - djangoproject.com
- Python 3.8.1 - python.org
- Bootstrap 4.4 - getbootstrap.com
- Pycharm - jetbrains.com/pycharm
- jQuery - 3.2.1
- Pillow 7.0.0
- webpush 0.3.2

### Build Instructions
Make sure that you have python installed on the server.
To install django run pip install Django==3.0.3
To install Pillow run pip install Pillow=7.0.0
To install webpush run pip install django-webpush
Run the following commands in order to set up the database and run the server:
 alphaAuction/manage.py makemigrations
 alphaAuction/manage.py migrate
 alphaAuction/manage.py migrate --run-syncdb
 alphaAuction/manage.py runserver
The server is now up on your local host
You can visit the main page by going to localhost:8000/auction/
In order to create auctions, add items, and add images you will need an admin account.
Create an admin account by running alphaAuction/manage.py createsuperuser and fill out the queries
Visit the admin page at localhost:8000/admin and log in in order to create the auction and items


### Extra notes
Make sure that anyone use a private or incognito tab is aware that they cannot get notifications with that type of tab.
Notifications will also not work if the people are connecting to an ip address rather than localhost or an https page.
    For example connecting to 144.39.... will not give them notifications.

### Unit testing instructions
If you want to run the tests and generate a test database run RunTests.py.
    -Please note that running RunTests.py will DELETE your existing database, so only run this if you don't
    need the current information
    -The test database generated from RunTests.py will give you a few users, auctions, and items to play around with.
    -After running alphaAuction/manage.py runserver, navigate to localhost:8000/auction/ and use test1 as the passphrase.
    -You should arrive at a test auction with over 10 item. In order to bid on these items you will need to log in, do so
    with the account bidder1.1@test.com as the email/username and testing as the password. Other bidders can be accessed at
    bidder1.2@test.com and bidder1.3@test.com with the same password of testing.
    -If you need to access an admin account, there is an admin account with a username and password of admin.
Otherwise to just run the tests, run alphaAuction/manage.py test auction.


### System Testing Instructions


### Understanding the prototype
- Our prototypes are in /docs/AuctionHFPrototype.ppt
- Slide 1 is the default view of items, control clicking on them will bring you to the prototype of our item view page
- On slide 1 you can control click on View to see our drop down menu of view types
- On slide 2 control clicking either grid view small or list view will bring you to a prototype of either page
- Control clicking items on any page should bring you to the prototype of our item view page
- Slide 8 is the prototype of our login screen

