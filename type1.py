from news import *

class Type1():
    def __init__(self, news, checksum, duplicated_list):
        self.news = news
        self.checksum = checksum
        self.duplicated_list = duplicated_list

        self.type1_doc = [] # [[t1, t2], [t3, t8]] ==> t1 is the same as t2, t3 is the same as t8

    def naive_compare(self):
        for duplicated_values in self.duplicated_list:
            checksum_list = self.get_checksum_for_list(duplicated_values)
            
            count_checksum_list = [checksum_list.count(i) for i in checksum_list]

            new_duplicated_values = []
            for (index, count) in enumerate(count_checksum_list):
                if count > 1:
                    new_duplicated_values.append(duplicated_values[index])
            
            # REFACTOR
            # this one can be improved by only comparing those documents with
            # the same checksum, instead of comparing all the documents left
            if len(new_duplicated_values) > 1:
                for i in range(len(new_duplicated_values) - 1):
                    for j in range(1, len(new_duplicated_values)):
                        news_id_1 = new_duplicated_values[i]
                        news_id_2 = new_duplicated_values[j]

                        # to make sure smaller news_id appear first
                        if news_id_1 > news_id_2:
                            temp = news_id_1
                            news_id_1 = news_id_2
                            news_id_2 = temp

                        result = self.news.compare(news_id_1, news_id_2)

                        if result:
                            self.type1_doc.append([news_id_1, news_id_2])

        return self.type1_doc

    def get_sorted_indices(self, array, reverse=False):
        return [i[0] for i in sorted(enumerate(array), reverse = reverse, key=lambda x:x[1])]

    def get_checksum_for_list(self, list):
        checksum_list = []
        for item in list:
            checksum_list.append(self.checksum[item])

        return checksum_list

