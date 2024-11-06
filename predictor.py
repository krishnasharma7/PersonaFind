model = None
np = None

# Import dependencies and load model if not loaded already
def load_dependencies():
    global model, np
    if model is None:
        from absl import logging
        import tensorflow as tf
        import tensorflow_hub as hub
        import numpy as np
        import os
        import re

        # Model input
        module_url = "C:\\Users\\krish\\OneDrive\\Desktop\\Projects\\Mini-Project\\universal-sentence-encoder_4"
        model = hub.load(module_url)
        np = np

def embed(input):
    # Ensure model is loaded
    load_dependencies()
    return model(input)


class TextDataProcessor:
    def __init__(self):
        pass
    
    def extract_text_data(self, filename):
        topic_content_dict = {}

        with open(filename, 'r') as f:
            for line in f:
                topic_summary_label = line.rsplit(':', 1)
                topic = topic_summary_label[0].strip()
                summary_label = topic_summary_label[1].rsplit("(", 1)
                summary = summary_label[0].strip()
                label = int(summary_label[1].rsplit(')')[0])
                topic_content_dict[topic] = [summary, label]

        return topic_content_dict

    def extract_embeddings(self, dictionary):
        topic_embedding_dict = {}
        embeddings = []

        for summary_label in dictionary:
            embeddings.append(dictionary[summary_label][0])

        for embedding, summary_label in zip(embeddings, dictionary):
            temp_list = [embedding]
            topic_embedding_dict[summary_label] = np.asarray(embed(temp_list))

        return topic_embedding_dict

    def input_similarity_cosine(self, prompt, dictionary):
        topic_similarity = {}
        prompt_list = [prompt]
        prompt_embed = np.asarray(embed(prompt_list))
        for topic in dictionary:
            cos_sim = np.dot(prompt_embed, dictionary[topic].T)
            topic_similarity[topic] = cos_sim

        return topic_similarity

    def summary_type(self, dictionary_1, dictionary_2, n):
        top_result_sim = 0
        sorted_list = sorted(dictionary_1.items(), key=lambda item: item[1], reverse=True)
        for i, topic in enumerate(sorted_list[:n]):
            top_result_sim += float(sorted_list[i][1])
        top_result_sim /= n
        if top_result_sim >= 0.1:
            return int(dictionary_2[sorted_list[0][0]][1])
        else:
            return  1# Call Pattern recognition problem 

    def process_input(self, filename, prompt, n):
         # Step 1: Extract text data from file
         topic_content_dict = self.extract_text_data(filename)
    
         # Step 2: Extract embeddings for the summaries
         topic_embedding_dict = self.extract_embeddings(topic_content_dict)
    
         # Step 3: Calculate similarity between prompt and summaries
         similarity_scores = self.input_similarity_cosine(prompt, topic_embedding_dict)
    
         # Step 4: Determine summary type based on similarity scores
         summary_type_label = self.summary_type(similarity_scores, topic_content_dict, n)
    
         return summary_type_label
    
    def append_summary(self, prompt, summary, label, filename):
         data = f"\n{prompt}: {summary} ({label})"
         with open(filename, "a") as f:
             f.write(data)
             