from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
           prompt = """
           You are an expert blog content writer. Use Markdown formatting.
           Task:
           Generate exactly ONE blog title for the topic: "{topic}"
           Rules:
           - The title must be creative and SEO-friendly
           - Do NOT provide multiple options
           - Do NOT include explanations, bullet points, or alternatives
           - Output only the single best title as a Markdown H1
           """
           sytem_message=prompt.format(topic=state["topic"])
           response=self.llm.invoke(sytem_message)
           return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        """
        translation_prompt = """
        Translate the following blog into {current_language}.

        Translate BOTH:
        - title (translated, markdown)
        - content (translated, markdown)

        Title:
        {blog_title}
        CONTENT:
        {blog_content}
        """

        blog_content=state["blog"]["content"]
        blog_title = state["blog"]["title"]
        messages=[
            HumanMessage(translation_prompt.format(current_language=state["current_language"],blog_title=blog_title, blog_content=blog_content))

        ]
        transaltion_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": {"title": transaltion_content.title,"content": transaltion_content.content}}
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french": 
            return "french"
        else:
            return state['current_language']