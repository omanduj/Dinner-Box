Dinner Box
=======

What you'll see
-----------
This project creates a website that allows users to find and monitor their favorite local restaurants. Once
users sign up or login into the service, they are able to search for restaurants that fit their desires as well as 
add notes, pick from personal collections and other functionalities. The dashboard is used to display user options for different
services. 

There is also functionality to issue API calls to the service in personal applications. To use tokens navigate to the correct
webpage and request a token. Once token is recieved follow the directions on its usage. You can also find instructions below:

How to use token service:
Issue requests to the following endpoint: 

>http://127.0.0.1:8000/auth/

Define the headers as follows: 

>-H "Authorization:{Bearer:my_token}"

Then define the information you are passing in in the following format: 

>--data "cost=$&rating=2"

The final request should appear similar to:

>http://127.0.0.1:8000/auth/ -H "Authorization:{Bearer:my_token}" --data "cost=$&rating=2"

Add curl at start if using as a CLI
You will have 90 minutes before the token you have obtained expires, but you can reapply for more!

How to Run
-----------

In order to properly run this project you must first install Poetry, a tool used for dependency management and
packaging in Python. A link to the installation documents can be found here:
>https://python-poetry.org/docs/

Following installation run the command "poetry install", this will install all the project's dependencies.

In order to run the application, you must execute the following command in the appropriate directory
(food_proj/food_app):
>python manage.py runserver

 This will cause the program to run locally on port 8000. The webpage is located in the following url:
>http://127.0.0.1:8000/home/
![Screen Shot 2022-01-13 at 10 53 11 PM](https://user-images.githubusercontent.com/44513190/149453204-5553e0f8-842d-44c9-b372-a555bbd60b97.png)

Once user has logged in or signed up, they will be directed to the following url:
>http://127.0.0.1:8000/user/dashboard/
![MainMenu](https://user-images.githubusercontent.com/44513190/149452705-844eca16-62c1-4450-b209-0ef7fbdb539a.png)

This will display user information and options user has available to them.

The following url is used to add a restaurants' note to a users account:
>http://127.0.0.1:8000/user/create-notes/
![Screen Shot 2022-01-13 at 10 28 04 PM](https://user-images.githubusercontent.com/44513190/149452869-4e1ea2d7-4832-420d-8dc4-c83cb46d09bb.png)

The following url is used to randomly select a local restaurant to eat at that fits user criteria:
>http://127.0.0.1:8000/user/foodpicker/

The following url is used to randomly select a restaurant to eat at that fits user criteria from their personal collection:
>http://127.0.0.1:8000/user/personal_picks/

The following url is used to view all notes registered to a users account:
>http://127.0.0.1:8000/user/view-notes

The following url is used to issue tokens for users who wish to use the random selector of local restaurants functionality:
>http://127.0.0.1:8000/token/
>![token](https://user-images.githubusercontent.com/44513190/149452930-b8b628de-25d7-4cfc-8ab5-626a1a7b6f7f.png)
