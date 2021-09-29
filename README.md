# Content-Ranking

The Content Ranking Engine of the Crawling Service component.

## Configuration

There are two ways to operate this tool:

1. Through Docker *(recommended)*
2. As a standalone CLI tool

The tool requires a configured [MongoDB]('https://www.mongodb.com/') database to operate.

### 1. Docker

Build the image for the Docker container by using the included ```Dockerfile```. Run the following command in the directory of the cloned project.

```shell
docker build -t content-ranking . 
```

To operate the tool, use ```docker-compose``` like the provided example:

```yaml
version: '2'
services:
  content-ranking:
    image: content-ranking
    entrypoint: python3 content_rank.py calc-score 
                --ip="localhost" 
                --username="user"
                --password="pass" 
                --db_crawl="CrawlDB" 
                --collection_crawl="crawl_collection"
                --collection_voc="iotsec_vocab_top10"
                --collection_topic_vec="topic_vectors10"
                --topn=10
                --post_window=30
    volumes:
      - ./data/:/content-ranking/data

```

In this example, the ```calc-score``` command will rank the rank the first 30 entries (```--post-window=30```) of the collection ```crawl_collection```.

To start the content ranking tool, type the following command:

```shell
docker-compose up -d
```

Or to be able to view the output messages:

```shell
docker-compose up
```

To stop the content ranking script type:

```shell
docker-compose down
```

### 2. CLI tool

By using this method, first, install the required packages:

```shell
pip3 install -r requirements.txt
pip3 install paramiko
python3 -c "import nltk;nltk.download('punkt')"
```

Then, simply input the command, as seen in the ```entrypoint``` part of the example above:

```shell
python3 content_rank.py calc-score --ip="localhost" --username="user" --password="pass" --db_crawl="CrawlDB" --collection_crawl="crawl_collection" --collection_voc="iotsec_vocab_top10" --collection_topic_vec="topic_vectors10" --topn=10 --post_window=30
```

## Core commands

The main functionality of the tool is performed by the ```calc-score``` command, but for the first run, ```update-retrain``` is required to intialize and populate the DBs.

For the names of files, DBs and collections it is recommended to keep the defaults, so they can be omitted.

Commands:

1. ```calc-score```:
    Computes the Relevance Score and Word Coverage of the crawled documents.

    <pre>Usage: content_rank.py calc-score [OPTIONS]

    Options:
        --tagfile TEXT               The name of the file that contains the Tags (default "_iotsec_tags.txt")
        --db_crawl TEXT              The name of the Crawl Database (default "CrawlDB")
        --db_voc TEXT                The name of the Vocabulary Database (default "IoTsecDB")
        --collection_crawl TEXT      The name of the Crawl mongoDB collection (default "crawl_collection")
        --collection_voc TEXT        The name of the vocabulary mongoDB collection (default "iotsec_vocab_top10")
        --collection_topic_vec TEXT  The name of the topic vector mongoDB collection (default "topic_vectors10")
        --username TEXT              The username to connect to mongoDB (default --empty--)
        --password TEXT              The password to connect to mongoDB (default --empty--)
        --ip TEXT                    The IP where mongoDB is hosted (default "127.0.0.1")
        --topn INTEGER               The top N most similar words for each Tag (default 10)
        --post_window INTEGER        The number of posts to process (default 0 to process entire collection)
        --iteration INTEGER          The iteration number of Content Ranking (default 0)
        --help                       Show the [Options] and exit
    </pre>

2. ```update-corpus```:
    Donwload the training files, preprocess them, and write them into a corpus.

    <pre>
    Usage: content_rank.py update-corpus [OPTIONS]

    Options:
        --tagfile TEXT               The name of the file that contains the Tags (default "_iotsec_tags.txt")
        --help                       Show the [Options] and exit
    </pre>

