A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.

Design:

Since my project is a web program, the best way to showcase it was through HTML and CSS. However, in order to add rather complicated features like the logging of water and the water calculator, I thought using the Flask application along with Python was the best way to showcase these features of my web app.

Before getting to my water features, I do need to discuss that the log in and log out feature for my database used another language, SQL, to store user names and hash passwords (with inspiration from CS50 finance). Via the SQL database, different users are able to log into my webiste and have their own information stored on the website without having to worry about others accessing their information. Combined with flask and jinja, users are able to log in and out at will.

Now, for the water log feature, in order to be able to store the log of each specific user, I thought that using a SQL database to store information fo reach user was the best approach. That way, a user is able to store how much water they've drunk and being able to acitively see that storage. All of the table viewing was used by grabbing the information from SQL and showcasing it on the website via the Jinja for loop.

Now, for the water calculator, I was able to implement the calculator via Flask with inspiration from a repo my TF provided for me. All of this was done with Python and the running of the actual equation I derived. All that was needed was input from the user which I got from HTML, but ultimately from Flask as it calculated the recommended water intake based on the user's phisiology.

Finally, to link a website providing information on why you should drink more water, I used the HTML tag "<a>" to link that website on that specific section.

With all these features, I implemented the Bootstrap CSS in order to organize everything and make it visually appealing. Combining everything here allowed me to successfully implement my web application. Speaking outloud, it's honestly amazing how all of these features combined allowed me to do this. How exciting.