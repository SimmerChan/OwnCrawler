
def value_calculator_url(anchor_text, l1, l2):
    """
    calculate the value of url based on the anchor_text
    :param anchor_text:
    :param l1:
    :param l2:
    :return:
    """
    value = 0
    k1 = False
    k2 = False
    for w1 in l1:
        if anchor_text.find(w1) != -1:
            value += 1
            k1 = True

    for w2 in l2:
        if anchor_text.find(w2) != -1:
            value += 1
            k2 = True

    if k1 is True and k2 is True:
        value += 2
    return value


def value_calculator_cluster(clusters_info):
    """
    calculate the value of cluster based on the cluster's area
    :param clusters_info:
    :return:
    """
    clusters_info_sorted_by_area = sorted(clusters_info, key=lambda item: item['area'], reverse=True)
    length = len(clusters_info_sorted_by_area)
    for info in clusters_info_sorted_by_area:
        info['value'] = 1
    if length > 5:
        clusters_info_sorted_by_area[0]['value'] = 3
        clusters_info_sorted_by_area[1]['value'] = 2
    else:
        clusters_info_sorted_by_area[0]['value'] = 2
    return clusters_info_sorted_by_area
