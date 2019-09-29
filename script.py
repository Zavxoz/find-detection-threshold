class DictOfObjects():
    def __init__(self):
        import collections
        self.objects = collections.defaultdict(lambda: [0, 0, 0])

    def __getitem__(self, item):
        return self.objects[item]

    def tp(self, name):
        self[name][0] += 1

    def fp(self, name):
        self[name][1] += 1

    def fn(self, name):
        self[name][2] += 1

    def calculate_score(self):
        dict_with_scores = {}
        for i in self.objects:
            statistic = self.objects[i]
            precision = statistic[0]/(statistic[0] + statistic[1])
            recall = statistic[0]/(statistic[0] + statistic[2])
            score = 2 * precision * recall / (precision + recall)
            dict_with_scores[i] = score
        return dict_with_scores


def main():
    classes = DictOfObjects()
    processing(classes)
    print(classes.calculate_score())


def processing(classes):
    with open('detection_val_log.txt', "r") as f:
        for i in f.readlines():
            tmp = i.split('--')
            true_objects = tmp[0]
            detected_object = tmp[1][:-2]
            dict_of_true = make_dict(true_objects)
            dict_of_detected = make_dict(detected_object)
            analyze(classes, dict_of_true, dict_of_detected)


def make_dict(objects):
    if not objects:
        return {}
    tmp_list = objects.split(';')
    tmp_list = (i.split(',') for i in tmp_list)
    import collections
    dict_of_data = {}
    for i in tmp_list:
        dict_of_data[i[0]] = [int(j) for j in i[1:5]]
    return dict_of_data


def analyze(classes, dict_of_true, dict_of_detected):
    keys = tuple(dict_of_true.keys())
    for i in keys:
        if i in dict_of_detected.keys():
            if iou(dict_of_true.pop(i), dict_of_detected.pop(i)) > 0.5:
                classes.tp(i)
            else:
                classes.fp(i)
    if len(dict_of_true) != 0:
        for i in dict_of_true.keys():
            classes.fn(i)
    if len(dict_of_detected) != 0:
        for i in dict_of_detected.keys():
            classes.fp(i)


def iou(box_a, box_b):
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])
    
    inter_area = max(0, x_b - x_a + 1) * max(0, y_b - y_a + 1)
    box_a_area = (box_a[2] - box_a[0] + 1) * (box_a[3] - box_a[1] + 1)
    box_b_area = (box_b[2] - box_b[0] + 1) * (box_b[3] - box_b[1] + 1)

    iou = inter_area / (box_a_area + box_b_area - inter_area)
    return iou


if __name__ == "__main__":
    main()
