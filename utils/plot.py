import matplotlib.pyplot as plt


def clusters_plot(clusters_in_use, s_clusters, elements_used):

    colors = ['#8faf3d', '#bb3ef5', '#8b4a00', '#d7d726', '#4455af', '#fcda9e', '#1dd7bd', '#dbb1a8', '#194c60',
              '#4614a7', '#3d8849', '#95cb3f', '#e1eef7', '#4ff6f8', '#331b89', '#746971', '#7ccc44', '#ab1a27',
              '#f4fc04', '#9330ea', '#0a8af9', '#7adcc9', '#3325ae', '#c9bb0a', '#36e060']

    max_left = sorted(elements_used, key=lambda item1: item1['left']).pop()['left']
    min_left = sorted(elements_used, key=lambda item1: item1['left'], reverse=True).pop()['left']
    max_top = sorted(elements_used, key=lambda item2: item2['top']).pop()['top']
    max_width = sorted(elements_used, key=lambda item3: item3['width']).pop()['width']

    figure = plt.figure()
    ax = figure.add_subplot(211)
    figure.subplots_adjust(top=0.85)

    for i in range(len(clusters_in_use)):
        for e in clusters_in_use[i]:
            ax.text(e['left'], e['top'], e['text'], style='italic',
                    bbox={'facecolor': colors[i], 'alpha': 0.5, 'pad': 1}, fontproperties='SimHei')

    ax.axis([min_left, max_left + max_width, 0, max_top])
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    ax.set_ylim(ax.get_ylim()[::-1])

    ax = figure.add_subplot(212)
    figure.subplots_adjust(top=0.85)

    for i in range(len(s_clusters)):
        for e in s_clusters[i]:
            ax.text(e['left'], e['top'], e['text'], style='italic',
                    bbox={'facecolor': colors[i], 'alpha': 0.5, 'pad': 1}, fontproperties='SimHei')

    ax.axis([min_left, max_left + max_width, 0, max_top])
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.show()
