

def get_letter_pixels(letter):
    """maps a given letter to a (10, 10) array of pixel values,
    where a 1 represents a letter pixel"""
    from PIL import Image, ImageDraw, ImageFont

    img_size = (10, 10)  # Adjust as needed
    img = Image.new("1", img_size, color=0)  # 1-bit image (black & white)
    draw = ImageDraw.Draw(img)

    # Load a font (you can use a different TTF file)
    font = ImageFont.load_default()

    # Draw letter
    draw.text((0, 0), letter, font=font, fill=1)

    # Convert to pixel matrix
    pixels = list(img.getdata())
    width, height = img.size
    pixel_matrix = [pixels[i * width : (i + 1) * width] for i in range(height)]
    return pixel_matrix
