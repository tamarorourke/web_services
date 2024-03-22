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
            response = self.session.post(f"{self.service_url}/api/logout/")
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

        response = self.session.post(f"{self.service_url}/api/stories/", json=story_data)

        if response.status_code == 201:
            print("Story posted successfully.")
        else:
            print(f"Failed to post story. Status Code: {response.status_code}, Detail: {response.text}")

    def stories_table(self, stories):
        print(f"{'Headline':<30} {'Category':<15} {'Region':<15} {'Author':<20} {'Date':<15} {'Details':<40}")
        print("-" * 135)

        for story in stories:
            print(f"{story['headline']:<30} {story['story_cat']:<15} {story['story_region']:<15} {story['author']:<20} {story['story_date']:<15} {story['story_details']:<40}")

    def get_stories(self, id=None, cat='*', reg='*', date='*'):
        if not id:
            print("Agency code is required.")
            return

        agencies = self.get_agencies()
        agency_info = agencies.get(id.upper())

        if not agency_info:
            print(f"No agency info found for agency code {id}.")
            return

        agency_url = agency_info.get('url')

        stories_url = f"{agency_url}/api/stories"
        params = {'story_cat': cat, 'story_region': reg, 'story_date': date}
        params = {k: v for k, v in params.items() if v != '*'}

        print(f"Fetching stories from: {stories_url} with params: {params}")

        response = self.session.get(stories_url, params=params)

        if response.status_code == 200:
            response_data = response.json()
            stories = response_data.get('stories', [])
            if stories:
                self.stories_table(stories)
            else:
                print("No stories found.")
        else:
            print(f"Failed to fetch stories. Status: {response.status_code}")

    def list_agencies(self):
        directory_url = "https://newssites.pythonanywhere.com/api/directory/"
        response = self.session.get(directory_url)

        if response.status_code == 200:
            agencies_data = response.json()
            agencies = {agency['agency_code'].upper(): agency for agency in agencies_data}

            print(f"{'Agency Name':<30} {'URL':<50} {'Agency Code':<15}")
            print("-" * 95)
            for agency in agencies_data:
                print(f"{agency['agency_name']:<30} {agency['url']:<50} {agency['agency_code']:<15}")
            return agencies
        else:
            print(f"Error fetching agency list. Status: {response.status_code}")
            return {}

    def get_agencies(self):
        directory_url = "https://newssites.pythonanywhere.com/api/directory/"
        response = self.session.get(directory_url)

        if response.status_code == 200:
            agencies_data = response.json()
            agencies = {agency['agency_code'].upper(): agency for agency in agencies_data}
            return agencies
        else:
            return {}

    def delete_story(self, story_key):
        if not self.service_url:
            print("Please login first.")
            return
            
        response = self.session.delete(f"{self.service_url}/api/stories/{story_key}/")

        if response.status_code == 200:
            print("Story deleted successfully.")
        elif response.status_code == 404:
            print("Story not found or not authorised to delete.")
        else:
            print(f"Failed to delete story. Status: {response.status_code}, Detail: {response.text}")
        
def main():
    client = NewsClient()

    while True:
        command_input = input("Command: ").strip().lower()
        command_parts = command_input.split()
        command = command_parts[0]

        if client.is_logged_in:
            if command_input == 'post':
                client.post()
            elif command == 'news':
                filters = {}
                for part in command_parts[1:]:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        key = key.lstrip('-')
                        filters[key] = value.strip('"')
                client.get_stories(**filters) 
            elif command_input == 'list':
                client.list_agencies()
            elif command_input.startswith('delete '):
                story_key = command_parts[1]
                client.delete_story(story_key)
            elif command_input == 'logout':
                client.logout()
            elif command_input == 'quit':
                break
            else:
                print("Unknown command.")
        else:
            if 'login' in command:
                _, url = command_input.split(maxsplit=1)
                client.login(url)
            elif command_input == 'quit':
                break
            else:
                print("Unknown command.")

if __name__ == "__main__":
    main()