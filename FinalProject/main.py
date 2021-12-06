import subprocess

from web_crawler.lib import remove_old_outputs
from web_crawler.settings import CLOSESPIDER_ITEMCOUNT

remove_old_outputs()

CLOSESPIDER_ITEMCOUNT = int(input("Enter How many pages you want to scrap? [Upper Boud]:"))

subprocess.run(["C:\\Users\\vasur\\Documents\\GitHub\\COMP6791\\FinalProject\\venv\\Scripts\\scrapy.exe","crawl","concordia"])