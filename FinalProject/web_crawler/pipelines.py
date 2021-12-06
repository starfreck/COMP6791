# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import threading

from web_crawler.lib import create_folder, create_file


class WebCrawlerPipeline:
    folder_name = "Outputs"
    file_name = "data.json"
    full_path = folder_name + "/" + file_name
    lock = threading.Lock()

    def __init__(self):
        # Create a Folder & File if it doesn't exist
        create_folder(self.folder_name)
        create_file(self.full_path)

    def process_item(self, item, spider):
        new_data = {'url': item['url'], 'title': item['title'], 'body': item['body']}

        data = []
        # Acquire lock
        self.lock.acquire()

        try:
            # Read File
            with open(self.full_path, 'r') as f:
                data = json.loads(f.read())
                if data is None:
                    data = []
                data.append(new_data)
        finally:
            # Write File
            with open(self.full_path, 'w') as f:
                f.write(json.dumps(data))

        # Release lock
        self.lock.release()

        return item
