import requests

class NewsClient:
    def __init__(self):
        self.session = requests.Session()
        self.service_url = None
        self.is_logged_in = False

    def login(self, url):
        self.service_url = url
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = self.session.post(f"{url}/api/login/", data={'username': username, 'password': password})
        if response.status_code == 200:
            print("Login successful.")
            self.is_logged_in = True
        else:
            print("Login unsuccessful.", response.text)

    def logout(self):
        if self.service_url:
            response = self.session.post(f"{self.service_url}/news_api/logout/")
            if response.status_code == 200:
                print("Logout successful.")
                self.is_logged_in = False
            else:
                print("Logout unsuccessful.", response.text)
        else:
            print("You are not logged in.")

    def post(self):
        if not self.service_url:
            print("Please login first.")
            return
        
        headline = input("Enter story headline: ")
        category = input("Enter story category: ")
        region = input("Enter story region: ")
        details = input("Enter story details: ")

        story_data = {
            "headline": headline,
            "category": category,
            "region": region,
            "details": details
        }

        response = self.session.post(f"{self.service_url}/news_api/stories/", json=story_data)

        if response.status_code == 201:
            print("Story posted successfully.")
        else:
            print(f"Failed to post story. Status Code: {response.status_code}, Detail: {response.text}")

    def get_stories(self):
        if not self.service_url:
            print("Please login first.")
            return
        # Query string
        params = {
            'story_cat': input("Enter story category (* for any): "),
            'story_region': input("Enter story region (* for any): "),
            'story_date': input("Enter story date (* for any, format dd/mm/yyyy): ")
        }
        
        response = self.session.get(f"{self.service_url}/news_api/stories/", params=params)
        
        if response.status_code == 200:
            stories = response.json().get('stories', [])
            print(f"Found {len(stories)} stories.")
            for story in stories:
                print(f"{story['headline']} - {story['story_date']}")
        elif response.status_code == 404:
            print("No stories found.")
        else:
            print(f"Failed to fetch stories. Status: {response.status_code}")

    def list_services(self):
        if self.is_logged_in:
            print("\nAvailable services:")
            print("1. post")
            print("2. news")
            print("3. delete <story_key>")
            print("4. logout")
        else:
            print("\nAvailable services:")
            print("1. login <url>")

    def delete_story(self, story_key):
        if not self.service_url:
            print("Please login first.")
            return

        # Send DELETE request
        response = self.session.delete(f"{self.service_url}/news_api/stories/{story_key}/")

        if response.status_code == 200:
            print("Story deleted successfully.")
        elif response.status_code == 404:
            print("Story not found or not authorized to delete.")
        else:
            print(f"Failed to delete story. Status: {response.status_code}, Detail: {response.text}")

    def register(self):
        agency_name = "Tamar ORourke News Agency"
        url = "sc21tor.pythonanywhere.com"
        agency_code = "TRO00"

        payload = {
            'agency_name': agency_name,
            'url': url,
            'agency_code': agency_code,
        }

        directory_url = "https://directory.pythonanywhere.com/api/directory/"

        response = requests.post(directory_url, json=payload)

        if response.status_code == 200:
            print("Successful registration.")
        else:
            print(f"Unsuccessful registration. Status code: {response.status_code}, Response: {response.text}")
        
def main():
    client = NewsClient()
    #client.register()

    while True:

        if client.is_logged_in:
            command_input = input("Command: ").lower()
            if command_input == 'post':
                client.post()
            elif command_input == 'news':
                client.get_stories()
            elif command_input == 'list':
                client.list_services()
            elif command_input.startswith('delete '):
                story_key = command_input.split()[1]
                client.delete_story(story_key)
            elif command_input == 'logout':
                client.logout()
            elif command_input == 'quit':
                break
            else:
                print("Unknown command.")
        else:
            command_input = input("Command: ").lower()
            if 'login' in command_input:
                _, url = command_input.split(maxsplit=1)
                client.login(url)
            elif command_input == 'list':
                client.list_services()
            elif command_input == 'quit':
                break
            else:
                print("Unknown command.")

if __name__ == "__main__":
    main()