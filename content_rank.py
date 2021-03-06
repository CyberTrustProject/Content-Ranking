# coding: utf-8

import functions as func
import click
from datetime import datetime as dt


default_tagfile = '_iotsec_tags.txt'
default_corpusfile = '__iotsec_corpus.txt'
default_db_crawl = 'CrawlDB'
default_collection_crawl = 'crawl_collection'
default_db_voc = 'IoTsecDB'
default_username = ''
default_password = ''
default_ip = '127.0.0.1'
default_topn = 10
default_collection_voc = 'iotsec_vocab_top' + str(default_topn)
default_collection_topic_vec = 'topic_vectors' + str(default_topn)
default_dimensions = 150
default_window = 5
default_min_count = 1
default_workers = 10
default_post_win = 0
default_iteration_number = 0


@click.group()
def main():
    pass


@main.command()
@click.option(
    '--tagfile',
    type=click.STRING,
    default=default_tagfile,
    help="The name of the file that contains the Tags"
)
def update_corpus(tagfile):
    """Donwload the training files, preprocess them, and write them into a corpus"""
    startTime = dt.now()
    func.download_stackexchange_data()
    func.xml_extraction()
    func.data_process(
        tokenizer=func.create_multiword_tags(tagfile)
    )
    print('Runtime: ' + str(dt.now() - startTime))


@main.command()
@click.option(
    '--corpusfile',
    type=click.STRING,
    default=default_corpusfile,
    help="The name of the file that contains the Corpus"
)
@click.option(
    '--dimensions',
    type=click.INT,
    default=default_dimensions,
    help="The \"dimensions\" hyperparameter of the Word2Vec model"
)
@click.option(
    '--window',
    type=click.INT,
    default=default_window,
    help="The \"window\" hyperparameter of the Word2Vec model"
)
@click.option(
    '--min_count',
    type=click.INT,
    default=default_min_count,
    help="The \"min_count\" hyperparameter of the Word2Vec model"
)
@click.option(
    '--workers',
    type=click.INT,
    default=default_workers,
    help="The \"workers\" hyperparameter of the Word2Vec model"
)
def train_model(corpusfile, dimensions, window, min_count, workers):
    """Train the word2vec model"""
    startTime = dt.now()
    func.train(
        corpusfile=corpusfile,
        dimensions=dimensions,
        window=window,
        min_count=min_count,
        workers=workers
    )
    print('Runtime: ' + str(dt.now() - startTime))


@main.command()
@click.option(
    '--tagfile',
    type=click.STRING,
    default=default_tagfile,
    help="The name of the file that contains the Tags"
)
@click.option(
    '--topn',
    type=click.INT,
    default=default_topn,
    help="The top N most similar words for each Tag"
)
@click.option(
    '--db_voc',
    type=click.STRING,
    default=default_db_voc,
    help="The name of the Vocabulary Database"
)
@click.option(
    '--collection_voc',
    type=click.STRING,
    default=default_collection_voc,
    help="The name of the vocabulary mongoDB collection"
)
@click.option(
    '--collection_topic_vec',
    type=click.STRING,
    default=default_collection_topic_vec,
    help="The name of the topic vector mongoDB collection"
)
@click.option(
    '--username',
    type=click.STRING,
    default=default_username,
    help="The username to connect to mongoDB"
)
@click.option(
    '--password',
    type=click.STRING,
    default=default_password,
    help="The password to connect to mongoDB"
)
@click.option(
    '--ip',
    type=click.STRING,
    default=default_ip,
    help="The IP where mongoDB is hosted"
)
def create_vocab(tagfile, topn, db_voc, collection_voc, collection_topic_vec, username, password, ip):
    """Create the topic vocabulary and add it to the mongoDB collection"""
    startTime = dt.now()
    func.create_topic_dict(
        tagfile=tagfile,
        topn=topn,
        collection=func.connect_to_mongo_collection(
            db_name=db_voc,
            collection_name=collection_voc,
            username=username,
            password=password,
            ip=ip
        )
    )
    func.compute_topic_vec(
        collection_voc=func.connect_to_mongo_collection(
            db_name=db_voc,
            collection_name=collection_voc,
            username=username,
            password=password,
            ip=ip
        ),
        collection_topic_vec=func.connect_to_mongo_collection(
            db_name=db_voc,
            collection_name=collection_topic_vec,
            username=username,
            password=password,
            ip=ip
        )
    )
    print('Runtime: ' + str(dt.now() - startTime))


