#19 items
insertion_tweets_query = '''insert into tweets(tweet_id, author_id, attachments, conversation_id, created_at, geo, in_reply_to_user_id, lang, possibly_sensitive, retweet_count, reply_count, like_count, quote_count, type, replied_to_id, reply_settings, source, text, matching_rules)
values (:tweet_id, :author_id, :attachments, :conversation_id, TO_UTC_TIMESTAMP_TZ(:created_at), :geo, :in_reply_to_user_id, :lang, :possibly_sensitive, :retweet_count, :reply_count, :like_count, :quote_count, :type, :replied_to_id, :reply_settings, :source, :text, :matching_rules)'''


#15 items
insertion_users_query = '''insert into users(user_id, tweet_id, created_at, description, location, name, profile_image_url, protected, followers_count, following_count, tweet_count, listed_count, url, username, verified)
values (:user_id, :tweet_id, TO_UTC_TIMESTAMP_TZ(:created_at), :description, :location, :name, :profile_image_url, :protected, :followers_count, :following_count, :tweet_count, :listed_count, :url, :username, :verified)'''


#5 items
insertion_mentions_query = '''insert into mentions(tweet_id, start_pos, end_pos, username, user_id)
values (:tweet_id, :start_pos, :end_pos, :username, :user_id)'''


#5 items
insertion_hashtags_query = '''insert into hashtags(tweet_id, start_pos, end_pos, tag)
values (:tweet_id, :start_pos, :end_pos, :tag)'''


#7 items
insertion_contexts_query = '''insert into contexts(tweet_id, domain_id, domain_name, domain_description, entity_id, entity_name, entity_description)
values (:tweet_id, :domain_id, :domain_name, :domain_description, :entity_id, :entity_name, :entity_description)'''


time_conversion_query = '''
select TO_UTC_TIMESTAMP_TZ(:time) from dual
'''
