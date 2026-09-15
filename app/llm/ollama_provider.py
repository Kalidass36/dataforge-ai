import requests

from app.llm.provider import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model="llama3.2:3b",
        base_url="http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str) -> str:

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=120,
            )

            if response.status_code != 200:
                raise RuntimeError(
                    "Ollama request failed.\n"
                    f"Status: {response.status_code}\n"
                    f"Response: {response.text}"
                )

            data = response.json()

            if "response" not in data:
                raise RuntimeError(
                    "Ollama response did not contain "
                    "'response'.\n"
                    f"Response: {data}"
                )

            resp = data["response"]

            # Ollama may return a string or a structured object. If it's a string,
            # strip whitespace; otherwise return the object as-is so callers
            # can handle dict/list results.
            if isinstance(resp, str):
                return resp.strip()
            return resp

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Could not connect to Ollama.\n"
                "Make sure Ollama is running."
            )

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "Ollama request timed out."
            )