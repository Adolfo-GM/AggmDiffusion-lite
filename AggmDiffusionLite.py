# Adolfo GM
# 2024-12-16
# AggmDiffusion Lite
# =============================================================

import numpy as np
from PIL import Image
import random
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import threading

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else x
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

def perlin_noise(width, height, scale=100, roughness=1.0):
    p = [i for i in range(256)]
    random.shuffle(p)
    p = p * 2
    noise_image = np.zeros((height, width), dtype=np.float32)
    for y in range(height):
        for x in range(width):
            X = int(x / scale)
            Y = int(y / scale)
            xf = (x / scale) - X
            yf = (y / scale) - Y
            u = fade(xf)
            v = fade(yf)
            aa = p[p[X] + Y]
            ab = p[p[X] + Y + 1]
            ba = p[p[X + 1] + Y]
            bb = p[p[X + 1] + Y + 1]
            x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
            x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)
            noise_value = lerp(x1, x2, v)
            noise_value = noise_value * roughness
            noise_image[y, x] = noise_value
    return noise_image

def get_color_from_palette(value, palette):
    normalized_value = (value + 1) * 0.5
    idx = int(normalized_value * (len(palette) - 1))
    return palette[idx]

def generate_colored_perlin_noise(width, height, scale=100, prompt="calm"):
    color_palettes = {
        "cloudy": [(200, 200, 255), (170, 170, 230), (130, 130, 200), (100, 100, 180), (50, 50, 150)],
        "mountainous": [(150, 75, 0), (120, 60, 0), (200, 100, 0), (255, 215, 0), (139, 69, 19)],
        "forest": [(0, 50, 0), (34, 139, 34), (60, 179, 113), (85, 107, 47), (107, 142, 35)],
        "desert": [(255, 223, 0), (255, 160, 0), (255, 99, 71), (255, 69, 0), (255, 165, 0)],
        "ocean": [(70, 130, 180), (100, 149, 237), (30, 144, 255), (0, 191, 255), (0, 0, 205)],
        "rainforest": [(34, 139, 34), (0, 100, 0), (85, 107, 47), (107, 142, 35), (0, 128, 0)],
        "volcanic": [(139, 69, 19), (255, 69, 0), (255, 0, 0), (255, 140, 0), (0, 0, 0)],
        "arctic": [(240, 248, 255), (220, 220, 255), (255, 250, 250), (176, 224, 230), (135, 206, 250)],
        "sunset": [(255, 69, 0), (255, 165, 0), (255, 99, 71), (255, 20, 147), (255, 105, 180)],
        "calm": [(173, 216, 230), (240, 248, 255), (220, 220, 220), (176, 224, 230), (135, 206, 250)],
        "default": [(255, 255, 255), (220, 220, 220), (180, 180, 180), (140, 140, 140), (100, 100, 100)]
    }
    if prompt == "cloudy":
        roughness = 0.5
        palette = color_palettes["cloudy"]
    elif prompt == "mountainous":
        roughness = 1.5
        palette = color_palettes["mountainous"]
    elif prompt == "forest":
        roughness = 1.2
        palette = color_palettes["forest"]
    elif prompt == "desert":
        roughness = 1.3
        palette = color_palettes["desert"]
    elif prompt == "ocean":
        roughness = 0.8
        palette = color_palettes["ocean"]
    elif prompt == "rainforest":
        roughness = 1.0
        palette = color_palettes["rainforest"]
    elif prompt == "volcanic":
        roughness = 2.0
        palette = color_palettes["volcanic"]
    elif prompt == "arctic":
        roughness = 0.6
        palette = color_palettes["arctic"]
    elif prompt == "sunset":
        roughness = 1.0
        palette = color_palettes["sunset"]
    elif prompt == "calm":
        roughness = 0.5
        palette = color_palettes["calm"]
    else:
        roughness = 1.0
        palette = color_palettes["default"]
    noise_data = perlin_noise(width, height, scale, roughness)
    colored_image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            noise_value = noise_data[y, x]
            colored_image[y, x] = get_color_from_palette(noise_value, palette)
    return colored_image

def get_user_prompt():
    prompt = simpledialog.askstring("Stable Diffusion - Image Generation", "Enter a prompt (e.g., 'cloudy', 'ocean', 'forest'):\nExample prompts: cloudy, mountainous, forest, desert, ocean, etc.")
    if not prompt:
        prompt = "default"
    return prompt

def get_matched_prompt(user_input):
    available_prompts = ["cloudy", "mountainous", "forest", "desert", "ocean", "default"]
    for prompt in available_prompts:
        if prompt in user_input.lower():
            return prompt
    return "default"

def generate_and_show_image():
    user_input = get_user_prompt()
    prompt = get_matched_prompt(user_input)
    root = tk.Tk()
    root.title("Stable Diffusion - Image Generation")
    progress = ttk.Progressbar(root, length=300, mode='indeterminate')
    progress.pack(pady=20)
    progress.start()
    label = tk.Label(root, text="Generating Image... Please wait.")
    label.pack(pady=10)
    def generate_image():
        width, height = 512, 512
        colored_image_data = generate_colored_perlin_noise(width, height, scale=50, prompt=prompt)
        image = Image.fromarray(colored_image_data)
        progress.stop()
        label.config(text="Image Generated! You can find it in the folder.")
        image.show()
        image.save(f"color_image_{prompt}.png")
        root.after(2000, root.destroy)
    threading.Thread(target=generate_image).start()
    root.mainloop()

generate_and_show_image()

if __name__ == "__main__":
    generate_and_show_image()