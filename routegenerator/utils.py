def enable_stop_nodes(stop_nodes):
    for n in stop_nodes:
        n.enable()


def all_nodes_disabled(stop_nodes):
    return get_num_disabled(stop_nodes) == len(stop_nodes)


def get_num_disabled(stop_nodes):
    return sum(1 for n in stop_nodes if not n.enabled)


# TODO: Check if you can use scipy.spatial.distance.euclidean instead
def euclidean(x, y):
    sum_squared = 0.0
    for i in range(len(x)):
        sum_squared += (x[i] - y[i]) ** 2

    return sum_squared ** 0.5
