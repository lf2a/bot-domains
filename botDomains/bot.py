import os
from pathlib import Path
from zipfile import ZipFile

from botcity.maestro import AutomationTaskFinishStatus
from botcity.web import WebBot

from botDomains.search_domains.godaddy import GoDaddy
from botDomains.search_domains.google_domains import GoogleDomain

PRINTS_PATH = os.path.join(str(Path.home()), 'Pictures')


class Bot(WebBot):
    def action(self, execution=None):
        domain = 'botcity.dev'

        try:
            GoDaddy.run(PRINTS_PATH, domain)
            GoogleDomain.run(PRINTS_PATH, domain)

            self.maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Task Finished OK."
            )
        except Exception as e:
            print(e)
            self.maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.FAILED,
                message="Task Finished - ERRO: %s" % e
            )

        zip = zip_result_files()
        print('Zip file: %s' % zip)
        self.maestro.post_artifact(execution.task_id, 'bot-domains-test.zip', zip)


def zip_result_files() -> str:
    zip_path = os.path.join(PRINTS_PATH, 'bot-domains-test.zip')
    os.chdir(PRINTS_PATH)
    with ZipFile(zip_path, 'w') as zipObj2:
        for file in os.listdir(PRINTS_PATH):
            if file.endswith('.png') or file.endswith('.jpg'):
                zipObj2.write(file)
    return zip_path


if __name__ == '__main__':
    Bot.main()
