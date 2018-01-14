from spiders import baidu_spider
import time


def main():

    while True:
        search_content = input("\n请输入要查询的字符串:\n")
        baidu_spider.crawl(search_content)
        # time.sleep(1)


def test():
    with open('test.txt', 'r')as f:
        content = f.read()
    baidu_spider.load_html(content)


if __name__ == '__main__':
    main()
