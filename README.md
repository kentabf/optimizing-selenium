### Background
As part of my work as an economics research assistant, I had to build a web scraper to to make a over 19,000 queries on a webpage. However, I couldn't easily resort to Python's Scrapy library as the data of interest is dynamically generated with JavaScript. To keep things simple, I used the testing framework Selenium to scrape with a webdriver (PhantomJS).

However, each query takes from 4 to 10 seconds. Most of this query time came from the I/O with the webdriver. To speed up the whole process, I implemented as a multithreaded scraper with Python's threading library – so that multiple webdrivers can make separate queries simultaneously. (I may have to be more careful with the use of the word "simultaneously", as this program still shares one core).

Given this, I wanted to see what the optimum threadcount will be to optimize the scraping time. While having more threads would initially be more beneficial, eventually the overhead costs will rise high enough to the point that it brings down performance efficiency. Given the relevant performance measure, I expect this to be a concave function with respect to threadcount - the purpose being to find the maximum point.

### Setup
There were a total of 19,642 search terms (i.e., queries to make). The search terms were randomly shuffled, and then evenly split into 9 groups, where each group was assigned a threadcount number: 1, 3, 5, ..., 17. The Selenium webscraper was run on each of these groups with the assigned threadcount number. Each group contained about 2,180 search terms.

For control, when running the scraper, I: - Limited my activity on my computer to very lightweight internet browsing and PDF viewing (studying for classes)
- Only used the university's internet connection

Each query/scrape involved the following: - Recording the time
- Inserting the first name, last name, and clicking "search"
- Saving the resulting html page source with BeautifulSoup in a Python dictionary object
- Recording the time to get the scrape-time

The webscraper was built to recursively handle multiple results pages, but every single query results were contained in one result page. 






