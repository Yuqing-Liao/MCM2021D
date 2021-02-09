import xlrd
import xlwt
import numpy as np


class Excel():
    def load_sheet(self, path):
        return xlrd.open_workbook(path).sheets()[0]

    def __len__(self, sheet):
        return sheet.nrows

    def read_by_row(self, sheet, row):
        data = []
        for r in sheet.row(row):
            data.append(r.value)
        return data

    def read_by_column(self, sheet, col):
        data = []
        for c in sheet.col(col):
            data.append(c.value)
        return data

    def create_sheet(self):
        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet('sheet', cell_overwrite_ok=True)
        return book, sheet

    def write_by_row(self, sheet, row, data):
        for c, d in enumerate(data):
            sheet.write(row, c, d)

    def write_by_column(self, sheet, col, data):
        for r, d in enumerate(data):
            sheet.write(r+1, col, d)

    def write_by_cell(self, sheet, row, column, val):
        sheet.write(row, column, val)

    def save_sheet(self, book, filename):
        book.save('output/' + filename)

    def output_degrees(self, influencer_dict):
        book, sheet = self.create_sheet()
        for i, id in enumerate(influencer_dict):
            inf = influencer_dict[id]
            data = [inf.id, inf.name, inf.genre, inf.indegree, inf.outdegree, \
                    inf.follower_within_genre, inf.follower_between_genre]
            self.write_by_row(sheet, i + 1, data)
        self.save_sheet(book, 'degrees.xls')

    def output_influence(self, influencer_dict):
        book, sheet = self.create_sheet()
        for i, id in enumerate(influencer_dict):
            inf = influencer_dict[id]
            data = [inf.id, inf.name, inf.genre, inf.influence, inf.outdegree, \
                    inf.follower_within_genre, inf.follower_between_genre]
            self.write_by_row(sheet, i + 1, data)
        self.save_sheet(book, 'influence.xls')

    def output_features(self, artist_dict):
        book, sheet = self.create_sheet()
        for i, id in enumerate(artist_dict):
            a = artist_dict[id]
            data = [a.id, a.name, a.genre] + a.features
            self.write_by_row(sheet, i + 1, data)
        self.save_sheet(book, 'features_by_artist.xls')


    def output_genre(self, genre_dict):
        """
        for g_name in self.genres:
            print(g_name, self.genres[g_name].num_of_inf, self.genres[g_name].num_of_artist)
        """
        book, sheet = self.create_sheet()
        for i, (g_name, g) in enumerate(genre_dict.items()):
            self.write_by_cell(sheet, 0, i, g.name)
            self.write_by_column(sheet, i, g.artist_id)
        self.save_sheet(book, 'artists_by_genre.xls')

    def output_similarity(self, _genre):
        """
        for g_name in self.genres:
            print(g_name, self.genres[g_name].num_of_inf, self.genres[g_name].num_of_artist)
        """
        book, sheet = self.create_sheet()
        similarity = _genre.similarity_matrix
        pool = _genre.pool
        for i, g in enumerate(pool):
            self.write_by_cell(sheet, 0, i+1, g[0])
            self.write_by_cell(sheet, i+1, 0, g[0])
            for j in range(len(similarity)):
                self.write_by_cell(sheet, i+1, j+1, similarity[i][j])
        self.save_sheet(book, 'normalized_similarity_by_genre.xls')


def between_similarity(arr1, arr2, method):
    """
    k1, k2 = arr1.shape[0], arr2.shape[0]
    dists = np.multiply(np.dot(arr1, arr2.T), -2)
    sq1 = np.sum(np.square(arr1), axis=1, keepdims=True)
    sq2 = np.sum(np.square(arr2), axis=1)
    dists = np.add(dists, sq1)
    dists = np.add(dists, sq2)
    dists = np.sqrt(dists)
    return dists
    """
    k1, k2 = arr1.shape[0], arr2.shape[0]
    dists = np.zeros((k1, k2))
    for i in range(k1):
        if method == 'L2':
            dists[i] = np.sqrt(np.sum(np.square(arr2 - arr1[i]), axis=1))
        elif method == 'L1':
            dists[i] = np.sum(np.abs(arr2 - arr1[i]), axis=1)
    sim = dists.sum() / (k1 * k2)
    return sim, dists


def within_similarity(arr, method):
    sim = 0
    k = arr.shape[0]
    dists = np.zeros((k, k))
    for i in range(k):
        for j in range(i + 1, k):
            if method == 'L2':
                dists[i][j] = dists[j][i] = np.sqrt(np.power(arr[i] - arr[j], 2).sum())
            elif method == 'L1':
                dists[i][j] = dists[j][i] = np.sum(np.abs(arr[i] - arr[j]))
            sim += dists[i][j]
    sim /= i * (i - 1)
    sim *= 2
    return sim, dists


if __name__ == '__main__':
    """
    excel = Excel()
    path = 'dataset/influence_data.xls'
    sheet = excel.load_sheet(path)
    print(excel.read_by_row(sheet, 0))
    # print(excel.extract_by_column(path, 0))
    print(excel.__len__(sheet))
    """
