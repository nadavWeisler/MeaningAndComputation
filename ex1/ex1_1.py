import random

import pandas as pd
import math

WORD = "rock"
SEED_COLLOCATIONS = {"A": ["music", "band"], "B": ["climbing", "large"]}


FREQUENCY_THRESHOLD = 2
SCORE_THRESHOLD = 1

raw_collocations = {"A": [], "B": []}


def print_data(title, data):
	separator = ""
	for i in range(len(title)):
		separator += "_"
	print(separator)
	print(title)
	print(separator)
	print(data)
	print(separator)


def extract_sentences(path, word, collocations):
	file = open(path, "r")
	result = dict()
	left_sentences = dict()
	left_sentences["sentence"] = []
	result["sentence"] = []
	result["sense"] = []
	current_sentence = ""
	is_in_sentence = False
	for line in file:
		line = line.strip()
		if line.startswith("<text") or line == "</text>":
			continue
		if line == "<s>":
			is_in_sentence = True
		elif line == "</s>":
			is_in_sentence = False
			if " " + word + " " in current_sentence:
				sense = classify_sense(current_sentence, word, 2, collocations)
				if (sense):
					result["sentence"].append(current_sentence)
					result["sense"].append(sense)
				else:
					left_sentences["sentence"].append(current_sentence)
			current_sentence = ""
		elif is_in_sentence:
			current_sentence += line
			current_sentence += " "
	return pd.DataFrame(result), pd.DataFrame(left_sentences)


def get_word_frequency(word, sense_sentences):
	frequency = 0
	for row in sense_sentences.iterrows():
		sentence = row[1]["sentence"]
		words = sentence.split()
		for instance in words:
			if instance.lower() == word.lower():
				frequency += 1
	return frequency


def classify_sense(sentence, word, window_size, collocations):
	result = False
	try:
		words = sentence.split()
		word_index = words.index(word)
		found_words = []
		new_collocations = []
		a_sense = False
		b_sense = False
		for index in range(1, window_size + 1):
			if word_index - index >= 0 and len(words[word_index - index]) > 1:
				found_words.append(words[word_index - index])
			if word_index + index < len(words) and len(words[word_index + index]) > 1:
				found_words.append(words[word_index + index])
		for collocation in found_words:
			collocation = collocation.lower()
			if collocation in collocations["A"]:
				a_sense = True
			if collocation in collocations["B"]:
				b_sense = True
			if collocation not in collocations["A"] and collocation not in collocations["B"]:
				new_collocations.append(collocation.lower())
		if a_sense and not b_sense:
			result = "A"
			raw_collocations["A"] += new_collocations
		elif b_sense and not a_sense:
			result = "B"
			raw_collocations["B"] += new_collocations
		return result
	except:
		return result


def get_instances_around(word, collocation, a_collocations, b_collocations, unclassified, window_size):
	try:
		a_instances = a_collocations.loc[a_collocations['collocation'] == collocation, "counts"].iloc[0]
	except:
		a_instances = 0
	try:
		b_instances = b_collocations.loc[b_collocations['collocation'] == collocation, "counts"].iloc[0]
	except:
		b_instances = 0
	unclassified_instances = 0
	for row in unclassified.iterrows():
		sentence = row[1]["sentence"]
		words = sentence.split()
		word_index = words.index(word)
		found_words = []
		for index in range(1, window_size + 1):
			if word_index - index >= 0:
				found_words.append(words[word_index - index])
			if word_index + index < len(words):
				found_words.append(words[word_index + index])
		for found_word in found_words:
			if collocation == found_word:
				unclassified_instances += 1
	return a_instances, b_instances, a_instances + b_instances + unclassified_instances



def split_raw_collocations():
	filtered_a = [item for item in raw_collocations["A"] if item not in raw_collocations["B"]]
	filtered_b = [item for item in raw_collocations["B"] if item not in raw_collocations["A"]]
	a_collocations = pd.DataFrame(filtered_a, columns=["collocation"])
	b_collocations = pd.DataFrame(filtered_b, columns=["collocation"])
	a_collocations = a_collocations['collocation'].value_counts().rename_axis('collocation').reset_index(name='counts')
	b_collocations = b_collocations['collocation'].value_counts().rename_axis('collocation').reset_index(name='counts')
	return a_collocations, b_collocations


def calculate_probability(num_of_instances_with_sense, total_instances):
	return num_of_instances_with_sense / total_instances


def get_candidates(collocation_to_check, other_collocation, unclassified_sentences, sense_sentences):
	candidates = {"Candidates": [], "Scores": [], "Frequency": []}
	for row in collocation_to_check.iterrows():
		candidate = row[1]["collocation"]
		try:
			instance_with_check, instance_with_other, total_instances = get_instances_around(WORD, candidate, collocation_to_check, other_collocation, unclassified_sentences, 2)
			prob_1 = calculate_probability(instance_with_check, total_instances)
			prob_2 = calculate_probability(instance_with_other, total_instances)
			if prob_2 != 0:
				candidate_score = abs(math.log(prob_1 / prob_2))
			elif prob_1 != 0:
				candidate_score = abs(math.log(prob_1))
			else:
				candidate_score = 0
			frequency = get_word_frequency(candidate, sense_sentences)
			if candidate_score >= SCORE_THRESHOLD and frequency >= FREQUENCY_THRESHOLD:
				candidates["Candidates"].append(candidate)
				candidates["Scores"].append(candidate_score)
				candidates["Frequency"].append(frequency)
		except IndexError:
			continue
	return pd.DataFrame(candidates).sort_values(by=['Scores'], ascending=False)


def get_sentences_from_top(top_list, sentences_list):
	sentences = []
	to_iter = sentences_list["sentence"].tolist()
	random.shuffle(to_iter)
	for sentence in to_iter:
		words = sentence.split()
		for word in words:
			if len(sentences) == 5:
				break
			if word in top_list and sentence not in sentences:
				sentences.append(sentence)
				continue
		if len(sentences) == 5:
			break
	return sentences





classified, unclassified = extract_sentences("./corpus_ex1", WORD, SEED_COLLOCATIONS)
print_data("NUM OF SENTENCES PER SMELL", classified.groupby('sense').count())
print_data("UNCLASSIFIED", len(unclassified.index))
a_collocations, b_collocations = split_raw_collocations()
print_data("A COLLOCATIONS", len(a_collocations.index))
print_data("B COLLOCATIONS", len(b_collocations.index))
print("GETTING CANDIDATES FOR A")
a_candidates = get_candidates(a_collocations, b_collocations, unclassified, classified.loc[classified['sense'] == "A"])
print("GETTING CANDIDATES FOR B")
b_candidates = get_candidates(b_collocations, a_collocations, unclassified, classified.loc[classified['sense'] == "B"])
top_5_a = a_candidates.head(5)
top_5_b = b_candidates.head(5)
print_data("TOP 10 SENSE A CANDIDATES", top_5_a)
print_data("TOP 10 SENSE B CANDIDATES", top_5_b)
a_sentences = pd.DataFrame(get_sentences_from_top(top_5_a["Candidates"].tolist(), unclassified), columns=['Sentences'])
b_sentences = pd.DataFrame(get_sentences_from_top(top_5_b["Candidates"].tolist(), unclassified), columns=['Sentences'])

print_data("A SENTENCES", a_sentences)
print_data("B SENTENCES", b_sentences)
