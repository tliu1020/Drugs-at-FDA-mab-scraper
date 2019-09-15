import scrapy
import json
import re
from ..items2 import FdaItem

class fdaSpider(scrapy.Spider):

    name = "api"
    start_urls = ['https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm ']
    # allowed_domains = ['accessdata.fda.gov']

    def parse(self, response):

        # count = 0

        for letter in response.css("div.tab-content a"):
            # count = count + 1
            url = letter.css("a::attr(href)").extract_first()

            yield response.follow(url, callback=self.parse2)

            # if count > 10:
            #     break

    def parse2(self, response):

        for drug in response.css("div.col-md-12 ul.collapse"):

            if drug.css("a::text").extract_first() in drug.css("a::text").re(r'.*\(.*MAB.*\).*'):

                index1 = drug.css("a::text").extract_first().find("(")
                brand = drug.css("a::text").extract_first()[:index1 -1]
                api_url = "https://api.fda.gov/drug/label.json?search=openfda.brand_name:" + "\"" + brand + "\""

                yield response.follow(api_url, callback=self.parse3)

    def parse3(self, response):

        item = FdaItem()
        json_response = json.loads(response.body_as_unicode())
        item["generic_drug"] = json_response["results"][0]["openfda"]["generic_name"][0]
        item["brand_drug"] = json_response["results"][0]["openfda"]["brand_name"][0]

        desc = json_response["results"][0]["description"][0]
        drug_subclass = re.findall(r"(DESCRIPTION:*\s[A-Z].*?\.(?=\s))", desc)
        item["drug_subclass"] = drug_subclass[0][12:]
        pH_lines = re.findall(r"(pH[^.]+?[a-z\s]*\d\.*\d*(\sto\s\d\.*\d*)*)", desc)
        pH_string = ", ".join(str(x) for x in pH_lines)

        item["ph"] = ','.join(str(x) for x in re.findall(r"(\d+\.?\d*)", pH_string))

        conc_lines = re.findall(r"(concentration.*?\d+\.?\d*.*?(?<=\/).*?(?=[\s\.]))", desc)
        conc_string = ", ".join(str(x) for x in conc_lines)
        conc_string = conc_string + " "

        item["concentration"] = ','.join(str(x) for x in re.findall(r"(\d+\.?\d*.*?(?<=\/).*?(?=[\s\.]))", conc_string))

        sentences_list = re.findall(r"(?<=\.)\s[A-Z].*?\.(?!\d)", desc)
        formulation_list = []
        for sentence in sentences_list:
            if "polysorbate" in sentence:
                formulation_list.append(sentence)

        item["formulation"] = formulation_list
        item["description"] = desc
        yield item
