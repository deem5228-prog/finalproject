"""
Color Service Module
Extracts average RGB values from egg yolk cropped images
and converts RGB to CIELAB (L*, a*, b*) color space.
"""

import io
import numpy as np
from PIL import Image
from skimage.color import rgb2lab


def extract_mean_rgb(image_input):
    """
    Extract average R, G, B values from an image.
    
    :param image_input: str/Path (file path), bytes, or PIL.Image object
    :return: dict with 'r', 'g', 'b' (rounded floats 0-255)
    """
    if isinstance(image_input, (str, bytes)):
        if isinstance(image_input, str):
            img = Image.open(image_input)
        else:
            img = Image.open(io.BytesIO(image_input))
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise ValueError("Unsupported image input type. Expected file path, bytes, or PIL.Image.")

    # Convert to RGB mode (handles RGBA or grayscale)
    img_rgb = img.convert('RGB')
    np_img = np.array(img_rgb)

    # Compute mean R, G, B values (provides highest R^2 = 0.9056 for SVR model)
    mean_r = float(np.mean(np_img[:, :, 0]))
    mean_g = float(np.mean(np_img[:, :, 1]))
    mean_b = float(np.mean(np_img[:, :, 2]))

    return {
        'r': round(mean_r, 2),
        'g': round(mean_g, 2),
        'b': round(mean_b, 2)
    }


def rgb_to_cielab(r: float, g: float, b: float):
    """
    Convert RGB values (0-255) to CIELAB color space (L*, a*, b*).
    
    :param r: Red component (0-255)
    :param g: Green component (0-255)
    :param b: Blue component (0-255)
    :return: dict with 'l', 'a', 'b'
    """
    # Normalize RGB to [0, 1] range for skimage rgb2lab
    rgb_norm = np.array([[[r / 255.0, g / 255.0, b / 255.0]]], dtype=np.float64)
    lab_arr = rgb2lab(rgb_norm)[0, 0]

    l_val = float(lab_arr[0])
    a_val = float(lab_arr[1])
    b_val = float(lab_arr[2])

    # Compute Chroma (C*) = sqrt(a*^2 + b*^2)
    chroma = float(np.sqrt(a_val**2 + b_val**2))

    # Compute Hue Angle (h°) = arctan2(b*, a*) in degrees (0 to 360)
    hue_rad = np.arctan2(b_val, a_val)
    hue_deg = float(np.degrees(hue_rad))
    if hue_deg < 0:
        hue_deg += 360.0

    return {
        'l': round(l_val, 2),
        'a': round(a_val, 2),
        'b': round(b_val, 2),
        'chroma': round(chroma, 2),
        'hue_angle': round(hue_deg, 2)
    }


def extract_color_features(image_input):
    """
    Extract both RGB and CIELAB color features from an image.
    
    :param image_input: str/Path (file path), bytes, or PIL.Image object
    :return: dict containing r, g, b, l, a, b
    """
    rgb = extract_mean_rgb(image_input)
    lab = rgb_to_cielab(rgb['r'], rgb['g'], rgb['b'])
    return {
        'r': rgb['r'],
        'g': rgb['g'],
        'b': rgb['b'],
        'l': lab['l'],
        'a': lab['a'],
        'b': lab['b'],
        'chroma': lab['chroma'],
        'hue_angle': lab['hue_angle']
    }


if __name__ == '__main__':
    # Simple test run
    test_rgb = extract_mean_rgb(Image.new('RGB', (100, 100), color=(226, 131, 23)))
    test_lab = rgb_to_cielab(test_rgb['r'], test_rgb['g'], test_rgb['b'])
    print("Test RGB:", test_rgb)
    print("Test CIELAB:", test_lab)
