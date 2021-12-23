import os.path
from datetime import datetime

from botcity.web import WebBot, Browser

from botDomains.search_domains.exceptions import ImageNotFoundException


class GoogleDomain(WebBot):

    @classmethod
    def run(cls, print_path: str, domain: str):
        go = GoogleDomain()
        go.load()
        go.goto('https://domains.google/intl/pt-BR_br/')

        try:
            go.search(domain)
            go.filtrar()
            go.get_domain_print(print_path, domain)
        except ImageNotFoundException as e:
            print(e)
        finally:
            go.stop_browser()

    def load(self):
        self.add_image('gd_procurar', self.get_resource_abspath('gd_procurar.png'))
        self.add_image('gd_filtro', self.get_resource_abspath('gd_filtro.png'))
        self.add_image('gd_search_ter', self.get_resource_abspath('gd_search_ter.png'))
        self.add_image('gd_.com', self.get_resource_abspath('gd_.com.png'))
        self.add_image('gd_aplicar', self.get_resource_abspath('gd_aplicar.png'))

    def goto(self, url: str):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.headless = True
        self.browser = Browser.CHROME
        self.driver_path = os.path.join(root_dir, '..', 'resources', 'web-drivers', 'chromedriver.exe')

        print('Acessando: ' + url)

        self.browse(url)
        self.wait(5_000)

    def search(self, dominio: str):
        if not self.find("gd_procurar", matching=0.9, waiting_time=20_000):
            self.not_found("gd_procurar")
        self.click(wait_after=1000)
        self.paste(dominio, wait=1000)
        self.enter(5000)

    def filtrar(self):
        if not self.find("gd_filtro", matching=0.9, waiting_time=20_000):
            self.not_found("gd_filtro")

        self.click(wait_after=1000)
        self.wait(10_000)

        # com, dev, com.br, io
        if not self.find("gd_search_ter", matching=0.9, waiting_time=20_000):
            self.not_found("gd_search_ter")
        self.click(wait_after=1000)

        self.paste('com', wait=1000)

        if not self.find("gd_.com", matching=0.9, waiting_time=20_000):
            self.not_found("gd_.com")

        self.click_relative(-38, 5, wait_after=1000)

        if not self.find("gd_aplicar", matching=0.9, waiting_time=20_000):
            self.not_found("gd_aplicar")

        self.click(wait_after=10_000)

    def get_domain_print(self, path_to_save: str, domain: str):
        for i in range(0, 5):
            timestamp = datetime.now().timestamp()
            file_path = os.path.join(path_to_save, str(i) + '-' + domain + '-' + str(timestamp) + '.png')
            print('Saving print: %s' % file_path)
            self.save_screenshot(file_path)
            self.scroll_down(2)

    def not_found(self, element: str):
        print('Element Not Found: %s' % element)
        raise ImageNotFoundException('Element Not Found: %s' % element)
