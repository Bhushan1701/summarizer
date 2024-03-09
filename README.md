Steps to run the code:
  1. Change the directory to the 'summarizer_app_project'. Use the command 'cd .\summarizer_app_project\'.
  2. Run the code using the comnand : 'python manage.py runserver'
  3. Once the server is up and running you can hit the post request to the '/summarizer_app/post_function/' route. The URL will look like this: "8000/summarizer_app/post_function/", if its running on local port 8000.
  4. Now send URL to summarize the page in the post request in form of a json with 'url' key and value of url as value.
  5. You will the summary in form of a json with url and summary.
