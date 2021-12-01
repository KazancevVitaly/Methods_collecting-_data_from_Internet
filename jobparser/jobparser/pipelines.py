# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobparserPipeline:
    def process_item(self, item, spider):
        print()
        if spider.name == 'hhru':
            final_salary = self.process_salary_hhru(item['salary'])
        else:
            final_salary = self.process_salary_superjob(item['salary'])
        min_salary = final_salary[0]
        max_salary = final_salary[1]
        currency = final_salary[2]
        return item

    def process_salary_hhru(self, salary):
        print()
        try:
            currency = salary[-2]
        except IndexError:
            currency = None
        lst = []
        for i in range(len(salary)):
            salary[0] = salary[0].replace(u'\xa0', u'')
            salary[0] = salary[0].replace(u' ', u'')
            try:
                salary[0] = int(salary[0])
                lst.append(salary[0])
                salary.pop(0)
            except ValueError:
                salary.pop(0)
            try:
                min_salary = min(lst)
            except ValueError:
                min_salary = None
            try:
                max_salary = max(lst)
            except ValueError:
                max_salary = None

        # min_salary = None
        # max_salary = None
        # currency = None
        return min_salary, max_salary, currency

    def process_salary_superjob(self, salary):
        print()
        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')
        if salary[0] == 'По договорённости':
            currency = None
            min_salary = None
            max_salary = None
        elif salary[0] == 'от' or salary[0] == 'до':
            min_salary = []
            currency = []
            for simb in salary[-1]:
                try:
                    number = int(simb)
                    min_salary.append(simb)
                except ValueError:
                    currency.append(simb)
            currency = ''.join(currency)
            min_salary = int(''.join(min_salary))
            max_salary = min_salary
        else:
            currency = salary[-1]
            min_salary = int(salary[0])
            max_salary = int(salary[1])
        return min_salary, max_salary, currency
