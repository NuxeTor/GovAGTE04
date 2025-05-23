import os
import requests
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def generate_education_agents_image():
    """Generate an image of education agents in a meeting for the PNAE program"""
    
    prompt = "Professional meeting of education professionals in a modern conference room. Diverse group of people in business attire sitting around a table with documents and laptops. Clean, well-lit government office setting with professional atmosphere. Realistic photography style."
    
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open('static/images/agentes_educacao_reuniao.jpg', 'wb') as f:
                f.write(image_response.content)
            print("Imagem criada com sucesso: static/images/agentes_educacao_reuniao.jpg")
            return True
        else:
            print("Erro ao baixar a imagem")
            return False
            
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")
        return False

if __name__ == "__main__":
    # Criar diretório se não existir
    os.makedirs('static/images', exist_ok=True)
    generate_education_agents_image()