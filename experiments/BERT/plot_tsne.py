"""
JSON line scheme:

dict {
> 'linex_index' :
  '0'
> 'features' :
  list [
    dict {
      > 'layers' :
        list [
          dict {
            > 'index' :
              number [min: -4, mean: -2.5, max: -1]
            > 'values' :
              list [
                number [min: -12.17, mean: -0.02341, max: 4.246]
                sublist.lengths: 768
              ]
          }
          sublist.lengths: 4
        ]
      > 'token' :
        string
          'for' x 2
          19 other elements
    }
  ]
}


"""

import os
import json
import numpy as np
from MulticoreTSNE import MulticoreTSNE as TSNE
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def pool_sentence_embs(path, pooling_layer=-2, pooling_strategy='mean'):
    embs = []
    sents = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            dic = json.loads(line)
            token_embs = []
            tokens = []
            for index in range(len(dic['features'])): #index is word in sent
                token_embs.append(dic['features'][index]['layers'][pooling_layer]['values'])
                tokens.append(dic['features'][index]['token'])
            sents.append(" ".join(tokens))
            token_embs = np.asarray(token_embs) #length of sentence X hidden dimension 768
            if pooling_strategy == "mean":
                embs.append(token_embs.mean(0))

        embs = np.asarray(embs)
        print(embs.shape)
        print (sents)
    return embs
            # sent = dic[]

def main(path):
    embs = pool_sentence_embs(path)
    print("Dimension", embs.shape)
    # target = [0 for i in range(embs.shape[0])]
    target = [1., 0., 0., 1., 1., 1., 0., 1., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 0., 1.] + [0. for i in range(22)]
    print(len(target))
    embeddings = TSNE(n_jobs=4, random_state=1).fit_transform(embs) #number sentence X dimension
    vis_x = embeddings[:, 0]
    vis_y = embeddings[:, 1]
    plt.scatter(vis_x, vis_y, c=target, cmap=ListedColormap(["blue", "red"]), marker='.', s=50)
    plt.title("BERT_tsne (red=A1, blue=other)")
    # plt.colorbar(ticks=range(10))
    # plt.clim(-0.5, 9.5)
    plt.show()

if __name__ == '__main__':
    main('BERT_feature_extraction.json')