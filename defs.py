# libraries
import webuiapi
from PIL import Image
import datetime


## setting def
def pre_setting(input_img):
    # setting controlnet & adetailer
    ads = webuiapi.ADetailer(ad_model="face_yolov8n.pt",
                             ad_prompt="attractive, looking at the viewers, cute, animation style")

    unit1 = webuiapi.ControlNetUnit(input_image=input_img,
                                    model='control_v11f1e_sd15_tile [a371b31b]',
                                    pixel_perfect="True")

    unit2 = webuiapi.ControlNetUnit(input_image=input_img,
                                    module='lineart_standard',
                                    model='control_v11p_sd15_lineart [43d4be0d]',
                                    pixel_perfect="True")
    print("Pre setting is done ...!")
    return ads, unit1, unit2


## img2img def
def gen_animate_img(input_img, api, ads, unit1, unit2, w, h, prompt_selected):
    # img2img
    result2 = api.img2img(
                        images=[input_img],
                        prompt=prompt_selected,
                        negative_prompt="blurry, water marks, poor quality",
                        
                        cfg_scale=1.5,
                        denoising_strength=0.85,
                        
                        sampler_name='Euler a',
                        width=int(w),
                        height=int(h),
                        steps=20,

                        adetailer=[ads],
                        controlnet_units=[unit1, unit2]
                        )
    suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    result2.image.save(f"./history_output/generated_{suffix}.png")
    print("Generating animation image is done ...!")
    return result2.image