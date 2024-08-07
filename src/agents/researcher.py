from griptape.structures import Agent
from griptape.rules import Rule
from griptape.config import StructureConfig
from src.drivers.gemini_prompt_driver import GeminiPromptDriver
from griptape.tools import WebScraper, TaskMemoryClient
from src.tools.search_tool import get_search_tool
import os
import json


def load_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json'))
    default_config = {
        "search_tool": {"max_results": 5},
        "gemini": {"api_key": "", "model": "gemini-pro"},
        "researcher": {
            "id": "explorer",
            "rules": [
                {"type": "Position", "value": "Chief Travel Explorer"},
                {"type": "Objective", "value": "Uncover the latest travel trends and destination insights."},
                {"type": "Background", "value": "You are a part of a leading travel consultancy. Your expertise lies in discovering new travel experiences and trends. You have a knack for turning data into compelling travel recommendations."}
            ],
            "task_prompt": "Conduct an in-depth analysis of current travel trends and emerging destinations for 2024. Highlight key trends, must-visit places, and their appeal to different types of travelers."
        },
        "writers": [
            {
                "role": "Cultural Travel Writer",
                "goal": "Reveal the rich cultural experiences of various destinations",
                "backstory": "Having explored numerous countries, you immerse readers in the traditions, festivals, and daily lives of the places you visit."
            },
            {
                "role": "Adventure Travel Enthusiast",
                "goal": "Guide thrill-seekers to the best adventure destinations",
                "backstory": "From mountain climbing to deep-sea diving, you share firsthand experiences and tips for adrenaline-filled adventures."
            }
        ],
        "writer_task_prompt": "Using the provided insights, craft a captivating blog post that explores the hottest travel trends and destinations of 2024. Your article should be engaging and easy to read, appealing to a broad audience of travel enthusiasts. Infuse it with excitement and avoid overly technical language.\n\nInsights:\n{{ parent_outputs['research'] }}",
        "end_task_prompt": "State: Adventure Awaits!"
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            loaded_config = json.load(f)
        # Update default_config with loaded values, ensuring all keys exist
        default_config.update(loaded_config)
    
    return default_config

config = load_config()





class ErrorHandlingAgent(Agent):
    def run(self, *args, **kwargs):
        try:
            return super().run(*args, **kwargs)
        except Exception as e:
            return str(e)

def build_researcher():
    """Builds a Researcher Structure."""
    researcher_config = config['researcher']

    researcher = ErrorHandlingAgent(
        config=StructureConfig(
            prompt_driver=GeminiPromptDriver(
                model=config['gemini']['model'],
                temperature=config['gemini'].get('temperature', 1),
                top_p=config['gemini'].get('top_p', 0.95),
                top_k=config['gemini'].get('top_k', 64),
                max_output_tokens=config['gemini'].get('max_output_tokens', 8192)
            ),
        ),
        id=researcher_config['id'],
        tools=[
            get_search_tool(),
            WebScraper(off_prompt=True),
            TaskMemoryClient(off_prompt=False),
        ],
        rules=[Rule(f"{rule['type']}: {rule['value']}") for rule in researcher_config['rules']],
    )

    return researcher