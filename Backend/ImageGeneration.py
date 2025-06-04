import asyncio
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep


base_dir = os.path.dirname(os.path.abspath(__file__))


env_path = os.path.join(base_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)


API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_TOKEN = os.getenv("HuggingFaceAPIKey")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Paths
data_folder = os.path.join(base_dir, "..", "Data")
file_path = os.path.join(base_dir, "..", "Frontend", "Files", "ImageGeneration.data")

# Ensure data folder exists
os.makedirs(data_folder, exist_ok=True)

def open_images(prompt):
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(data_folder, jpg_file)

        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                print(f"Opening image: {image_path}")
                img.show()
                sleep(1)
            except IOError:
                print(f"❌ Failed to open image: {image_path}")
        else:
            print(f"⚠️ Image does not exist: {image_path}")

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f" API Error {response.status_code}: {response.text}")
        return None
    return response.content

async def generate_image(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details"
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        image_path = os.path.join(data_folder, f"{prompt.replace(' ', '_')}{i+1}.jpg")
        if image_bytes and isinstance(image_bytes, bytes) and len(image_bytes) > 100:
            with open(image_path, "wb") as f:
                f.write(image_bytes)
        else:
            print(f" Skipping image {i+1} due to empty or invalid response.")

def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

# Main loop
while True:
    try:
        with open(file_path, "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.strip().split(",")

        if Status == "True":
            print("🧠 Generating Images...")
            GenerateImages(prompt=Prompt)

            # Reset the data file status
            with open(file_path, "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)

    except KeyboardInterrupt:
        print("🔴 Interrupted by user.")
        break

    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        sleep(1)
