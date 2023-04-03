import torch
import time
import random
import PIL
from torch import autocast
from diffusers import StableDiffusionImg2ImgPipeline

#model_id = "stabilityai/stable-diffusion-2-base"
model_id = "stabilityai/stable-diffusion-2-1"
#model_id = "runwayml/stable-diffusion-v1-5"

guidance_scale = 7.5

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)#.to("cuda")#"runwayml/stable-diffusion-v1-5")
#"runwayml/stable-diffusion-v1-5")#, torch_dtype=torch.float16)
#        "CompVis/stable-diffusion-v1-4")#, 
#        revision="fp16", torch_dtype=torch.float16)

#pipe.to("cuda")

#pipe.enable_attention_slicing()
pipe.enable_sequential_cpu_offload()
#pipe.enable_attention_slicing(1)
#pipe.enable_xformers_memory_efficient_attention()

def i2i(source_image_prefix, prompt, negative_prompt, description = None, count = 1, steps = 50, seed = None):
    filename = source_image_prefix + ".png"
    with PIL.Image.open(filename) as source_image:
        if (seed is None):
            seed = random.randint(0, 10000)
        generator = [torch.Generator(device="cuda").manual_seed(seed)]
        for i in range(count):
            output = pipe(prompt,
                          negative_prompt = negative_prompt,
                          generator = generator,
                          num_inference_steps = steps,
                          image=source_image,
                          guidance_scale = guidance_scale)
            for image in output.images:
                if description is None:
                    description = prompt.replace(" ", "_").replace(",", "")
                file = str(seed) + "_" + description + "_" + str(int(time.time()))
                image.save(f"{file}.png")
            seed += 1
