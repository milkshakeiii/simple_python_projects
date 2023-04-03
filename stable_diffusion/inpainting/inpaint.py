import PIL
import PIL.ImageDraw
import torch
import time
from io import BytesIO

from diffusers import StableDiffusionInpaintPipeline

guidance_scale = 7.5
steps = 50

pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting")
pipe.enable_sequential_cpu_offload()
pipe.enable_attention_slicing(1)

def inpaint(fileprefix, prompt, negative_prompt):
    filename = fileprefix + ".png"
    maskname = fileprefix + "_mask.png"
    with PIL.Image.open(filename) as image_file:
        with PIL.Image.open(maskname) as mask_file:
            init_image = image_file.convert("RGB")
            mask_image = mask_file.convert("RGB")
            width, height = init_image.size
            image = pipe(prompt=prompt, negative_prompt=negative_prompt, image=init_image, mask_image=mask_image, height=height, width=width, guidance_scale=guidance_scale, num_inference_steps=steps).images[0]
            image.save("inpaint_" + str(int(time.time())) + "_" + filename)

def outpaint(fileprefix, prompt, negative_prompt, pixels_right, pixels_down = 0, centering = (0, 0)):
    filename = fileprefix + ".png"
    with PIL.Image.open(filename) as image_file:
        init_image = image_file.convert("RGB")
        expanded_image = PIL.ImageOps.pad(init_image,
                                          (init_image.size[0]+pixels_right, init_image.size[1]+pixels_down),
                                          centering = centering,
                                          color = "#FFFFFF")
        mask_image = expanded_image.copy()
        draw = PIL.ImageDraw.Draw(mask_image)
        draw.rectangle(((0, 0), (init_image.size[0]-10, init_image.size[1])), fill="#000000")
        draw.rectangle(((init_image.size[0]-10, 0), init_image.size), fill="#FFFFFF")
        width, height = expanded_image.size
        expanded_image.save("test1.png")
        mask_image.save("test2.png")
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, image=expanded_image, mask_image=mask_image, height=height, width=width, guidance_scale=guidance_scale, num_inference_steps=steps).images[0]
        image.save("outpaint_" + str(int(time.time())) + "_" + filename)

