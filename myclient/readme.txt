News Aggregator Service (readme.txt)

- To run the client application: 'python client.py'

Commands (if user is not authenticated):

- To login : 'login <url>' (url = https://sc21tor.pythonanywhere.com)
    * Username = tamarorourke
    * Password = Bullseye123
- To quit application : 'quit'

Commands (if user is authenticated):

- To logout : 'logout'
- To post a news story : 'post'
    * Enter story headline
    * Enter story category (pol, art, tech, or trivia)
    * Enter story region (uk, eu, or w)
    * Enter story details
- To list all news services : 'list'
- To request news stories : 'news -id=<id> -cat=<category> -reg=<region> -date=<date>'
    * <id> to be replaced with Agency Code from 'list' (e.g., "TRO00")
    * <category> to be replaced with "*" to display all categories or a specific category (e.g., "tech")
    * <region> to be replaced with "*" to display all regions or a specific region (e.g., "UK")
    * <date> to be replaced with "*" to display all dates or a specific date of the format "dd/mm/yyyy" (e.g., "22/03/2024")
- To delete a news story : delete <story_key>
    * <story_key> to be replaced with "id" attribute of respective story in database