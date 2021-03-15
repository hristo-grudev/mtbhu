import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import MtbhuItem
from itemloaders.processors import TakeFirst


class MtbhuSpider(scrapy.Spider):
	name = 'mtbhu'
	start_urls = ['https://www.mtb.hu/mtb-sajtoszoba']

	def parse(self, response):
		post_links = response.xpath('//li[@class="o-list__item"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h3[@id="page_title"]/text()').get()
		description = response.xpath('//div[@class="c-article__body tinymce u-mb-x4"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		try:
			date = re.findall(r'\d{4}\.\s\S+\s\d{2}', description)[0]
		except:
			try:
				date = re.findall(r'\d{4}\.\d{2}\.\d{2}|\d{2}\s\S+\s\d{4}', title)[0]
			except:
				date = ''

		item = ItemLoader(item=MtbhuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
