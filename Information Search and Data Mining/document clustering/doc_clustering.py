import pandas as pd
from sklearn.cluster import KMeans
import math

document_vector = [0]
similarity_metrics = [0]

def set_document_vector():
    global document_vector
    train = open('example1/train.dat', 'r')
    docvec = open('document_vector.dat', 'w')
    count = 0
    for line in train: break # first line of train.dat is a comment
    for line in train:
        # skip label and split elements of vector
        one_doc_vec_elem_list = line.split(' ', 1)[1].split(' ')
        one_document_vector = [0] * 9948 # 9947 is number of words
        for vector_element_string in one_doc_vec_elem_list:
            docvec.write(vector_element_string + ' ')
            vector_element = vector_element_string.split(':')
            # vector_element[0] is feature, and vector_element[1] is value
            one_document_vector[int(vector_element[0])] = float(vector_element[1])
        # set a document vector
        document_vector.append(one_document_vector)
        count += 1
        if count == 200: break
    train.close()
    docvec.close()


def set_similarity_metrics():
    global document_vector, similarity_metrics
    f = open('similarity_metrics.txt', 'w')
    cosine_similarity = [0] * 201
    doc_id = 1
    for vectorA in document_vector[1:]:
        sum_square_of_A, index = 0, 1
        for elem in vectorA:
            sum_square_of_A += elem * elem
        for vectorB in document_vector[1:]:
            sum_square_of_B, sum_of_AxB = 0, 0
            for i, (elemofA, elemofB) in enumerate(zip(vectorA, vectorB)):
                sum_square_of_B += elemofB * elemofB
                sum_of_AxB += elemofA * elemofB
            root_sum_square_of_B = math.sqrt(sum_square_of_B)
            cosine_similarity[index] = sum_of_AxB / \
                            (math.sqrt(sum_square_of_A) * math.sqrt(sum_square_of_B))
            f.write(str(index) + ':' + str(cosine_similarity[index]) + ' ')
            index += 1
        similarity_metrics.append(cosine_similarity)
        cosine_similarity = [0] * 201
        doc_id += 1
        f.write('\n')
    f.close()

def document_clustering(num_clusters):
    df = pd.DataFrame(columns=tuple(range(200)))
    for i in range(200):
        df.loc[i] = similarity_metrics[i+1][1:]
    data_values = df.values
    kmeans = KMeans(n_clusters=num_clusters).fit(data_values)
    df['cluster_id'] = kmeans.labels_
    cluster_list = list(range(num_clusters))

    with open('clustering_result.txt', 'w') as f:
        f.write('number of clusters : ' + str(num_clusters) + '\n')
        print('number of clusters :', num_clusters)
        for id in range(num_clusters):
            doc_id_list = df[df['cluster_id'] == id].index.values.tolist()
            f.write('cluster ' + str(id) + ' : ' + str(doc_id_list) + '\n')
            print('cluster', str(id), ':', str(doc_id_list))

if __name__ == '__main__':
    set_document_vector()
    set_similarity_metrics()
    document_clustering(5)
