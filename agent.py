from huggingface_hub import InferenceClient
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from io import BytesIO
import os


# =========================
# API KEYS
# =========================
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# =========================
# LLM
# =========================

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


# =========================
# IMAGE MODEL
# =========================

image_pipe = InferenceClient(
    provider="hf-inference",
    model="stabilityai/stable-diffusion-3-medium-diffusers",
    api_key=HF_TOKEN
)


# =========================
# IMAGE STORAGE
# =========================

image_store = {}


# =========================
# IMAGE GENERATION TOOL
# =========================

@tool
def generate_image(prompt: str) -> str:
    """
    Generate an image from a text prompt using Hugging Face.
    The generated image is kept in memory and is not saved to disk.
    """

    print("\n🎨 IMAGE GENERATION AGENT")
    print("Prompt:", prompt)

    image = image_pipe.text_to_image(prompt)

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    image_store["latest"] = buffer.getvalue()

    print("✅ Image generated successfully")

    return "IMAGE_GENERATED"


# =========================
# DISPLAY TOOL
# =========================

@tool
def display_image(image_path: str) -> str:
    """
    Prepare the generated image for display in the web interface.
    """

    print("\n🖼️ DISPLAY IMAGE AGENT")
    print("✅ Image ready for display")

    return "IMAGE_READY_FOR_DISPLAY"


# =========================
# TOOLS
# =========================

tools = [
    generate_image,
    display_image
]


# =========================
# AGENT
# =========================

agent = create_agent(
    model=llm,
    tools=tools
)
