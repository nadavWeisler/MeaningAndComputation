
import gensim
import pandas as pd
import scipy as sp

print("start")

# Exports data from corpus
sentences, cur_sent = list(), list()
with open('./wackypedia_en1.words10.20Mwords') as f:
    for line in f:
        line = line.strip()
        if line == '</s>':
            sentences.append(cur_sent)
            cur_sent = list()
        elif line != '<s>' and not line.startswith('<text') and not line.startswith('</text'):
            cur_sent.append(line.split('\t')[0])

print("Read corpus")

# Builds the models
model_big_ten = gensim.models.Word2Vec(
    sentences, min_count=5, window=1, vector_size=10)
model_small_ten = gensim.models.Word2Vec(
    sentences, min_count=5, window=10, vector_size=10)

model_big_five = gensim.models.Word2Vec(
    sentences, min_count=5, window=1, vector_size=500)
model_small_five = gensim.models.Word2Vec(
    sentences, min_count=5, window=10, vector_size=500)

models = [model_big_ten, model_big_five, model_small_ten, model_small_five]

print("Model built")

# Makes the similarity lists
words = pd.read_csv('./SimLex-999/SimLex-999.txt', delimiter='\t')
pairs = list(zip(words['word1'], words['word2']))
golden_sim = words['SimLex999']
results = [[], [], [], []]
for j in range(len(models)):
    for i in range(len(pairs)):
        try:
            similarity = models[j].wv.similarity(pairs[i][0], pairs[i][1])
        except KeyError:
            similarity = 0
        finally:
            results[j].append(similarity)
print("done5")

cor_results = []
golden_sim = words['SimLex999']
for result in results:
    sim_res = sp.stats.spearmanr(result, golden_sim)
    cor_results.append(sim_res)

f = open("corrFile.txt","w+")
f.writelines(cor_results)
print(cor_results)