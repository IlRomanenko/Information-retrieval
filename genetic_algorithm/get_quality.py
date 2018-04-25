import numpy as np

def evaluate_model(model, query_characteristics):
    values = model.calc(*query_characteristics[2])
    result = np.zeros(query_characteristics[0].shape[0])
    for i, pos in enumerate(query_characteristics[1]):
        result[pos] += values[i]

    return np.array([query_characteristics[0], result])

def evaluate_quality(doc_weights, doc_target_mask):
    
    sort_indexes = np.argsort(doc_weights)
    ranksForRetrievedDocs = doc_target_mask[:, sort_indexes]
    
    cumRanksForRetrievedDocs = np.cumsum(ranksForRetrievedDocs)
    cutOffPrecision = cumRanksForRetrievedDocs / np.arange(1, ranksForRetrievedDocs.shape[0] + 1)
    qualValue = np.sum(cutOffPrecision * ranksForRetrievedDocs) / doc_target_mask.shape[0]
    
    return qualValue

def get_quality(model, queries):

    vec_quality = []
    for i, query_characteristics in enumerate(queries):
        doc_weights = np.zeros(query_characteristics[1].shape[0])

        for word_characteristics in query_characteristics[0]:
            doc_weights += model.calc(*word_characteristics)

        quality = evaluate_quality(doc_weights, query_characteristics[1])
        vec_quality.append(quality)
    
    #print(np.sum(np.round(vec_quality, 4)))

    quality = np.sum(vec_quality)

    # TODO add regularization 
    return quality