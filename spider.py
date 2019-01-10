from urllib import request
import re

class Spider():

    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<i class="video-station-num">([\s\S]*?)</i>'
    attention_number_pattern = '<i class="ricon ricon-eye"></i>([\s\S]*?)</span>'
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='UTF-8')
        return htmls
        a = 1

    def __analysis(self, htmls):
        root_html=re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            attention_number = re.findall(Spider.attention_number_pattern, html)
            anchor = {'name': name, 'number': number, 'attention_number': attention_number}
            anchors.append(anchor)
        return anchors

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*',anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        for anchor in anchors:
            print(anchor['name']+'   '+anchor['number']+'   '+anchor['attention_number'])


    def __refine(self, anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0],
            'attention_number': anchor['attention_number'][0]
            }
        return map(l, anchors)

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()


