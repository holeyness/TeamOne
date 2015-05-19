# comp120-spring2015-team1
Final Project: Real Time Voting
For our final project, we decided to implement a content voting system that likes must be continuously received in order to keep the post alive. Each new post is give a 30 second life that can be extended with new likes, and the clock is synchronized across all the clients and the server.

Tehcnical details: new posts are added asynchronously through the pusher api which is a form of a websocket. The new post is pushed to all the clients and the timer starts when the clients receive the update. When a like is generated via a POST request to the server, the server relays all that information to all the clients which on the client side, adds a like and resets the clock. If the clock ever hits 0, the client deletes the object from the DOM. The server only outputs posts that are "alive", so future clients won't see dead posts either.

Pros:
- Real time voting
- Content is moderated in real time
- Posts are sorted based on popularity and freshness

Cons:
- We are using someone else's API, which is paid
- The post is just deleted from the DOM, a more graceful method may be useful

Future improvements:
- Improved algorithm for sorting ranking by likes and time
- Filter feeds into communities with tags or subreddit like structures
- Scalability that extends past the pusher API

Detailed presentation notes can be found here: https://docs.google.com/document/d/1Sqo1eutBy10Rawuv3N6yk1XitopsOMHEJoS5J9VQPgo/edit?usp=sharing


Leg 6: Polling
Polling was implemented on our server using pusher.com. Instead of hosting our own websocket, the third-party API handles that for us which enables us to test the funcitonality without setting things up on a server (like AWS).

Technical details: everytime a new post is created (in views.py), the server uses a library (pusher) that sends the serialized json data to the api of pusher.com. This is done through json, and various details can be formatted using json.

The pusher.com then pushes the information in a json package to any listening clients (which could just be another tab on the same browser). The client then creates a new div of a post and fill it with the appropriate information from the json message and updates the HTML DOM with the new post.

Here's the service we are using: https://pusher.com/

Notes for this service: You can create channels to handle multiple calls for different events. The client can also subscribe to different channels if needed

Pros: 
- Simple to implement (doesn't need to set up additional service)
- Simple to code (the code for the server-side was one line)
- Easy to maintain (since they handle the server that synchronizes everything, each half of the transaction can be dealt with independently)
- Good documentation (if needed)
- Secure

Cons: 
- Paid (although the free plan is more than generous enough, but only max 20 connections at at ime)
- External server has all the messages you pass around (although they do offer encrypted SSL)

Leg 5: API
Added User_Posts model which holds two foreign key that relates posts with users.
All references of posts are replaced with user_posts and the user who owns the data is displayed.
All aspects of upload/newsfeed/single post is working.
API is documented at the footer of the site, and located here: https://docs.google.com/a/ianluo.com/document/d/1dsGt3VH-6be7_TKpXuN1nf1MoPpBoYiMpcnGwDTTl4k/edit


Leg 4: Optimization

OPTIMIZATION TECHNIQUES

We optimized our application by doing the following:
	-Using a distributed memory caching system (Reddis)
	-Using an HTML5 application cache
	-Using a CDN (AWS' CloudFront)
	-JavaScript and CSS minifcation
	-Combining CSS and JavaScript files
	-Placing JavaScript at the bottom of pages

Note: At this time, the CDN is still being implemented, and caching is being debugged.

TESTING TOOLS

For this leg, we tested our application using Y-Slow, PageInsights, and Google Audits


PERFORMANCE ASPECTS

Pre-Optimization
	
	Y-Slow
		OVERALL GRADE: B (84/100)
		Grades/Notes for Improvement Areas:
		A - Make Fewer HTTP Requests
				-Use 4 stylesheets, try combining into 1
		B - Make favicon small and cacheable
		C - Use cookie-free domains
		D - Compress components with gzip
		F - Use a CDN
		  - Add Expires headers

		Empty Cache: 11 HTTP requests, 7823.4k total weight

	PageInsights Notes:
		-Optimize the order of stylesheets and scripts
		-Serve scaled images
		-Optimize images
		-Enable compression
		-Minify HTML, CSS, JavaScript
		-Specify image dimensions
		-Set an expiry date
		-Defer parsing JavaScript

	Google Audits Notes:
		-Minimize cookie size
		-Specify image dimensions
		-Optimize order of styles and scripts
		-Remove unused CSS rules
		-Use normal CSS property names instead of vendor-prefixed ones

Post-Optimization

	Y-Slow
		OVERALL GRADE: B (85/100)
		Grades/Notes for Improvement Areas:
		A - Use 3 stylesheets, try combining into 1
		B - Make favicon small and cacheable
		C  - Use cookie-free domains
		D - Compress components with gzip (compression still being implemented)
		F - Use a CDN (still being implemented)
		  - Add Expires headers
		
		Empty Cache: 9 HTTP requests, 7912.9k total weight

	PageInsights Notes:
		-Minify HTML
		-Specify image dimensions
		-Defer parsing JavaScript
		-Enable compression (still being implemented)

	Google Audits Notes:
		-Leverage browser caching (still being implemented)
		-Minimize cookie size
		-Specify image dimensions


Leg 1: Data Schema and Wireframe

Our data schema separates users, their followers, their posts, and the comments on that post. We use relational tables to connect a post to its user and its comments, as well as to connect users to their followers' posts. The schema utilizes a large number of tables and relational tables to ensure that it is simple and easy to grow as the application may change with time. The schema attempts to do nothing new - we follow the models exemplified in class and expect little trouble implementing it.

Our wireframes display the two core interfaces of our application. The first, the newsfeed, is comparable to the Facebook/Twitter/Instagram timeline so often see in social media. We use a newsfeed as the primary purpose of this application is to share content with others. Left and right buttons on the screen (or the left and right arrow keys) will be used to cycle through content and display its likes and comments. The second wireframe displays a user's profile for them to modify or upload their content. The profile page utilizes a similar design as the newsfeed. Though our designs are obviously subject to change, they are currently intentionally simple to avoid overwhelming users and to leave room for development should new features be necessary.

Leg 2: Implementing the Minimum Viable Product

The minimum viable product for our app consists of two views of the content. One view is the newsfeed, where right now all of the content will be shown. The other view shows a single peice of content. The content is comprised solely of posts. Each post will have a title, and description retrieved from our database, as well as a linked image file uploaded and hosted on the server. 

The home page will serve as the newsfeed. ~/
Any single post can be viewed through ~/post/(#of post)
A post is uploaded through ~/upload/

We are using django-bootstrap3, installed through pip install django-bootstrap3.

This gives us the ability to use bootstrap components and css classes in our mvp.

Aproximate # hours team spent learning python/django: 10
Aproximate # hours team spent implementing MVP : 6

Biggest challenge this leg: Figuring out how to do file uploads
in Django.







