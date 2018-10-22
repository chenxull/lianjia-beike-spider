#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import re
from bs4 import BeautifulSoup
from lib.item.xiaoqu import *
from lib.zone.district import *
from lib.request.headers import *
from lib.utility.log import logger
from lib.spider.spider import SPIDER_NAME


def get_xiaoqu_info(city, area):
    district = area_dict.get(area, "")
    chinese_district = get_chinese_district(district)
    chinese_area = chinese_area_dict.get(area, "")
    xiaoqu_list = list()
    page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDER_NAME, area)
    print(page)
    logger.info(page)

    headers = create_headers()
    response = requests.get(page, timeout=10, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
        total_page = int(matches.group(1))
    except Exception as e:
        print("\tWarning: only find one page for {0}".format(area))
        print(e)
        total_page = 1

    # 从第一页开始,一直遍历到最后一页
    for i in range(1, total_page + 1):
        headers = create_headers()
        page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, area, i)
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elems = soup.find_all('li', class_="xiaoquListItem")
        for house_elem in house_elems:
            price = house_elem.find('div', class_="totalPrice")
            name = house_elem.find('div', class_='title')
            on_sale = house_elem.find('div', class_="xiaoquListItemSellCount")

            # 继续清理数据
            price = price.text.strip()
            name = name.text.replace("\n", "")
            on_sale = on_sale.text.replace("\n", "").strip()

            # 作为对象保存
            xiaoqu = XiaoQu(chinese_district, chinese_area, name, price, on_sale)
            xiaoqu_list.append(xiaoqu)
    return xiaoqu_list


if __name__ == "__main__":
    # urls = get_xiaoqu_area_urls()
    # print urls
    get_xiaoqu_info("sh", "beicai")