from aip import AipOcr

# 百度OCR接口属性
APP_ID = '19266231'
API_KEY = 'aWbq8mIiC3K13QoCGH6YPUu3'
SECRET_KEY = 'Fe1c7PmQvScwwg1m1O4rLnoXGLNszGRD'

aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 通用文字识别（高精度版）
def basicAccurate(file):
    options = {}
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "true"  # 检测语言
    result = aipOcr.basicAccurate(file, options)
    return (result)

# 以列表的形式返回图片中提取的每一行文本
def detect_image(filepath):
    file = get_file_content(filepath)
    result = basicAccurate(file)
    print(result)
    sum = []
    for word in result['words_result']:
        sum.append(word['words'] + '\n')
    return sum