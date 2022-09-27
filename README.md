<h3 align="center">Statistic service</h3>

<!-- TABLE OF CONTENTS -->
<details open="open">

<summary>Table of Contents</summary>
    <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#methods-description">Methods description</a></li>
    </ol>
</details>

<!-- ABOUT THE PROJECT -->

##  About The Project
This is a microservice for statistics counters. The service can interact with the client using the REST API.

<!-- GETTING STARTED -->
## Installation

1. Clone the repo:
   ```sh
   git clone git@github.com:shell-escape/statistics_service.git
   ```
2. run docker-compose:
   ```sh
   docker-compose up --build
   ```
3. The service is running on port 8001, you can check it in the browser:
   ```sh
   http://localhost:8001/docs
   ```
   
<!-- METHODS DESCRIPTION -->

## Methods description

There are three methods:
 
1. **save_stat** - Method for saving statistic.

    Accepts input:

    - date - event date in 'YYYY-MM-DD' format
    - views - number of views
    - clicks - number of clicks
    - cost - the cost of clicks (in rubles, accurate to kopecks)

    The views, clicks and cost fields are optional. Statistics are aggregated by date.

2. **get_stat** - statistic display method.

    Accepts input:

    - from - period start date in 'YYYY-MM-DD' format (inclusive)
    - to - period end date in 'YYYY-MM-DD' format (inclusive)

    Responds with statistic sorted by date. The response contains the following fields:

    - date - event date
    - views - number of views
    - clicks - number of clicks
    - cost - cost of clicks
    - cpc = cost/clicks (average cost per click)
    - cpm = cost/views * 1000 (average cost per 1000 views)


3. **delete_stat** - method for resetting statistic.

    Deletes the statistic.

