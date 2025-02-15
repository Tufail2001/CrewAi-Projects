from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

class ExampleFlow(Flow):
    model = "gemini/gemini-1.5-pro"  # Using a more stable model
    
    @start()
    def generate_blog_title(self):
        try:
            response = completion(
                model='gemini/gemini-1.5-pro',
                api_key=API_KEY,
                messages=[{"role": "user", "content": "Generate a trending blog title"}]
            )
            title = response['choices'][0]['message']['content']
            return title
        except Exception as e:
            print(f"Error generating title: {str(e)}")
            return "Default Blog Title"

    @listen('generate_blog_title')
    def generate_blog(self, title):
        try:
            response = completion(
                model='gemini/gemini-1.5-pro',  # Using the same model for consistency
                api_key=API_KEY,
                messages=[{"role": "user", "content": f"generate a blog about {title}"}]
            )
            blog = response['choices'][0]['message']['content']
            print(f"Blog content: {blog}")
            return blog
        except Exception as e:
            print(f"Error generating blog: {str(e)}")
            return "Error generating blog content"

def kickoff():
    obj = ExampleFlow()
    result = obj.kickoff()
    print(result)
    return result

if __name__ == "__main__":
    kickoff() 