from __future__ import annotations

import base64
import os
from io import BytesIO
from pathlib import Path

import bentoml
from llama_index.core.multi_modal_llms import MultiModalLLM
from llama_index.core.multi_modal_llms.generic_utils import ImageDocument
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from PIL import Image

BASIC_PROMPT = """\
Please analyze this image comprehensively and provide the following information:

1. General Overview:
    - Main subject matter and content
    - Overall composition and context
    - Key visual elements present

2. Text Content:
    - Transcribe any visible text accurately
    - Include headers, labels, and captions
    - Note any important text formatting or emphasis

3. Data Visualization (if present):
    - For tables:
        * Convert to markdown format
        * Preserve column headers and data relationships
    - For charts/graphs:
        * Describe the type of visualization
        * Explain key trends and patterns
        * List important data points and values
    - For diagrams/flowcharts:
        * Explain the structure and relationships
        * Describe the flow or process
        * Note any important symbols or annotations

4. Additional Details:
    - Identify any branding or logos
    - Note color schemes if significant
    - Describe any relevant metadata or context

Please format the response clearly and maintain the original structure of any data.
"""


class SimpleImageParser:
    def __init__(self, model: MultiModalLLM):
        self.model = model

    """A simple parser for extracting information from images using VLMs.

    Args:
        model (MultiModalLLM): The multi-modal language model to use for parsing
    """

    def process_image(self, image_path: Path) -> str:
        """Convert image to base64 encoding"""
        image = Image.open(image_path)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    async def parse(self, image_path: Path) -> str:
        """Parse image content"""
        image_data = self.process_image(image_path)
        image_doc = ImageDocument(image_url=f"data:image/jpeg;base64,{image_data}")
        response = await self.model.acomplete(
            prompt=BASIC_PROMPT, image_documents=[image_doc]
        )
        return str(response)


@bentoml.service
class VLMService:
    @bentoml.api
    async def parse_image(
        self, image_path: Path, max_tokens: int = 512, temperature: float = 0.7
    ) -> str:
        """Parse image content"""
        model = OpenAIMultiModal(
            model=os.getenv("MULTI_MODAL_LLM_MODEL", "gpt-4o-mini"),
            api_key=os.getenv("OPENAI_API_KEY"),
            api_base=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            max_new_tokens=max_tokens,
            temperature=temperature,
            verbose=bool(os.getenv("BENTOML_DEBUG")),
        )
        parser = SimpleImageParser(model)
        return await parser.parse(image_path)
