import json
from duckduckgo_search import DDGS
from griptape.artifacts import TextArtifact
from griptape.structures import Pipeline
from griptape.tasks import CodeExecutionTask
from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunClient
import os

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

def search_duckduckgo(task: CodeExecutionTask) -> TextArtifact:
    keywords = task.input.value
    results = DDGS().text(keywords, max_results=config['search_tool']['max_results'])
    return TextArtifact(results)

def build_search_pipeline() -> Pipeline:
    pipeline = Pipeline()
    pipeline.add_task(
        CodeExecutionTask(
            "{{ args[0] }}",
            run_fn=search_duckduckgo,
        ),
    )
    return pipeline

def get_search_tool():
    search_driver = LocalStructureRunDriver(structure_factory_fn=build_search_pipeline)
    return StructureRunClient(
        name="SearchTool",
        description="Search the web for information",
        driver=search_driver,
        off_prompt=True,
    )