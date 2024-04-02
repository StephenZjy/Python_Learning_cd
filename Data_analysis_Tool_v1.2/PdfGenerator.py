import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import utils
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT

font_path = 'C:\\Windows\\Fonts\\msyh.ttc'
pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
DEFAULT_FONT['helvetica'] = 'ChineseFont'


def add_image(canvas, img_path, x, y, width, height):
    if os.path.exists(img_path):
        img = utils.ImageReader(img_path)
        canvas.drawImage(img, x, y, width, height, preserveAspectRatio=True, mask='auto')
    else:
        print(f"Image not found: {img_path}. Skipping.")

def generate_pdf_single_run(output_path, label):
    pdf_path = output_path + f'/report_{label}.pdf'
    # 创建PDF文档
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # 设置正文字体
    body_font = 'ChineseFont'
    body_size = 15

    # 添加标题
    c.setFont(body_font, body_size + 10)
    title_text = "数据分析报告"
    c.drawCentredString(306, 750, title_text)

    # 添加基础信息
    c.setFont(body_font, body_size)
    basic_info = "1. 基础信息"
    c.drawString(30, 700, basic_info)

    # 生成Fig 1-1 run信息汇总
    fig_path = output_path + f"/imgs_{label}/run_info.png"
    add_image(c, fig_path, 30, 250, 550, 500)

    c.showPage()

    # 添加上孔信息
    c.setFont(body_font, body_size)
    hole_info = "2. 上孔信息"
    c.drawString(30, 750, hole_info)

    # 生成Fig 1-2 run上孔信息
    fig_path = output_path + f"/imgs_{label}/pore_info.png"
    add_image(c, fig_path, 0, 540, 350, 200)

    c.showPage()

    # 添加1. 准确率相关统计
    c.setFont(body_font, body_size)
    chapter_title = "3. 准确率相关统计"
    c.drawString(30, 750, chapter_title)

    # 添加1.1 准确率分布
    c.setFont(body_font, body_size - 2)
    section_title = "3.1 准确率分布"
    c.drawString(30, 710, section_title)

    # 生成Fig 1-1-1 准确率分布直⽅图
    fig_path = output_path + f"/imgs_{label}/average_identity_distribution.png"
    add_image(c, fig_path, 15, 400, 600, 300)

    # 添加1.2 与读⻓关系
    section_title = "3.2 与读⻓的关系"
    c.drawString(30, 360, section_title)

    # 生成L617 - Read len与Identity相关性散点图
    scatter_plot_path = output_path + f"/imgs_{label}/correlation_read_len_and_identity.png"
    add_image(c, scatter_plot_path, 15, 50, 600, 300)

    c.showPage()

    c.setFont(body_font, body_size - 2)
    section_title = "3.3 错误类型统计"
    c.drawString(30, 740, section_title)

    c.setFont(body_font, body_size - 5)
    section_title = "错误类型统计汇总表"
    c.drawString(258, 700, section_title)

    fig_path = output_path + f"/imgs_{label}/error_type_statistics.png"
    add_image(c, fig_path, 30, 450, 550, 300)

    fig_path = output_path + f"/imgs_{label}/base_error_type.png"
    add_image(c, fig_path, 15, 150, 600, 300)

    c.showPage()

    fig_path = output_path + f"/imgs_{label}/error_type.png"
    add_image(c, fig_path, 15, 450, 600, 300)

    fig_path = output_path + f"/imgs_{label}/base_error.png"
    add_image(c, fig_path, 15, 100, 600, 300)

    c.showPage()

    c.setFont(body_font, body_size)
    read_len_info = "4. 读长相关统计"
    c.drawString(30, 750, read_len_info)

    # 生成Fig 1-2 run上孔信息
    fig_path = output_path + f"/imgs_{label}/read_len_distribution.png"
    add_image(c, fig_path, 15, 440, 600, 300)

    read_len_info = "5. 速度相关统计"
    c.drawString(30, 400, read_len_info)

    # 生成Fig 1-2 run上孔信息
    fig_path = output_path + f"/imgs_{label}/linker_speed_distribution.png"
    add_image(c, fig_path, 15, 90, 600, 300)

    c.showPage()

    c.setFont(body_font, body_size)
    chapter_title = "6. AR相关统计"
    c.drawString(30, 750, chapter_title)

    c.setFont(body_font, body_size - 2)
    section_title = "6.1 AR分布"
    c.drawString(30, 700, section_title)

    # 生成Fig 1-1-1 准确率分布直⽅图
    fig_path = output_path + f"/imgs_{label}/ar_mean_distribution.png"
    add_image(c, fig_path, 15, 390, 600, 300)

    # 添加1.2 与读⻓关系
    section_title = "6.2 四种碱基AR占比"
    c.drawString(30, 350, section_title)

    # 生成L617 - Read len与Identity相关性散点图
    scatter_plot_path = output_path + f"/imgs_{label}/4_base_AR.png"
    add_image(c, scatter_plot_path, 15, 40, 600, 300)

    c.showPage()

    c.setFont(body_font, body_size)
    chapter_title = "7. DW相关统计"
    c.drawString(30, 750, chapter_title)

    c.setFont(body_font, body_size - 2)
    section_title = "7.1 DW分布"
    c.drawString(30, 700, section_title)

    # 生成Fig 1-1-1 准确率分布直⽅图
    fig_path = output_path + f"/imgs_{label}/dw_mean_distribution.png"
    add_image(c, fig_path, 15, 390, 600, 300)

    # 添加1.2 与读⻓关系
    section_title = "7.2 四种碱基DW占比"
    c.drawString(30, 350, section_title)

    # 生成L617 - Read len与Identity相关性散点图
    scatter_plot_path = output_path + f"/imgs_{label}/4_base_DW.png"
    add_image(c, scatter_plot_path, 15, 40, 600, 300)

    c.showPage()

    c.setFont(body_font, body_size)
    chapter_title = "8. CR相关统计"
    c.drawString(30, 750, chapter_title)

    c.setFont(body_font, body_size - 2)
    section_title = "8.1 CR分布"
    c.drawString(30, 700, section_title)

    # 生成Fig 1-1-1 准确率分布直⽅图
    fig_path = output_path + f"/imgs_{label}/cr_mean_distribution.png"
    add_image(c, fig_path, 15, 390, 600, 300)

    # 添加1.2 与读⻓关系
    section_title = "8.2 四种碱基CR占比"
    c.drawString(30, 350, section_title)

    # 生成L617 - Read len与Identity相关性散点图
    scatter_plot_path = output_path + f"/imgs_{label}/4_base_CR.png"
    add_image(c, scatter_plot_path, 15, 40, 600, 300)

    c.showPage()

    c.setFont(body_font, body_size)
    chapter_title = "9. Pore-LT与Basecall-LT相关统计"
    c.drawString(30, 750, chapter_title)

    fig_path = output_path + f"/imgs_{label}/Pore_LT-Basecall_LT.png"
    add_image(c, fig_path, 15, 440, 600, 300)

    # 保存PDF文档
    c.save()


