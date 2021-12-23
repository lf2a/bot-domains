import os.path
from datetime import datetime

from botcity.web import WebBot, Browser

from botDomains.search_domains.exceptions import ImageNotFoundException


class GoDaddy(WebBot):

    @classmethod
    def run(cls, print_path: str, domain: str):
        go = GoDaddy()
        go.load()
        go.goto('https://www.godaddy.com/pt-br')

        try:
            go.search(domain)
            go.get_domain_print(print_path, domain)
        except ImageNotFoundException as e:
            print(e)
        finally:
            go.stop_browser()

        go.stop_browser()

    def load(self):
        self.add_image('go_consultar_dominio', self.get_resource_abspath('go_consultar_dominio.png'))
        self.add_image('go_aguardando_buscar', self.get_resource_abspath('go_aguardando_buscar.png'))
        self.add_image('go_anchor_ajuda', self.get_resource_abspath('go_anchor_ajuda.png'))

    def goto(self, url: str):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        print(os.path.join(root_dir, '..', 'resources', 'web-drivers', 'geckodriver.exe'))
        self.headless = True
        self.browser = Browser.FIREFOX
        self.driver_path = os.path.join(root_dir, '..', 'resources', 'web-drivers', 'geckodriver.exe')

        print('Acessando: ' + url)

        self.browse(url)
        self.set_screen_resolution(1920, 1080)
        self.wait(5_000)

    def search(self, dominio: str):
        print('Buscando: ' + dominio)
        if not self.find('go_consultar_dominio', matching=0.9, waiting_time=20_000):
            self.not_found('go_consultar_dominio')

        self.click_relative(-329, 0, wait_after=1000)
        self.paste(dominio, wait=1000)
        self.enter(wait=10_000)

        for i in range(0, 5):
            if self.find('go_aguardando_buscar', matching=0.9, waiting_time=10_000):
                print('Buscando...')
                continue
            print('Busca finalizada!')
            break

    def get_domain_print(self, path_to_save: str, domain: str):
        for i in range(0, 100):
            timestamp = datetime.now().timestamp()
            file_path = os.path.join(path_to_save, str(i) + '-' + domain + '-' + str(timestamp) + '.png')
            print('Saving print: %s' % file_path)
            self.save_screenshot(file_path)

            if self.find("go_anchor_ajuda", matching=0.9, waiting_time=5_000):
                break

            self.scroll_down(2)

    def not_found(self, element: str):
        print('Element Not Found: %s' % element)
        raise ImageNotFoundException('Element Not Found: %s' % element)
