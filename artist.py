import collections
import numpy as np
from util import Excel
from heatmap import make_heatmap
import matplotlib.pyplot as plt

MAX_SPAN = 80


class Influence():
    def __init__(self, p=0, e=0, t=0):
        self.Persistency = p
        self.Expandability = e
        self.Transitivity = t

    def cal(self):
        return self.Persistency + self.Expandability + self.Transitivity


class Artist():
    def __init__(self, id, name, genre, year=-1):
        self.id = id
        self.name = name
        self.year = year
        self.genre = genre
        self.features = [0 for _ in range(6)]
        self.num_of_work = 0


class Influencer(Artist):
    def __init__(self, id, name, genre):
        Artist.__init__(self, id, name, genre, year=-1)
        self.genre = genre
        self.edges = []
        self.indegree = 0
        self.outdegree = 0
        self.follower_within_genre = 0
        self.follower_between_genre = 0
        self.max_span = 0
        self.influence = 0

    def cal_outdegree(self):
        self.outdegree = len(self.edges)

    def cal_outdegree_genre(self):
        for e in self.edges:
            if e.is_same_genre:
                self.follower_within_genre += 1
            else:
                self.follower_between_genre += 1

    def cal_influence(self):
        for e in self.edges:
            self.influence += e.influence_coef.cal()

    def add_edge(self, e):
        self.edges.append(e)
        if e.time_span > self.max_span:
            self.max_span = e.time_span


class Edge():
    def __init__(self, influencer_id, follwer_id, follower_genre, influencer_genre, time_span):
        global _graph
        self.influencer_id = influencer_id
        self.follower_id = follwer_id
        self.follower_genre = follower_genre
        self.time_span = time_span
        self.influencer_genre = influencer_genre
        self.is_same_genre = (follower_genre == influencer_genre)
        self.influence_coef = None
        self.similarity = None

    def cal_influ_coef(self, _graph):
        # global _graph
        p = self.time_span / MAX_SPAN
        e = 0.5 if self.is_same_genre else 1
        t = 1 if self.follower_id in _graph.influencers else 0.5
        self.influence_coef = Influence(p, e, t)


class Artist_Graph():
    def __init__(self):
        self.excel = Excel()
        self.paths = ['dataset/influence_data.xls',
                      'dataset/data_by_year.xls',
                      'dataset/data_by_artist.xls',
                      'dataset/test.xls']
        self.influencers = collections.defaultdict()
        self.edges = []
        # [0: influencer_id, 1: influencer_name, 2: influencer_main_genre,
        #  3: influencer_active_start, 4: follower_id, 5: follower_name,
        #  6: follower_main_genre, 7: follower_active_start]
        # influence_data = self.excel.load_sheet(self.paths[-1])
        influence_data = self.excel.load_sheet(self.paths[0])
        last_record = [-1]
        for i in range(1, self.excel.__len__(influence_data)):
            record = self.excel.read_by_row(influence_data, i)
            influencer_id, influencer_name, influencer_main_genre, follower_id, \
            follwer_main_genre, time_span = int(record[0]), record[1], record[2], \
                                            int(record[4]), record[6], int(record[7] - record[3])
            e = Edge(influencer_id, follower_id, follwer_main_genre, influencer_main_genre, time_span)
            if influencer_id != last_record[0]:
                self.influencers[influencer_id] = (Influencer(influencer_id, influencer_name, influencer_main_genre))
            self.influencers[influencer_id].add_edge(e)
            self.edges.append(e)
            last_record = record

    def cal_indegree(self):
        for e in self.edges:
            if e.follower_id in self.influencers:
                self.influencers[e.follower_id].indegree += 1

    def cal_outdegree(self):
        for i in self.influencers:
            self.influencers[i].cal_outdegree()
            self.influencers[i].cal_outdegree_genre()

    def cal_degree(self):
        self.cal_indegree()
        self.cal_outdegree()

    def cal_influence(self):
        for e in self.edges:
            e.cal_influ_coef(self)
        for i in self.influencers:
            self.influencers[i].cal_influence()


def init_artists(excel):
    Artists = _graph.influencers.copy()
    path = 'dataset/influence_data.xls'
    artist_data = excel.load_sheet(path)
    for i in range(1, excel.__len__(artist_data)):
        record = excel.read_by_row(artist_data, i)
        name, id, genre = record[5], int(record[4]), record[6]
        if id not in Artists:
            Artists[id] = Artist(id, name, genre)
    return Artists


def cal_avg_feature(excel):
    global Artists
    path = ['output/features1_by_music.xls', 'output/features2_by_music.xls']
    no_exist = 0
    for i in range(2):
        sheet = excel.load_sheet(path[i])
        for r in range(1, excel.__len__(sheet)):
            data = excel.read_by_row(sheet, r)
            id_list, feature = data[0].strip("[]").split(", "), data[1:]
            for i in id_list:
                i = int(i)
                if i not in Artists:
                    no_exist += 1
                    continue
                for j in range(6):
                    Artists[i].features[j] += feature[j]
                    Artists[i].num_of_work += 1
    print(no_exist, "artists don't exist.")
    for id in Artists:
        if Artists[id].num_of_work == 0:
            print(id, "has no work!")
        else:
            for i in range(6):
                Artists[id].features[i] /= Artists[id].num_of_work


def cal_influence_matrix():
    global _graph
    genre_num = {'Religious': 0, 'Jazz': 1, 'Stage & Screen': 2, 'International': 3,
                 'Latin': 4, 'New Age': 5, 'Classical': 6,
                 'Electronic': 7, 'Folk': 8, 'Vocal': 9, 'Reggae': 10,
                 'Pop/Rock': 11, 'R&B;': 12, 'Blues': 13, 'Country': 14}
    influence_matrix = [[0 for _ in range(15)] for _ in range(15)]
    labels = ['Religious', 'Jazz', 'Stage & Screen', 'International',
              'Latin', 'New Age', 'Classical', 'Electronic', 'Folk',
              'Vocal', 'Reggae', 'Pop/Rock', 'R&B;', 'Blues', 'Country']
    for e in _graph.edges:
        if e.influencer_genre in genre_num and e.follower_genre in genre_num:
            x = genre_num[e.influencer_genre]
            y = genre_num[e.follower_genre]
            influence_matrix[x][y] += 1
    influence_matrix = np.array(influence_matrix)
    max_s = np.max(influence_matrix, axis=1).reshape(-1, 1)
    min_s = np.min(influence_matrix, axis=1).reshape(-1, 1)
    influence_matrix = (influence_matrix - min_s) / (max_s - min_s)
    make_heatmap(influence_matrix, labels)


if __name__ == '__main__':
    global _graph, Artists
    _graph = Artist_Graph()
    _graph.cal_degree()
    _graph.cal_influence()
    # cal_influence_matrix()
    # plt.show()
    excel = Excel()
    # Artists = init_artists(excel)
    # print(len(_graph.influencers))
    """
    for i in _graph.influencers:
        inf = _graph.influencers[i]
        print(i, inf.name, inf.indegree, inf.outdegree, inf.follower_within_genre, inf.follower_between_genre)
    """
    # excel.output_degrees(_graph.influencers)
    # excel.output_influence(_graph.influencers)
    # cal_avg_feature(excel)
    # excel.output_features(Artists)

