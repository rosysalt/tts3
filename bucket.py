class Bucket():
    # default value
    hash_size = 1

    def __init__(self, hash_size, ids, checksum_values):
        self.hash_size = hash_size
        self.checksum_values = dict()

        for (index, value) in enumerate(checksum_values):
            self.checksum_values[ids[index]] = value

        self.hash_map = dict()

        for i in range(hash_size):
            self.hash_map[i] = []

        for (index, checksum) in enumerate(checksum_values):
            self.add(ids[index], checksum)

    def add(self, name, value):
        hash_value = value % self.hash_size
        self.hash_map[hash_value].append(name)

    def get_bucket(self, hash_value):
        return self.hash_map[hash_value]

    def get_duplicated_hash_value(self):
        """
        return: [
                    [t1, t4, t7], # t1 t4 t7 might be duplicated documents
                    [t2, t8]
                ]
        """
        duplicated_doc_list = []
        for values in self.hash_map.values():
            if len(values) > 1:
                duplicated_doc_list.append(values)

        return duplicated_doc_list

    def get_duplicated_checksum_doc_list(self):
        duplicated_hash_value_doc_list = self.get_duplicated_hash_value()

        duplicated_checksum_doc_list = []

        for duplicated_values in duplicated_hash_value_doc_list:
            checksum_list = self.get_checksum_for_list(duplicated_values)

            count_checksum_list = [checksum_list.count(i) for i in checksum_list]

            new_duplicated_values = []
            for (index, count) in enumerate(count_checksum_list):
                if count > 1:
                    new_duplicated_values.append(duplicated_values[index])

            if len(new_duplicated_values) > 1:
                for i in range(len(new_duplicated_values) - 1):
                    for j in range(1, len(new_duplicated_values)):
                        news_id_1 = new_duplicated_values[i]
                        news_id_2 = new_duplicated_values[j]

                        duplicated_checksum_doc_list.append((news_id_1, news_id_2))

        return duplicated_checksum_doc_list

    def get_checksum_for_list(self, list):
        checksum_list = []
        for item in list:
            checksum_list.append(self.checksum_values[item])

        return checksum_list