3. ```train-model```:
    Train the Word2Vec model.

    *(Note: for information regarding the Word2Vec hyperparameters, refer to this [link](https://radimrehurek.com/gensim/models/word2vec.html))*

    <pre>
    Usage: content_rank.py train-model [OPTIONS]

    Options:
        --corpusfile TEXT            The name of the file that contains the Corpus (default "__iotsec_corpus.txt")
        --dimensions INTEGER         The "dimensions" hyperparameter of the Word2Vec model (default 150)
        --window INTEGER             The "window" hyperparameter of the Word2Vec model (default 5)
        --min_count INTEGER          The "min_count" hyperparameter of the Word2Vec model (default 1)
        --workers INTEGER            The "workers" hyperparameter of the Word2Vec model (default 10)
        --help                       Show the [Options] and exit
    </pre>

4. ```create-vocab```:
    Create the topic vocabulary and add it to the mongoDB collection.

    <pre>
    Usage: content_rank.py create-vocab [OPTIONS]

    Options:
        --tagfile TEXT               The name of the file that contains the Tags (default "_iotsec_tags.txt")
        --db_voc TEXT                The name of the Vocabulary Database (default "IoTsecDB")
        --collection_voc TEXT        The name of the vocabulary mongoDB collection (default "iotsec_vocab_top10")
        --collection_topic_vec TEXT  The name of the topic vector mongoDB collection (default "topic_vectors10")
        --username TEXT              The username to connect to mongoDB (default --empty--)
        --password TEXT              The password to connect to mongoDB (default --empty--)
        --ip TEXT                    The IP where mongoDB is hosted (default "127.0.0.1")
        --topn INTEGER               The top N most similar words for each Tag (default 10)
        --help                       Show the [Options] and exit
    </pre>

5. ```update-retrain```:
    Re-run the entire process of downloading, extracting, preprocessing, training & add to collection *(required command for first run)*.

    <pre>
    Usage: content_rank.py  update-retrain [OPTIONS]

    Options:
    --tagfile TEXT               The name of the file that contains the Tags (default "_iotsec_tags.txt")
    --corpusfile TEXT            The name of the file that contains the Corpus (default "__iotsec_corpus.txt")
    --db_voc TEXT                The name of the Vocabulary Database (default "IoTsecDB")
    --collection_voc TEXT        The name of the vocabulary mongoDB collection (default "iotsec_vocab_top10")
    --collection_topic_vec TEXT  The name of the topic vector mongoDB collection (default "topic_vectors10")
    --username TEXT              The username to connect to mongoDB (default --empty--)
    --password TEXT              The password to connect to mongoDB (default --empty--)
    --ip TEXT                    The IP where mongoDB is hosted (default "127.0.0.1")
    --topn INTEGER               The top N most similar words for each Tag (choose between 5, 10, 15)
    --dimensions INTEGER         The "dimensions" hyperparameter of the Word2Vec model (default 150)
    --window INTEGER             The "window" hyperparameter of the Word2Vec model (default 5)
    --min_count INTEGER          The "min_count" hyperparameter of the Word2Vec model (default 1)
    --workers INTEGER            The "workers" hyperparameter of the Word2Vec model (default 10)
    --help                       Show the [Options] and exit
    </pre>

## References

For more information regarding the functionality of the tool, refer to the following literature:

1. Paris Koloveas, Thanasis Chantzios, Christos Tryfonopoulos, and Spiros Skiadopoulos. A crawler architecture for harvesting the clear, social, and dark web for IoT-related cyber-threat intelligence. *In Proceedings of the IEEE Workshop on Cyber Security & Resilience in the Internet of Things (CSRIoT @ IEEE Services)*, Milan, Italy, July 2019.

2. Paris Koloveas, Thanasis Chantzios, Sofia Alevizopoulou, Spiros Skiadopoulos, and Christos Tryfonopoulos. inTIME: A Machine Learning-Based Framework for Gathering and Leveraging Web Data to Cyber-Threat Intelligence. *In Electronics* 10(7): 818, 2021.

## Contact Information

This repository is maintained by **Paris Koloveas**, University of Peloponnese.

* Email: pkoloveas@uop.gr