def generate_pdf_multiple_run(output_path, label_list):
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Analysis Report</title>
</head>
<body>
<h1 style="font-size: 33px;text-align: center;">数据分析报告</h1>

<h2 style="font-size: 20px;">1. 基础信息</h2>

<img src="{output_path}/imgs/run_info.png">

<div style="page-break-after: always;"></div>

<h2 style="font-size: 20px;">2. 上孔信息</h2>

<img src="{output_path}/imgs/pore_info.png">

<div style="page-break-after: always;"></div>

<h2 style="font-size: 20px;">3. 准确率相关统计</h2>

<h3 style="font-size: 18px;">3.1 准确率分布</h3>

<img src="{output_path}/imgs/average_identity_distribution.png" width="900" height="450">

<h3 style="font-size: 18px;">3.2 与读长关系</h3>
'''
    for label in label_list:
        html_content += f'''
<div></div>
<img src="{output_path}/imgs/correlation_read_len_and_identity_{label}.png" width="900" height="450">
'''
    html_content += f'''
<h3 style="font-size: 18px;">1.3 错误类型统计</h3>
<h4 style="font-size: 15px;">1.3.1 错误类型统计汇总表</h4>
'''
    for label in label_list:
        html_content += f'''
<div style="font-size: 13px; text-align: center;"><p>{label} - 错误类型统计汇总表</p></div>
<img src="{output_path}/imgs/error_type_statistics_{label}.png" width="640" height="230" style="text-align: center;">
'''
    html_content += f'''