@main.command()
@click.option(
    '--tagfile',
    type=click.STRING,
    default=default_tagfile,
    help="The name of the file that contains the Tags"
)
@click.option(
    '--corpusfile',
    type=click.STRING,
    default=default_corpusfile,
    help="The name of the file that contains the Corpus"
)
@click.option(
    '--topn',
    type=click.INT,
    default=default_topn,
    help="The top N most similar words for each Tag"
)
@click.option(
    '--dimensions',
    type=click.INT,
    default=default_dimensions,
    help="The \"dimensions\" hyperparameter of the Word2Vec model"
)
@click.option(
    '--window',
    type=click.INT,
    default=default_window,
    help="The \"window\" hyperparameter of the Word2Vec model"
)
@click.option(
    '--min_count',
    type=click.INT,
    default=default_min_count,
    help="The \"min_count\" hyperparameter of the Word2Vec model"
)
@click.option(
    '--workers',
    type=click.INT,
    default=default_workers,
    help="The \"workers\" hyperparameter of the Word2Vec model"

)
@click.option(
    '--db_voc',
    type=click.STRING,
    default=default_db_voc,
    help="The name of the Vocabulary Database"
)
@click.option(
    '--collection_voc',
    type=click.STRING,
    default=default_collection_voc,
    help="The name of the vocabulary mongoDB collection"
)
@click.option(
    '--collection_topic_vec',
    type=click.STRING,
    default=default_collection_topic_vec,
    help="The name of the topic vector mongoDB collection"
)
@click.option(
    '--username',
    type=click.STRING,
    default=default_username,
    help="The username to connect to mongoDB"
)
@click.option(
    '--password',
    type=click.STRING,
    default=default_password,
    help="The password to connect to mongoDB"
)
@click.option(
    '--ip',
    type=click.STRING,
    default=default_ip,
    help="The IP where mongoDB is hosted"
)
def update_retrain(tagfile, corpusfile, topn, dimensions, window, min_count, workers, db_voc, collection_voc, collection_topic_vec, username, password, ip):
    """Re-run the entire process of downloading, extracting, preprocessing, training & add to collection"""
    startTime = dt.now()
    func.update_retrain_all(
        tagfile=tagfile,
        corpusfile=corpusfile,
        collection_voc=func.connect_to_mongo_collection(
            db_name=db_voc,
            collection_name=collection_voc,
            username=username,
            password=password,
            ip=ip
        ),
        collection_topic_vec=func.connect_to_mongo_collection(
            db_name=db_voc,
            collection_name=collection_topic_vec,
            username=username,
            password=password,
            ip=ip
        ),
        topn=topn,
        dimensions=dimensions,
        window=window,
        min_count=min_count,
        workers=workers
    )
    print('Runtime: ' + str(dt.now() - startTime))


@main.command()
@click.option(
    '--post_window',
    type=click.INT,
    default=default_post_win,
    help="The number of posts to process (defaults to 0 to process entire collection)"
)
@click.option(
    '--tagfile',
    type=click.STRING,
    default=default_tagfile,
    help="The name of the file that contains the Tags"
)
@click.option(
    '--topn',
    type=click.INT,
    default=default_topn,
    help="The top N most similar words for each Tag"
)
@click.option(
    '--db_voc',
    type=click.STRING,
    default=default_db_voc,
    help="The name of the Vocabulary Database"
)
@click.option(
    '--collection_voc',
    type=click.STRING,
    default=default_collection_voc,
    help="The name of the vocabulary mongoDB collection"
)
@click.option(
    '--collection_topic_vec',
    type=click.STRING,
    default=default_collection_topic_vec,
    help="The name of the topic vector mongoDB collection"
)
@click.option(
    '--db_crawl',
    type=click.STRING,
    default=default_db_crawl,
    help="The name of the Crawl Database"
)
@click.option(
    '--collection_crawl',
    type=click.STRING,
    default=default_collection_crawl,
    help="The name of the Crawl mongoDB collection"
)
@click.option(
    '--username',
    type=click.STRING,
    default=default_username,
    help="The username to connect to mongoDB"
)
@click.option(
    '--password',
    type=click.STRING,
    default=default_password,
    help="The password to connect to mongoDB"
)
@click.option(
    '--ip',
    type=click.STRING,
    default=default_ip,
    help="The IP where mongoDB is hosted"
)
@click.option(
    '--iteration',
    type=click.INT,
    default=default_iteration_number,
    help="The iteration number of Content Ranking (starts from 0 by default)"
)
def calc_score(post_window, tagfile, topn, db_voc, collection_voc, collection_topic_vec, db_crawl, collection_crawl, username, password, ip, iteration):
    """Computes the Similarity Score of the crawlDB Posts for a specified number of Posts"""
    startTime = dt.now()

    coll = func.connect_to_mongo_collection(
        db_name=db_crawl,
        collection_name=collection_crawl,
        username=username,
        password=password,
        ip=ip
    )

    collection_topic_vec = func.connect_to_mongo_collection(
        db_name=db_voc,
        collection_name=collection_topic_vec,
        username=username,
        password=password,
        ip=ip
    )

    collection_voc = func.connect_to_mongo_collection(
        db_name=db_voc,
        collection_name=collection_voc,
        username=username,
        password=password,
        ip=ip
    )

    topic_vec = func.get_topic_vec(collection_topic_vec)
    tokenizer = func.create_multiword_tags(tagfile=tagfile)

    score_label = "score{}".format(topn)

    for doc in coll.find({}, batch_size=10, no_cursor_timeout=True).limit(post_window):

        # print(score_label)
        if score_label not in doc:
            # print("{} not ranked".format(doc['doc_id']))

            score, word_coverage = func.post_relevance(
                post=doc['raw_text'],
                topic_vec=topic_vec,
                collection_voc=collection_voc,
                topn=topn,
                tokenizer=tokenizer
            )

            # print("got score {}".format(score))
            # print('Runtime: ' + str(dt.now() - startTime))

            id_query = {'_id': doc['_id']}

            score_query = {'$set': {score_label: score}}
            coll.update_one(id_query, score_query)

            word_coverage_query = {'$set': {'word_coverage': word_coverage}}
            coll.update_one(id_query, word_coverage_query)

            iteration_query = {'$set': {'iteration': iteration}}
            coll.update_one(id_query, iteration_query)

            ner_init_query = {'$set': {'ner': False}}
            coll.update_one(id_query, ner_init_query)

            misp_init_query = {'$set': {'in_misp': False}}
            coll.update_one(id_query, misp_init_query)

            print("{} has relevance score: {} and word coverage: {} (Time: {})".format(doc['doc_id'], score, word_coverage, str(dt.now() - startTime)))
        else:
            print("{} is ranked".format(doc['doc_id']))
            # id_query = {'_id': doc['_id']}
            # delete_scores_query = {'$unset': {'score10': ""}}
            # coll.update_one(id_query, delete_scores_query)

    print('Runtime: ' + str(dt.now() - startTime))


if __name__ == "__main__":
    main()
