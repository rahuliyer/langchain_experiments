import os
import json
import requests

from notion import NotionClient
from api_key_loader import load_api_keys

load_api_keys()

NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + NOTION_API_KEY
}

notion = NotionClient(auth=NOTION_API_KEY)

def find_root_object():
        res = notion.search()
        for node in res.results:
               if node.parent.type == "workspace" and \
                        node.parent.workspace == True:
                return {
                        "type": node.object,
                        "id": node.id,
        }

def create_page(parent_type, parent_id, title):
        parent = {
               "page_id": parent_id
        }

        new_page = {
                "title": [
                {
                        "text": {
                        "content": title
                        }
                }]
        }

        res = notion.pages.create(parent=parent, properties=new_page)

        return {
                "id": res["id"],
                "url": res["url"]
        }

def add_text_to_page(page_id, text):        
        new_text = [
                {
                        "type": "paragraph",
                        "text": {
                                "content": "This is the first line of the new text."
                        }
                }
        ]

        data = {
                "properties": {
                        "Text": {
                                "rich_text": text
                        }
                }
        }

        res = requests.patch(BASE_URL + "/pages/" + page_id, headers= HEADERS, data=json.dumps(data))
        print(f"status code: {res.status_code}, error: {res.text}")

if __name__ == "__main__":
        res = find_root_object()
        print(res)
#        res = create_page(res["type"], res["id"], "bobo1")
#        print(json.dumps(res, indent=4))
#        page_id = res["id"]
#        res = add_text_to_page(page_id, "hello, world!")
#        res = add_text_to_page(page_id, "hello, world2!")