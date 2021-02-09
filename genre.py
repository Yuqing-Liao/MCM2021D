from util import Excel, between_similarity, within_similarity
from heatmap import make_heatmap
import matplotlib.pyplot as plt
import collections
from artist import Influencer, Artist, Artist_Graph
import numpy as np
from print_numpy import write_numpy

class Genre:
    def __init__(self, name):
        self.name = name
        self.num_of_inf = 0
        self.num_of_artist = 0
        # self.in_inf = 0
        # self.out_inf = 0
        self.influencer_id = []
        self.artist_id = []
        self.feature_matrix = []
        self.similarity_matrix = None


class Genre_Graph():
    def __init__(self):
        self.excel = Excel()
        self.path = 'output/features_by_artist.xls'
        self.genres = collections.defaultdict()
        self.artists = _graph.influencers.copy()
        self.similarity_matrix = []
        self.pool = []
        self.distance = ['L1', 'L2', 'Minkowski']
        genre_data = self.excel.load_sheet(self.path)
        for i in range(1, self.excel.__len__(genre_data)):
            record = self.excel.read_by_row(genre_data, i)
            artist_id, artist_name, genre_name, feature = int(record[0]), record[1], \
                                                              record[2], record[3:]
            if feature[0] == 0:
                    continue
            if genre_name not in self.genres:
                self.genres[genre_name] = Genre(genre_name)
            if artist_id not in self.artists:
                self.artists[artist_id] = Artist(artist_id, artist_name, genre_name)
                self.genres[genre_name].num_of_inf += 1
                self.genres[genre_name].influencer_id.append(artist_id)
            self.genres[genre_name].num_of_artist += 1
            self.genres[genre_name].artist_id.append(artist_id)
            self.genres[genre_name].feature_matrix.append(feature)

    def cal_similarity(self):
        pool = []
        for g_name, g in self.genres.items():
            if g_name not in ['Children\'s', 'Avant-Garde', 'Unknown', 'Easy Listening', 'Comedy/Spoken']:
                pool.append((g_name, np.array(g.feature_matrix)))
        self.pool = pool
        l = len(pool)
        l2_matrix = [[None for _ in range(l)] for _ in range(l)]
        self.similarity_matrix = [[None for _ in range(l)] for _ in range(l)]
        for i in range(l):
            sim, self.genres[pool[i][0]].similarity_matrix = within_similarity(pool[i][1], self.distance[0])
            self.similarity_matrix[i][i] = sim
            write_numpy(self.genres[pool[i][0]].similarity_matrix, pool[i][0]+'.txt')
            for j in range(i+1, l):
                sim, l2_matrix[i][j] = between_similarity(pool[i][1], pool[j][1], self.distance[0])
                self.similarity_matrix[i][j] = self.similarity_matrix[j][i] = sim
                write_numpy(l2_matrix[i][j], pool[i][0]+'_to_'+pool[j][0]+'.txt')
        # self.print_similarity()


    def normalize(self):
        sim = np.array(self.similarity_matrix)
        # sim = np.log(np.divide(1, sim))
        sim = np.divide(1, sim)
        # sim = np.exp(-sim)
        max_s = np.max(sim, axis=1).reshape(-1, 1)
        min_s = np.min(sim, axis=1).reshape(-1, 1)
        sim = (sim - min_s) / (max_s - min_s)
        make_heatmap(sim, [i[0] for i in self.pool])
        self.similarity_matrix = sim.tolist()


if __name__ == '__main__':
    excel = Excel()
    global _genre, _graph
    _graph = Artist_Graph()
    _graph.cal_degree()
    _graph.cal_influence()
    _genre = Genre_Graph()

    # explore_jazz_musicians()
    #
    #_genre.cal_similarity()
    #_genre.normalize()
    #excel.output_similarity(_genre)
    #excel.output_genre(_genre.genres)
    #plt.show()


