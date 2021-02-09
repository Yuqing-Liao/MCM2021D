import collections
from artist import _graph
from genre import _genre

def explore(id_list):
    followers = collections.defaultdict(int)
    group = []
    for id in id_list:
        # print(id, _genre.artists[id].name)
        for e in _graph.influencers[id].edges:
            if e.follower_id in _genre.artists or e.follower_id in _graph.influencers:
                # print(e.follower_id, _genre.artists[e.follower_id].name)
                followers[e.follower_id] += 1

                if not e.is_same_genre and e.follower_id not in group and\
                        e.follower_id in _graph.influencers and _graph.influencers[e.follower_id].influence>275:
                    print(_graph.influencers[id].name, '~~~>', _graph.influencers[e.follower_id].name, _graph.influencers[e.follower_id].genre)

    # sorted(followers.items(), key=lambda followers:followers[1])
    for id, f in followers.items():
        if id in id_list and followers[id] > 3:
            print("!!!!", id, _genre.artists[id].name, followers[id])
            group.append(id)
        elif id in id_list:
            print("!", id, _genre.artists[id].name, followers[id])
            group.append(id)
        elif followers[id] > 5:
            print(id, _genre.artists[id].name, followers[id])
            group.append(id)
    for id in id_list:
        if id not in followers and followers[id] == 0:
            print("discarding...", id, _genre.artists[id].name, followers[id])
    print(group)
    importance = [[],[],[],[],[]]
    for i in group:
        inf = _graph.influencers[i]
        if inf.influence > 200:
            importance[0].append(inf.name)
        elif inf.influence > 150:
            importance[1].append(inf.name)
        elif inf.influence > 100:
            importance[2].append(inf.name)
        elif inf.influence > 50:
            importance[3].append(inf.name)
        else:
            importance[4].append(inf.name)

    for i, im in enumerate(importance):
        print(i,":", im)

    for i in group:
        for e in _graph.influencers[i].edges:
            if e.follower_id in group:
                print(#i,
                    _graph.influencers[i].name,# e.follower_id,
                    "--->", _graph.influencers[e.follower_id].name)
    for i in group:
        for e in _graph.influencers[i].edges:
            if e.follower_id not in group:
                if e.follower_id in _genre.artists:
                    print(  # i,
                        _graph.influencers[i].name,  # e.follower_id,
                        "->", _genre.artists[e.follower_id].name)


def explore_jazz_musicians():
    jazz_id = [423829, 175553, 211758, 317093, 287604, 490416, 259529, 484396,
     805930, 764702, 378624, 640675, 957296, 9680,\
     94210,201760,742899]

    explore(jazz_id)
