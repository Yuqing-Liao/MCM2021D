import numpy as np
from util import Excel, within_similarity
import collections

excel = Excel()
"""
sheet = excel.load_sheet("output/features_by_artist.xls")
d = collections.defaultdict()

for i in range(excel.__len__(sheet)):
    id = int(excel.read_by_row(sheet, i)[0])
    d[id] = i


feature = np.loadtxt(open("output/features_by_artist_.csv"),delimiter=",", skiprows=0)
print(feature.shape)
l = feature.shape[0]
influence_matrix = [[0 for _ in range(l)] for _ in range(l)]

sheet = excel.load_sheet("dataset/influence_data.xls")
for i in range(1, excel.__len__(sheet)):
    data = excel.read_by_row(sheet, i)
    inf_id, fol_id = int(data[0]), int(data[4])
    influence_matrix[d[inf_id]][d[fol_id]] = 1

sim, dists = within_similarity(feature, 'L1')
inf_sim = dists * influence_matrix
inf_sim = np.sum(inf_sim, axis=1) / np.sum(influence_matrix, axis=1)
non_influence_matrix = np.subtract(1, influence_matrix)
for i in range(l):
    non_influence_matrix[i][i] = 0
non_inf_sim = dists * non_influence_matrix
non_inf_sim = np.sum(non_inf_sim, axis=1) / np.sum(non_influence_matrix, axis=1)
np.save('inf_sim', inf_sim)
np.save('non_inf_sim', non_inf_sim)
"""
inf_sim = np.load("inf_sim.npy")
non_inf_sim = np.load("non_inf_sim.npy")
print(inf_sim)
print(np.sum(inf_sim < non_inf_sim), np.sum(inf_sim > non_inf_sim))
