class Bucket():
    # default value
    hash_size = 1

    def __init__(self, hash_size):
        self.hash_size = hash_size
        self.hash_map = dict()

        for i in range(hash_size):
            self.hash_map[i] = []

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

