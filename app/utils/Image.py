import random
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw


def gen_picture(code):
    """生成验证码图片
    """
    # 新建一个图层
    im = Image.new('RGB', (50, 15), 'white')
    # 加载默认字体
    font = ImageFont.load_default()
    # 获取draw对象
    draw = ImageDraw.Draw(im)
    # 随机颜色
    random_color = (
        random.randint(32, 127),
        random.randint(32, 127),
        random.randint(32, 127))
    # 将数字输出到图片
    for item in range(4):
        draw.text(
            (6 + random.randint(-3, 3) + 10 * item,
             2 + random.randint(-2, 2)),
            text=code[item], fill=random_color, font=font)

    # 保存图片
    #im.save("./media/captcha/%s.png" % str(code), format="JPEG")

    # 重新设置图片大小
    im.resize((100, 24))
    # 图片转换为Base64字符串
    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_str = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')
