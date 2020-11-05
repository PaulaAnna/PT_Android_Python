import pandas as pd
import os
import re

class CsvCreator:

    def __init__(self, path_data, frameworks=['Android-flutter', 'Android-native', 'Android-react', 'Android-ionic']):
      self.PATH_DIR = path_data
      self.FRAMEWORKS = frameworks

    def find_shortest(self):
        minimum = 100
        for fw in self.FRAMEWORKS:
            for subdir, dirs, files in os.walk(os.path.join(self.PATH_DIR + fw + '/')):
                for filename in files:
                    if filename.endswith('.txt'):
                        with open(os.path.join(self.PATH_DIR + fw + '/' + filename), 'r') as f:
                            lines = f.readlines()
                            if len(lines) < minimum:
                                minimum = len(lines)
        print('Minimum: {}'.format(minimum))
        return minimum

    def remove_first_two_rows(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            lines = lines[2:]
        
        with open(file_path, "w") as f:
            for line in lines:
                f.write(line)

    def create_df(self, file_path, nr_rows):
        df = pd.read_fwf(file_path, header=None)
        df = df.drop(df.index[nr_rows:])
        print(df.shape)
        print(df.head(2))
        cpu = df.drop([0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], axis=1)
        mem = df.drop([0,1,2,4,5,6,7,8,9,10,11,12,13,14,15], axis=1)
        return cpu, mem

    def create_df_new(self, file_path, nr_rows):
        df_list = []
        print(file_path)
        with open(file_path) as f:
            for line in f:
                # remove whitespace at the start and the newline at the end
                line = line.strip()
                # split each column on whitespace
                columns = re.split('\s+', line, maxsplit=15)
                df_list.append(columns)

        df = pd.DataFrame(df_list)
        df = df.drop(df.index[nr_rows:])
        print(df.shape)
        print(df.head(2))

        cpu = df.drop([0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], axis=1)
        mem = df.drop([0,1,2,4,5,6,7,8,9,10,11,12,13,14,15], axis=1)
        return cpu, mem

    def create_csv(self):
        dfs = {}
        for fw in self.FRAMEWORKS:
            dfs[fw + '-cpu'] = pd.DataFrame()
            dfs[fw + '-mem'] = pd.DataFrame()

        nr_rows = self.find_shortest() - 2
        for fw in self.FRAMEWORKS:
            for subdir, dirs, files in os.walk(os.path.join(self.PATH_DIR + fw + '/')):
                for filename in files:
                    print(filename)
                    if filename.endswith('.txt'):
                        file_path = os.path.join(self.PATH_DIR + fw + '/' + filename)
                        # Erste beide Zeilen mit Header loeschen
                        self.remove_first_two_rows(file_path)
                        df_cpu, df_mem = self.create_df_new(file_path, nr_rows)
                        dfs[fw + '-cpu'] = pd.concat([dfs[fw + '-cpu'],(df_cpu)], axis=1)
                        dfs[fw + '-mem'] = pd.concat([dfs[fw + '-mem'],(df_mem)], axis=1)
                    # TXT Datei nach Auswertung loeschen
                    # os.remove(file_path)

        for key, df in dfs.items():  
            df.to_csv (os.path.join(self.PATH_DIR, 'final-' + key + '.csv'), index=None, header=False)