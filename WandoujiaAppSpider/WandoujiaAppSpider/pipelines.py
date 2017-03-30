# coding:utf-8
import MySQLdb


class WandoujiaappspiderPipeline(object):

    @staticmethod
    def handle_special_char(content):
        '''
        This function is to delete special char like \ ' "  from content
        in case of error when insert content into database table
        :param content: the content to be inserted into database table
        :return: content after remove special char
        '''
        content = ''.join(content.split('\''))
        content = ''.join(content.split('\"'))
        content = ''.join(content.split('\\'))
        return content

    @staticmethod
    def set_insert_table_value(item):
        '''
        Generate the value message to be inserted into database table from item
        :param item: the spider passed item
        :return: the value message
        '''
        item_list = list()
        item_list.append(item['name'])
        item_list.append(item['package'])
        item_list.append(item['category'])
        item_list.append(item['description'])
        item_list.append(item['comments'])
        item_list.append(item['like_num'])
        item_list.append(item['install_num'])
        item_list.append(item['classification'])
        item_list.append(item['update_time'])
        item_list.append(item['tags'])
        item_list.append(item['url'])
        item_list.append(item['source'])
        value = ''
        for i in item_list:
            value += ('\'' + WandoujiaappspiderPipeline.handle_special_char(i) + '\'' + ',')
        return value.strip(',')

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def __init__(self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="tcslyz", db="app", charset='utf8')
        self.db.autocommit(1)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        sql = "insert into wandoujia20170328 (name, package, category, description,\
                comments, like_num, install_num ,classification, update_time, tags ,url, source) values(%s)" \
              % WandoujiaappspiderPipeline.set_insert_table_value(item)
        self.cursor.execute(sql)