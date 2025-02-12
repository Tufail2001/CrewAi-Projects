from crewai.flow.flow import Flow, start, listen 
from litellm import completion

API_KEY="AIzaSyCG64YuzmdJjvFf7uuCpO1VvneQX6P7g5w"

class BlogAssignment(Flow):

    @start()
    def generat_random_topic(self):
        result = completion(
            model="gemini/gemini-1.5-flash",
            api_key=API_KEY,
            messages=[{"role": "user", "content": "Return a random trending blog topic 2025 ."}],
        )

        topic = result['choices'][0]['message']['content']
        print(f"Topic: {topic}")
        return topic
    

    @listen("generat_random_topic")
    def generate_outline(self, topic):
        result = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=API_KEY,
            messages=[{"role": "user", "content": f"Generate an outline for a blog on {topic}."}],
        )
        outline = result['choices'][0]['message']['content']
        print(f"Outline: {outline}")
        return outline
    

    @listen("generat_outline")
    def generate_blog(self, outline):
        result = completion(
            model="gemini/gemini-2.0-flash-exp",
            api_key=API_KEY,
            messages=[{"role": "user", "content": f"Write an interesting blog by using this outline  {outline}."}],
        )
        blog=result['choices'][0]['message']['content']
        print(f"Blog: {blog}")
        print(f"topic: {outline}")
        self.state['blog'] = blog
    
    
    @listen("generate_blog")
    def save_blog(self, blog):
        with open("out_come.md", "w") as file:
            file.write(self.state['blog'])
            return self.state['blog']



def kickoff():
    obj = BlogAssignment()
    result =obj.kickoff()
    print(result)

