import cv2
from pyzbar.pyzbar import decode


def scan_qr_code(image_path):
    # 读取图片
    image = cv2.imread(image_path)

    # 检测并解码图像中的二维码
    decoded_objects = decode(image)

    for obj in decoded_objects:
        # 打印二维码数据
        print("Data:", obj.data.decode("utf-8"))

        # 绘制二维码的边界框
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(points)
            points = hull

        n = len(points)
        for j in range(0, n):
            cv2.line(image, points[j], points[(j + 1) % n], (0, 255, 0), 3)

    # 显示带有二维码边界框的图像
    cv2.imshow('QR Code Scanner', image)

    # 按下任意键关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 替换成你的图片路径
    image_path = '/Users/shadikesadamu/Downloads/WechatIMG903.jpg'
    scan_qr_code(image_path)
