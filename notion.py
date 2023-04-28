from langchain.tools import BaseTool

import json

class NotionQueryDatabaseTool(BaseTool):
    name = "notion_query_database"
    description = "Use this tool when you need to query for notion databases. The response will be a list of database ids encoded as json. If there are multiple elements, ask for which one to use"

    def _run(self, *kwargs) -> str:
        return json.dumps([{
            "db_id": "db_id_42"
        },
        {
            "db_id": "db_id_43"
        }])
    
    def _arun(self, *kwargs) -> str:
        raise NotImplementedError("NotionQueryDatabaseTool does not support async")

class NotionCreatePageTool(BaseTool):
    name = "notion_create_page"
    description = "Use this tool when you need to create a notion document or page. If a database id is not provided then first query for one. Then provide the input as json with the keys database_id for the notion database id and page_name for the page name."

    def _run(self, document_name, *kwargs) -> str:
        print(f"document name is {document_name}")

        try: 
            args = json.loads(document_name)
            if args["database_id"] != "db_id_42":
                return "Invalid database id"
            
            return json.dumps({
                "page_id": "page_id_42"
            })
        except Exception as e:
            return "Invalid input"
            
    def _arun(self, *kwargs) -> str:
        raise NotImplementedError("NotionCreatePageTool does not support async")

class NotionAddTextToPageTool(BaseTool):
    name = "notion_add_text_to_page"
    description = "Use this tool when you need to add text to a Notion page or document. Format the input as json with the key page_id for the page and text for the text"

    def _run(self, args, *kwargs) -> str:
        print(f"args are {args}")
    
    def _arun(self, *kwargs) -> str:
        raise NotImplementedError("NotionAddTextToPageTool does not support async")