from lxml import etree
import requests

BASE_DOMAIN = 'http://www.ygdy8.net'

HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/69.0.3497.100 Safari/537.36",
    }

def get_detail_urls(url):

    response = requests.get(url, headers=HEADERS)
    # print(response.text)
    # print(response.content.decode('gbk'))
    html = response.text

    html = etree.HTML(html)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    # for detail_url in detail_urls:
    #     print(BASE_DOMAIN+detail_url)
    detail_urls = map(lambda  url:BASE_DOMAIN+url, detail_urls)
    return detail_urls

def parse_detail_page(url):
    movie = {}
    response = requests.get(url,headers=HEADERS)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    movie['title'] = title

    zoomE = html.xpath("//div[@id='Zoom']")[0]
    imgs = zoomE.xpath(".//img/@src")
    if imgs is list:
        cover = imgs[0]
        screenshot = imgs[1]
        movie['cover'] = cover
        movie['screenshot'] = screenshot
    else:
        movie['cover'] = imgs

    def parse_infor(infor, rule):
        return infor.replace(rule,"").strip()

    infors = zoomE.xpath(".//text()")
    for index,infor in enumerate(infors):
        # print(infor)
        # print(index)
        # print("="*30)

        if infor.startswith("◎年　　代"):
            infor = parse_infor(infor,"◎年　　代")
            movie['year'] = infor
        elif infor.startswith("◎产　　地"):
            infor = parse_infor(infor, "◎产　　地")
            movie['country'] = infor
        elif infor.startswith("◎类　　别"):
            infor = parse_infor(infor, "◎类　　别")
            movie['category'] = infor
        elif infor.startswith("◎语　　言"):
            infor = parse_infor(infor, "◎语　　言")
            movie['language'] = infor
        elif infor.startswith("◎IMDb评分"):
            infor = parse_infor(infor, "◎IMDb评分")
            movie['imdb_rating'] = infor
        elif infor.startswith("◎片　　长"):
            infor = parse_infor(infor, "◎片　　长")
            movie['duration'] = infor
        elif infor.startswith("◎导　　演"):
            infor = parse_infor(infor, "◎导　　演")
            movie['director'] = infor
        elif infor.startswith("◎主　　演"):
            infor = parse_infor(infor, "◎主　　演")
            actors = [infor]
            for x in range(index+1, len(infors)):
                actor = infors[x].strip()
                if actor.startswith("◎简　　介"):
                    break
                actors.append(actor)
            movie['actors'] = actors
        elif infor.startswith("◎简　　介"):
            infor = parse_infor(infor, "◎简　　介")
            # movie['introduction'] = infor
            for x in range(index+1,len(infors)):
                profile = infors[x].strip()
                if profile.startswith("【下载地址】"):
                    break
                movie['profile'] = profile
    dowmload_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie['download_url'] = dowmload_url
    return movie





def spider():
    # {}占个位置，format填充
    base_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'
    movies = []
    for x in range(1,8):
        # 第一个for循环控制总共有7页
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            # 第二个for循环遍历一页中所有电影详情url
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)

    # print(movies)


if __name__ == '__main__':
    spider()