<h4 style="font-size: 15px;">1.3.2 错误类型统计汇总图</h4>
'''
    for label in label_list:
        html_content += f'''
<div></div>
<img src="{output_path}/imgs/base_error_type_{label}.png" width = "900"height = "450" >
<div></div>
'''
    html_content += f'''
<div style="page-break-after: always;"></div>

<h4 style="font-size: 15px;">1.3.3 错误类型对比图</h4>
<div></div>
<img src="{output_path}/imgs/error_type.png" width="900" height="450">

<div></div>
<img src="{output_path}/imgs/base_error.png" width="900" height="450">

<div style="page-break-after: always;"></div>

<h2 style="font-size: 20px;">4. 读长相关统计</h2>

<img src="{output_path}/imgs/read_len_distribution.png" width="900" height="450">

<h2 style="font-size: 20px;">5. 速度相关统计</h2>

<img src="{output_path}/imgs/linker_speed_distribution.png" width="900" height="450">

<div style="page-break-after: always;"></div>

<h2 style="font-size: 20px;">6. AR相关统计</h2>

<h3 style="font-size: 18px;">6.1 AR分布</h3>

<img src="{output_path}/imgs/ar_mean_distribution.png" width="900" height="450">

<h3 style="font-size: 18px;">6.2 四种碱基AR占比</h3>
'''
    for label in label_list:
        html_content += f'''
<div></div>
<img src="{output_path}/imgs/4_base_AR_{label}.png" width="900" height="450">
'''
    html_content += f'''
<h2 style="font-size: 20px;">7. DW相关统计</h2>

<h3 style="font-size: 18px;">7.1 DW分布</h3>

<img src="{output_path}/imgs/dw_mean_distribution.png" width="900" height="450">

<div style="page-break-after: always;"></div>

<h3 style="font-size: 18px;">7.2 四种碱基DW占比</h3>
'''
    for label in label_list:
        html_content += f'''
<div></div>
<img src="{output_path}/imgs/4_base_DW_{label}.png" width="900" height="450">
'''
    html_content += f'''
<div style="page-break-after: always;"></div>

<h2 style="font-size: 20px;">8. CR相关统计</h2>

<h3 style="font-size: 18px;">8.1 CR分布</h3>

<img src="{output_path}/imgs/cr_mean_distribution.png" width="900" height="450">

<h3 style="font-size: 18px;">8.2 四种碱基CR占比</h3>
'''
    for label in label_list:
        html_content += f'''
<div></div>
<img src="{output_path}/imgs/4_base_CR_{label}.png" width="900" height="450">
'''
    html_content += f'''
<h2 style="font-size: 20px;">9. Pore-LT与Basecall-LT相关统计</h2>
'''
    for label in label_list:
        html_content += f'''
<div></div>
<img src="{output_path}/imgs/Pore_LT-Basecall_LT_{label}.png" width="900" height="450">
'''
    pdf_path = output_path + '/report.pdf'
    html_to_pdf(html_content, pdf_path)


def html_to_pdf(html_content, output_pdf_path):
    with open(output_pdf_path, "w+b") as pdf_file:
        pisa.pisaDocument(io.BytesIO(html_content.encode('utf-8')), pdf_file, encoding='utf-8', font_path='ChineseFont')
