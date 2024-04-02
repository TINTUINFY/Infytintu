class csvWrapper():
    
    def __init__(self, file):
        self.file = file

    def read_csv(self):  
        with open(self.file, "r") as csvfile:
            info = csvfile.readlines()
            result = ' '.join([str(elem) for elem in info])
            result = ''.join(result.splitlines())
        return result
