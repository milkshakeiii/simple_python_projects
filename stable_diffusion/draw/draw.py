import torch
import time
import random
from torch import autocast
from diffusers import StableDiffusionPipeline

#model_id = "stabilityai/stable-diffusion-2-base"
#model_id = "stabilityai/stable-diffusion-2-1"
model_id = "/home/milkshake/simple_python_projects/stable_diffusion/textual_inversion/some_garbage"
#model_id = "runwayml/stable-diffusion-v1-5"

# get your token at https://huggingface.co/settings/tokens
# token = "HF_TOKEN_PLACEHOLDER"
pipe = StableDiffusionPipeline.from_pretrained(model_id)#.to("cuda")#"runwayml/stable-diffusion-v1-5")
#"runwayml/stable-diffusion-v1-5")#, torch_dtype=torch.float16)
#        "CompVis/stable-diffusion-v1-4")#, 
#        revision="fp16", torch_dtype=torch.float16)

pipe.to("cuda")

#pipe.enable_attention_slicing()
#pipe.enable_sequential_cpu_offload()
#pipe.enable_attention_slicing(1)
#pipe.enable_xformers_memory_efficient_attention()

def draw(prompt, negative_prompt, description = None, count = 1, steps = 50, seed = None):
    if (seed is None):
        seed = random.randint(0, 10000)
    generator = [torch.Generator(device="cuda").manual_seed(seed)]
    for i in range(count):
        output = pipe(prompt,
                      negative_prompt = negative_prompt,
                      generator = generator,
                      num_inference_steps = steps)
        for image in output.images:
            if description is None:
                description = prompt.replace(" ", "_").replace(",", "")
            file = str(seed) + "_" + description + "_" + str(int(time.time()))
            image.save(f"{file}.png")
        seed += 1
