from PIL import Image, ImageDraw

def create_striped_pattern(image_size, stripe_color, stripe_width_ratio=0.2):

    stripes = Image.new("RGBA", image_size)
    draw = ImageDraw.Draw(stripes)
    stripe_height = int(36 * stripe_width_ratio)
    gap_height = 36 - stripe_height

    for x in range(0, stripes.size[1], stripe_height + gap_height):
        draw.rectangle([(x, 0), (x + stripe_height, stripes.size[1])], fill=stripe_color)

    return stripes

def apply_pattern_to_image(original_img, pattern_img=None, pattern_type="solid", overlay_color=(255, 0, 0)):

    width, height = original_img.size

    for x in range(width):
        for y in range(height):
            r, g, b, a = original_img.getpixel((x, y))
            brightness = (r + g + b) / 3

            if pattern_type == "stripes" and pattern_img:
                new_color = pattern_img.getpixel((x, y))[:3] + (min(pattern_img.getpixel((x, y))[3],a),) if brightness > 127 else overlay_color + (a,)
            elif pattern_type == "solid":
                new_color = overlay_color + (a,)
            if pattern_type == "empty":
                new_color = (255, 255, 255, 0) if brightness > 127 else overlay_color + (a,)

            original_img.putpixel((x, y), new_color)

    return original_img

def process_image(image_path, overlay_color, filling_type):

    img = Image.open(image_path).convert("RGBA")
    pattern_img = None

    if filling_type == "stripes":
        pattern_img = create_striped_pattern(img.size, overlay_color)

    return apply_pattern_to_image(img, pattern_img, filling_type, overlay_color)

def create_card(logo, number, height=768):
    # Calculate image dimensions
    bg_width, bg_height = height // 2, height

    # Load and resize the logo
    logo_size = height // 3
    logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

    # Create a white background image
    background = Image.new('RGB', (bg_width, bg_height), 'white')

    # Calculate the position for the logos
    x = (bg_width - logo_size) // 2
    y_space = (bg_height - (logo_size * number)) // (number + 1)

    # Paste the logo(s) onto the background
    for i in range(number):
        y = y_space * (i + 1) + logo_size * i
        background.paste(logo, (x, y), logo)

    return background

def create_card_with_template(logo, number, template_path):

    background = Image.open(template_path).convert("RGBA")

    bg_width, bg_height = background.size

    # Load and resize the logo
    logo_size = round(bg_height // 3.2)
    logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)


    # Calculate the position for the logos
    x = (bg_width - logo_size) // 2
    y_space = (bg_height - (logo_size * number)) // (number + 1)

    # Paste the logo(s) onto the background
    for i in range(number):
        y = y_space * (i + 1) + logo_size * i
        background.paste(logo, (x, y), logo)

    return background


def convert_to_custom_base3(number):
    # Convert the number to base 3
    base3_number = ''
    while number > 0:
        base3_number = str(number % 3) + base3_number
        number //= 3

    # Make it 4 characters long by adding leading zeros if necessary
    base3_number = base3_number.zfill(4)

    # Replace 0 with 'a', 1 with 'b', and 2 with 'c'
    custom_string = base3_number.replace('0', 'a').replace('1', 'b').replace('2', 'c')

    return custom_string

def create_set(shapes, colors, height=120, template=False):
    n=0
    for shape in shapes:
        for color in colors:
            for filling in ["empty","stripes","solid"]:
                logo = process_image(shape, color, filling)
                for number in [1,2,3]:
                    # print(n,shape, color, number, filling)
                    if template==False:
                        create_card(logo, number, height).rotate(90, expand=True).save(str(n)+".png")
                    else:
                        create_card_with_template(logo, number, template).save(convert_to_custom_base3(n)+".png")
                    n+=1


shapes=["./a.png","./b.png","./c.png"]
colors = [(198, 0, 100),(255, 128, 0),(24, 151, 173)]
create_set(shapes, colors)
