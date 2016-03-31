from sklearn.cluster import DBSCAN  # Use scikit-learn to perform clustering
import numpy as np


# ElementList contains a line for each element we want to cluster with his top and left position,
#  width and eight and xpath


def find_all(xpath, pattern):
    index_list = []
    ix = xpath.find(pattern)
    while ix != -1:
        index_list.append(ix)
        ix = xpath.find(pattern, ix + 1)
    return index_list


def page_segmentation(elementlist):
    xpath_dict = set()  # Build a dictionary of XPATH of each element
    elements_used = list()

    for item in elementlist:
        path_split_idx = find_all(item["xpath"], "/")
        for idx in path_split_idx:
            xpath_dict.add(item["xpath"][:idx])

    xpath_dict = list(xpath_dict)

    # Build feature matrix with each element

    features = []  # Table will store features for each element to cluster
    for item in elementlist:
        # Keep only inside browser visual boundary
        # if item["left"] > 0 and item["top"] > 0 and (item["left"] + item["width"]) < 1366:
        if item["width"] != 0:
            visual_features = [item["left"], item["left"] + item["width"], item["top"], item["top"] + item["height"],
                               (item["left"] + item["left"] + item["width"]) / 2,
                               (item["top"] + item["top"] + item["height"]) / 2]

            dom_features = [0] * len(xpath_dict)  # using DOM parent presence as a feature. Default as 0
            path_split_idx = find_all(item["xpath"], "/")
            elements_used.append(item)

            for i, idx in enumerate(path_split_idx):
                # give an empirical 70 pixels distance weight to each level of the DOM (far from perfect implementation)
                dom_features[xpath_dict.index(item["xpath"][:idx])] = 800 / (i + 1)
            # create feature vector combining visual and DOM features
            features.append(visual_features + dom_features)

    try:

        features = np.asarray(features)  # Convert to numpy array to make DBSCAN work

        # DBSCAN is a good general clustering algorithm
        eps_value = 900  # maximum distance between clusters
        db = DBSCAN(eps=eps_value, min_samples=1, metric='cityblock').fit(features)

        # DBSCAN Algorithm returns a label for each vector of input array
        labels = db.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        clusters = [[] for i in range(n_clusters)]

        for i in range(0, len(labels)):
            n = labels[i]
            clusters[n].append(elements_used[i])

        # TODO del clusters whose number of elements is less than 3
        s_clusters = sorted(clusters, key=lambda item_len: len(item_len), reverse=True)
        clusters_in_use = list()

        for s in s_clusters:
            if len(s) > 1:
                clusters_in_use.append(s)
            else:
                break

        length_clusters_in_use = len(clusters_in_use)
        clusters_in_use_info = [{} for i in range(length_clusters_in_use)]
        average_top = list()
        total_center_y = 0
        total_center_x = 0
        total_area = 0

        for j in range(0, length_clusters_in_use):
            for e in clusters_in_use[j]:
                total_center_y += (e['height']+e['top']*2)/2
                total_area += e['height']*e['width']
                total_center_x += (e['width']+e['left']*2)/2

            length_clusters = len(clusters_in_use[j])
            average_top.append(total_center_y/length_clusters)
            clusters_in_use_info[j]['cluster'] = clusters_in_use[j]
            clusters_in_use_info[j]['area'] = total_area/length_clusters
            clusters_in_use_info[j]['centerX'] = round(total_center_x/length_clusters)
            clusters_in_use_info[j]['centerY'] = round(total_center_y/length_clusters)
            total_center_y = 0
            total_center_x = 0
            total_area = 0

        min_average_top = min(average_top)
        max_average_top = max(average_top)
        index_min_top = average_top.index(min_average_top)
        index_max_top = average_top.index(max_average_top)

        if index_max_top > index_min_top:
            clusters_in_use_info.pop(index_max_top)
            clusters_in_use_info.pop(index_min_top)
        else:
            clusters_in_use_info.pop(index_min_top)
            clusters_in_use_info.pop(index_max_top)

        # plot.clusters_plot(clusters_in_use, s_clusters, elements_used)
        return clusters_in_use_info

    except ValueError:
        return None

