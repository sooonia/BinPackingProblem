import pandas as pd


def smart_packer(items, num_batches):

    batches = [[] for _ in range(num_batches) ]
    weights = [0 for _ in range(num_batches) ]
    items.sort_values(by='WEIGHT', ascending='FALSE')

    for ix, row in items.iterrows():
        batch = weights.index(min(weights))
        weights[batch] += row.WEIGHT
        batches[batch].append(row.ID)
    return batches, weights

if __name__ == '__main__':
    items = pd.read_csv('test_data_GA.csv')
    items.ID = items.ID.astype(str)
    num_batches = 4
    batches, weights = smart_packer(items, num_batches)
    print("DONE")

