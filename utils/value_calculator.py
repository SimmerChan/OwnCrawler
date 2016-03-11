
def value_calculator(anchor_text, l1, l2):
    value = 0
    for w1 in l1:
        if anchor_text.find(w1) != -1:
            value += 1

    for w2 in l2:
        if anchor_text.find(w2) != -1:
            value += 1
    return value
