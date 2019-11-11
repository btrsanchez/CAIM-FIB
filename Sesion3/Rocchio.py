import argparse
import TFIDFViewer as tf

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

#python3 Rocchio.py --nrounds 1 --k 5 --R 5 --alpha 1 --beta 0.8 --index news --query toronto

def queryToDict(query):
        dic = {}
        for t in query:
                if "^" not in t:
                        dic[t] = 1
                else:
                        new = t.split("^")
                        dic[new[0]] = new[1]

        return dic

def dictToQuery(query):
        p = ""
        for t,w in query.items():

                strw = str(int(w))
                p += t+"^"+strw+" "
        return p

def calcTFIDFDic(query, docs, client, index):
        tfquery = {}

        for word,_ in query.items():
                tfquery[word] = 0

        for d in docs:
                doc_id = tf.search_file_by_path(client, index, d.path)
                doc_tw = tf.toTFIDF(client, index, doc_id)

                dtw = dict(doc_tw)

                for word,_ in query.items():
                    tfquery[word] += dtw[word]

        return tfquery


if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('--nrounds', default=None, type=int, help='number of applications of Rocchio’s rule')
        parser.add_argument('--k', default=None, type=int, help='number of top documents considered relevant')
        parser.add_argument('--R', default=None, type=int, help='maximum number of new terms to be kept in the new query')
        parser.add_argument('--alpha', default=None, type=float, help='weights in the Rocchio rule')
        parser.add_argument('--beta', default=None, type=float, help='weights in the Rocchio rule')
        parser.add_argument('--index', default=None, required=True, help='Index to search')
        parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')
        
        args = parser.parse_args()
        
        nrounds = args.nrounds
        k = args.k
        R = args.R
        alpha = args.alpha
        beta = args.beta
        index = args.index
        query = args.query
        print(query)

        try:
                client = Elasticsearch()
                s = Search(using=client, index=index)

                if query is not None:

                        #Obtener los k docs mas relevantes
                        q = Q('query_string',query=query[0])
                        for i in range(1, len(query)):
                                q &= Q('query_string',query=query[i])
                        s = s.query(q)
                        response = s[0:k].execute()

                        #Pasar la query a un diccionario
                        dicQuery = queryToDict(query)
                        print('IT: %s QUERY =%s' % ('1',  query))

                        #Calcular tfidf

                        tfquery = calcTFIDFDic(dicQuery, response, client, index)

                        #Aplicar Rocchio rule
                        for i in range(3,nrounds):  

                                for word, w in dicQuery.items():
                                        dicQuery[word] = int(alpha)*int(w) + int(beta)*int((tfquery[word]/k))        

                                pQuery = dictToQuery(dicQuery)

                                print('IT: %s QUERY =%s' % (str(i-1),  pQuery))
                                
                                q = Q('query_string',query=pQuery[0])
                                for i in range(1, len(query)):
                                        q &= Q('query_string',query=pQuery[i])
                                s = s.query(q)
                                response = s[0:k].execute()

                                tfquery = calcTFIDFDic(dicQuery, response, client, index)

                        for word, w in dicQuery.items():
                                        dicQuery[word] = int(alpha)*int(w) + int(beta)*int((tfquery[word]/k))

                        pQuery = dictToQuery(dicQuery)
                        print('IT: %s QUERY =%s' % (str(nrounds),  pQuery))

                        q = Q('query_string',query=pQuery[0])
                        for i in range(1, len(query)):
                            q &= Q('query_string',query=pQuery[i])
                        s = s.query(q)
                        response = s[0:k].execute()

                        for r in response:  # only returns a specific number of results
                                print(f'ID= {r.meta.id} SCORE={r.meta.score}')
                                print(f'PATH= {r.path}')
                                print(f'TEXT: {r.text[:50]}')
                                print('-----------------------------------------------------------------')

                else:
                        print('No query parameters passed')

        except NotFoundError:
                print(f'Index {index} does not exist')