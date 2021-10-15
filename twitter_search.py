#!/usr/bin/env python
import threading
import requests
import cx_Oracle
import signal
import json
import queries as db
from constants import URL, token, DB, DB_USER, DB_PASSWORD

terminate = False

def exit_loop(signum,frame): 
    global terminate          
    terminate = True


def select_from_db(query, args_dict, connection):
    cursor = connection.cursor()
    items = []
    get_query = cursor.execute(query, args_dict)
    col_names = [row[0] for row in cursor.description]
    for row in get_query:
        data = {}
        for i, col in enumerate(col_names):
            data[col.lower()] = row[i]
        items.append(data)
    cursor.close()
    return items


def call_procedure(proc_name, args, connection):
    cursor = connection.cursor()
    cursor.callproc(proc_name, args)
    cursor.close()      


def insert_into_db(query, args_dict, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query, args_dict)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        try:
            cursor.close()
        except:
            pass


def process_input(tweet, connection):
    my_json = tweet.decode('UTF-8')
    data = json.loads(my_json)
    tweet = data.get('data')
    if not tweet:
        return
    
    referenced_tweets = tweet.get('referenced_tweets')
    if not referenced_tweets:
        referenced_tweet = {'id':'', 'type':''}
    else:
        referenced_tweet = tweet.get('referenced_tweets')[0]

    tweets_args = {
        "tweet_id": tweet.get('id'), 
        "author_id": tweet.get('author_id'), 
        "attachments":'', 
        "conversation_id": tweet.get('conversation_id'), 
        "created_at": tweet.get('created_at'), 
        "geo": '',#data['data']['geo'], 
        "in_reply_to_user_id": tweet.get('in_reply_to_user_id'), 
        "lang": tweet.get('lang'), 
        "possibly_sensitive": tweet.get('possibly_sensitive'), 
        "retweet_count": tweet.get('public_metrics').get('retweet_count', 0), 
        "reply_count": tweet.get('public_metrics').get('reply_count', 0), 
        "like_count": tweet.get('public_metrics').get('like_count', 0), 
        "quote_count": tweet.get('public_metrics').get('quote_count', 0), 
        "type": referenced_tweet.get('type'), 
        "replied_to_id": referenced_tweet.get('id'), 
        "reply_settings": tweet.get('reply_settings'), 
        "source": tweet.get('source'), 
        "text": tweet.get('text'), 
        "matching_rules": data['matching_rules'][0]['id']
    }
    if not insert_into_db(db.insertion_tweets_query, tweets_args, connection):
        return

    includes = data.get('includes')
    if includes:
        users = includes.get('users')
    
    if users:
        for user in users:
            public_metrics = user.get('public_metrics', None)
            if not public_metrics:
                public_metrics = {}
            users_args = {
                "user_id": user.get('id'), 
                "tweet_id": tweet.get('id'), 
                "created_at": user.get('created_at'), 
                "description": user.get('description'), 
                "location": user.get('location'), 
                "name": user.get('name'), 
                "profile_image_url": user.get('profile_image_url'), 
                "protected": user.get('protected'), 
                "followers_count": public_metrics.get('followers_count'), 
                "following_count": public_metrics.get('following_count'), 
                "tweet_count": public_metrics.get('tweet_count'), 
                "listed_count": public_metrics.get('listed_count'), 
                "url": user.get('url'), 
                "username": user.get('username'), 
                "verified": user.get('verified')
            }
            insert_into_db(db.insertion_users_query, users_args, connection)

    entities = tweet.get('entities')
    if entities:
        mentions = entities.get('mentions')
        if mentions:
            for mention in mentions:
                mentions_args = {
                    "tweet_id": tweet.get('id'), 
                    "start_pos": mention.get('start'), 
                    "end_pos": mention.get('end'), 
                    "username": mention.get('username'), 
                    "user_id": mention.get('id')
                }
                insert_into_db(db.insertion_mentions_query, mentions_args, connection)

        hashtags = entities.get('hashtags')
        if hashtags:
            for hashtag in hashtags:
                hashtags_args = {
                    "tweet_id": tweet.get('id'), 
                    "start_pos": hashtag.get('start'), 
                    "end_pos": hashtag.get('end'), 
                    "tag": hashtag.get('tag')
                }
                insert_into_db(db.insertion_hashtags_query, hashtags_args, connection)

    context_annotations = tweet.get('context_annotations')
    if context_annotations:
        for context in context_annotations:
            domain = context.get('domain')
            if not domain:
                domain = {}
            entity = context.get('entity')
            if not entity:
                entity = {}
            contexts_args = {
                "tweet_id": tweet.get('id'), 
                "domain_id": domain.get('id'), 
                "domain_name": domain.get('name'), 
                "domain_description": domain.get('description'), 
                "entity_id": entity.get('id'), 
                "entity_name": entity.get('name'), 
                "entity_description": entity.get('description')
            }
            insert_into_db(db.insertion_contexts_query, contexts_args, connection)
    
    call_procedure('sentiment_analysis', [tweet.get('id')], connection)


    

if __name__ == "__main__":
    HEADERS = {"Authorization": f"Bearer {token}"}

    connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB, threaded = True)
    connection.autocommit = True

    count = 0
    threads = []

    signal.signal(signal.SIGINT, exit_loop)
    signal.signal(signal.SIGTERM, exit_loop)
    signal.signal(signal.SIGQUIT, exit_loop)

    try:
        with requests.get(url = URL, headers = HEADERS, stream=True) as resp:
            for line in resp.iter_lines():
                if line:
                    t = threading.Thread(target=process_input, args=(line, connection))
                    if terminate:
                        print('\nTerminating...')
                        break
                    threads.append(t)
                    t.start()
    except Exception as e:
        print(e)

    for t in threads:
        t.join()    
    

  
  

