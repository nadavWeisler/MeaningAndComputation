#	left
#	left -> to	left -> side
#	left -> from	left -> turn

import pandas as pd
import math

WORD = "left"
SEED_COLLOCATIONS = {"A": ["to", "from"], "B": ["side", "hand"]}

FREQUENCY_THRESHOLD = 50  # TODO: FIND OUT WHAT TO SET HERE, FOR NOW IT'S RANDOM
SCORE_THRESHOLD = 1  # TODO: FIND OUT WHAT TO SET HERE, FOR NOW IT'S RANDOM

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
			current_sentence = ""
		elif is_in_sentence:
			current_sentence += line
			current_sentence += " "
	return pd.DataFrame(result)


def get_word_frequency(word):
	file = open("./corpus_ex1.freq_list", "r")
	invalid_word = -1
	for line in file:
		line_data = line.split()
		if line_data[0] == word:
			return line_data[1]
	return invalid_word


def classify_sense(sentence, word, window_size, collocations):
	result = False
	try:
		words = sentence.split()
		word_index = words.index(word)
		found_words = []
		new_collocations = []
		a_counter = 0
		b_counter = 0
		for index in range(1, window_size + 1):
			if word_index - index >= 0:
				found_words.append(words[word_index - index])
			if word_index + index < len(words):
				found_words.append(words[word_index + index])
		for collocation in found_words:
			if collocation in collocations["A"]:
				a_counter += 1
			if collocation in collocations["B"]:
				b_counter += 1
			if collocation not in collocations["A"] and collocation not in collocations["B"]:
				new_collocations.append(collocation)
		if a_counter != b_counter:
			result = "A" if a_counter > b_counter else "B"
			raw_collocations[result] += new_collocations
		return result
	except:
		return result


def split_raw_collocations():
	a_collocations = pd.DataFrame(raw_collocations["A"], columns=["collocation"])
	b_collocations = pd.DataFrame(raw_collocations["B"], columns=["collocation"])
	a_collocations = a_collocations['collocation'].value_counts().rename_axis('collocation').reset_index(name='counts')
	b_collocations = b_collocations['collocation'].value_counts().rename_axis('collocation').reset_index(name='counts')
	return a_collocations, b_collocations


def calculate_probability(num_of_instances_with_sense, total_instances):
	return num_of_instances_with_sense / total_instances


def get_candidates(collocation_to_check, other_collocation):
	candidates = {"Candidates": [], "Scores": [], "Frequency": []}
	for row in collocation_to_check.iterrows():
		candidate = row[1]["collocation"]
		instance_with_check = row[1]["counts"]
		try:
			instance_with_other = other_collocation.loc[other_collocation['collocation'] == candidate, "counts"].iloc[0]
			total_instances = instance_with_check + instance_with_other
			candidate_score = math.log((calculate_probability(instance_with_check,
															  total_instances) / calculate_probability(
				instance_with_other, total_instances)))
			candidates["Candidates"].append(candidate)
			candidates["Scores"].append(candidate_score)
			candidates["Frequency"].append(get_word_frequency(candidate))
		except IndexError:
			# TODO: What to do once a collocation is in one index?
			continue
	return pd.DataFrame(candidates).sort_values(by=['Scores'], ascending=False)


res = extract_sentences("./corpus_ex1", WORD, SEED_COLLOCATIONS)
print_data("NUM OF SENTENCES PER SMELL", res.groupby('sense').count())
a_collocations, b_collocations = split_raw_collocations()
print_data("A COLLOCATIONS", len(a_collocations.index))
print_data("B COLLOCATIONS", len(b_collocations.index))
a_candidates = get_candidates(a_collocations, b_collocations)
b_candidates = get_candidates(b_collocations, a_collocations)
print_data("TOP 5 SENSE A CANDIDATES", a_candidates.head(5))
print_data("TOP 5 SENSE B CANDIDATES", b_candidates.head(5))

# TODO: STEPS 4.2, 5 and 6 :)
