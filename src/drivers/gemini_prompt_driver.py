import os
from dotenv import load_dotenv
import google.generativeai as genai
from griptape.drivers import BasePromptDriver
from griptape.artifacts import TextArtifact, ErrorArtifact
from typing import Generator, Optional
from griptape.tokenizers import BaseTokenizer

class DummyTokenizer(BaseTokenizer):
    def __init__(self, model: str):
        super().__init__(model=model)

    def tokenize(self, text: str) -> list:
        return list(text)

    def detokenize(self, tokens: list) -> str:
        return ''.join(tokens)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenize(text))

class GeminiResult:
    def __init__(self, text):
        self.text = text

    def to_artifact(self):
        return TextArtifact(self.text)

class GeminiPromptDriver(BasePromptDriver):
    def __init__(self, model="gemini-1.5-pro-exp-0801", temperature=1, top_p=0.95, top_k=64, max_output_tokens=8192):
        load_dotenv()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        
        self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
        }
        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(history=[])
        
        super().__init__(model=model, tokenizer=DummyTokenizer(model=model))

    def _extract_prompt_from_stack(self, prompt_stack):
        messages = []
        for message in prompt_stack.messages:
            if message.role == "system":
                messages.append({"role": "system", "content": message.content[0].artifact.value})
            elif message.role == "user":
                messages.append({"role": "user", "content": message.content[0].artifact.value})
        return messages

    def try_run(self, prompt) -> Optional[GeminiResult]:
        try:
            if hasattr(prompt, 'messages'):  # Check if it's a PromptStack
                messages = self._extract_prompt_from_stack(prompt)
                response = self.chat_session.send_message(messages[-1]["content"])
            else:
                response = self.chat_session.send_message(prompt)
            
            return GeminiResult(response.text)
        except Exception as e:
            print(f"Error in GeminiPromptDriver.try_run: {e}")
            return GeminiResult(str(e))

    def try_stream(self, prompt) -> Generator[GeminiResult, None, None]:
        try:
            if hasattr(prompt, 'messages'):  # Check if it's a PromptStack
                messages = self._extract_prompt_from_stack(prompt)
                response = self.chat_session.send_message(messages[-1]["content"], stream=True)
            else:
                response = self.chat_session.send_message(prompt, stream=True)
            
            for chunk in response:
                yield GeminiResult(chunk.text)
        except Exception as e:
            print(f"Error in GeminiPromptDriver.try_stream: {e}")
            yield GeminiResult(str(e))

    def run(self, prompt) -> GeminiResult:
        result = self.try_run(prompt)
        if result is not None:
            return result
        else:
            raise Exception("Failed to generate response")