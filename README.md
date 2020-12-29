Ginger Test project
===================

This is a test project required by ginger.io. The idea of the project is to collect
and show the information from arxiv.org.

The idea is to show at least 6 months of data from arxiv.org and allow the user to see some important information. 
For this project, I decided to use Django on the backend and HTML pages with bootstrap to show the information to the user.
To fetch the data from arxiv the project come with a management command that allow select how much information, 
is necessary to be fetched.


Functionalities:
----------------

- Management command  arxiv_data, used to call the APi from Arxiv and fetch the articles and authors. 
- List and details for authors
- List and details for articles
- User Login
- User Registration
- Start favorite authors and articles


Fetching de data
----------------
 
The command arxiv_data must be used to fetch the data if 6 months of data is not available, you can change 
the parameters to fetch data for a larger period is required. Additionally to this, the command could be used 
with the limit of days to 1 with a cronjob or a celery task to keep the database updated with the last elements
from Arxiv.

Parameters:
    - **items_page**: allow limit how many items can be fetched by request, limit from Arxiv 30000 
    - **limit_days**: allow limit the number of days to be fetched, the default is 6 months. 

Meta
----

Author:
    Mariano Ramirez
