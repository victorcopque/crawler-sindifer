import scrapy

from crawler_sindifer.list_associates import all_links


class AssociatesSindifer(scrapy.Spider):
    name = 'AssociatesSindifer'
    allowed_domains = ['sindiferes.com.br']
    start_urls = ["https://sindiferes.com.br/associados"]

    custom_settings={ 'FEED_URI': "sindifer.csv", 'FEED_FORMAT': 'csv'} 

    def parse(self, response):

        for company_main_link in all_links:
            yield scrapy.Request(
                url=response.urljoin(company_main_link), 
                callback=self.parse_company_details,
            )

    def parse_company_details(self, response):
        name = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[2]/td[1]/text()").extract_first()
        phone = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[8]/td[1]/text()").extract_first()
        email_header = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[9]/th[1]/text()").extract_first()
        email = ""
        if email_header == "E-mail:":
            email = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[10]/td[1]/text()").extract_first()
            street = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[13]/td[1]/text()").extract_first()
            neighborhood = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[15]/td[1]/text()").extract_first()
            city = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[15]/td[2]/text()").extract_first()
            state = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[15]/td[3]/text()").extract_first()
        else:
            street = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[11]/td[1]/text()").extract_first()
            neighborhood = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[13]/td[1]/text()").extract_first()
            city = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[13]/td[2]/text()").extract_first()
            state = response.xpath("//div[@id='site']/div[@id='coluna_2']/div[@id='cont']/table[@class='tabela_associado']/tr[13]/td[3]/text()").extract_first()

        scraped_info = {
            'Empresa': name, 
            'Phone': phone,
            'Email': email,
            'Logradouro': street,
            'Bairro': neighborhood,
            'Cidade': city,
            'Estado': state
        }
        yield scraped_info