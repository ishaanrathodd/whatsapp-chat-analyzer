import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import re
import emoji


def remove_escape_sequence(data):
    # Remove LRM character from the WhatsApp chat text
    cleaned_data = re.sub(r'[\u00A0\u200B\u200D\u200C\u200E\u200F\u202A-\u202E\u202C\u2028\u2029\u034F]', '', data)
    return cleaned_data


def fetch_stats(selected_user, media_df, non_media_df):
    if selected_user != 'All':
        media_df = media_df[media_df['user'] == selected_user]

    # No. of messages
    num_messages = media_df.shape[0]

    # No. of words excluding media which is not included in the dataframe and replaced by words like omitted.
    words = []
    for message in non_media_df['message']:
        words.extend(message.split())

    # No. of stickers, images, videos and audios
    num_media_messages = media_df[media_df['message'].str.contains('image omitted|.heic|.png|.jpeg|.jpg|gif omitted|video omitted|.mov|.mp4|.mkv|.m4a|sticker omitted|audio omitted|.wav|.flac|.pdf|.ppt|.pptx|.doc|.docx|.xls|.xlsx|.txt|.csv|media omitted')].shape[0]
    num_stickers = media_df[media_df['message'].str.contains('sticker omitted')].shape[0]
    num_images = media_df[media_df['message'].str.contains('image omitted|.heic|.png|.jpeg|.jpg|gif omitted', na=False)].shape[0]
    num_documents = media_df[media_df['message'].str.contains('.pdf|.ppt|.pptx|.doc|.docx|.xls|.xlsx|.txt|.csv', na=False)].shape[0]
    num_videos = media_df[media_df['message'].str.contains('video omitted|.mov|.mp4|.mkv|.m4a', na=False)].shape[0]
    num_audios = media_df[media_df['message'].str.contains('audio omitted|.wav|.flac')].shape[0]

    return num_messages, len(words), num_videos, num_images, num_stickers, num_audios, num_media_messages, num_documents


# Link extractor
def find_links(messages):
    # Initialize an empty list to store the extracted URLs
    links = []

    # Iterate through each message in the DataFrame
    for message in messages:
        # Split the message into words
        words = message.split()
        # Iterate through each word to find URLs containing "https://"
        for word in words:
            if "https://" in word or "http://" in word:
                # Append the URL to the links list
                links.append(word)
    link = len(links)
    # Return the list of extracted URLs
    return link


# Returning number of messages done by particular person and its percentage
def busy_users(media_df):
    x = media_df['user'].value_counts().head()
    new_df = round((media_df['user'].value_counts() / media_df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, new_df


def create_wordcloud(selected_user, non_media_df):
    f = open('stop_hinglish.txt', 'r', encoding='utf-8')
    stop_words = f.read()

    if selected_user != 'All':
        df = non_media_df[non_media_df['user'] == selected_user]

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            word.strip()
            if word not in stop_words:
                words.append(word)

        return " ".join(words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    non_media_df['message'] = non_media_df['message'].apply(remove_stop_words)
    df_wc = wc.generate(non_media_df['message'].str.cat(sep=" "))
    return df_wc


# Most Common Words
def most_common_words(selected_user, non_media_df):
    if selected_user != 'All':
        non_media_df = non_media_df[non_media_df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in non_media_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_words_df


# Most Common Emojis
def most_common_emojis(selected_user, non_media_df):
    if selected_user != 'All':
        non_media_df = non_media_df[non_media_df['user'] == selected_user]

    emojis = []
    for message in non_media_df['message']:
        emojis.extend([c for c in message for match in emoji.emoji_list(c)])

    most_common_emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return most_common_emojis_df


# Monthly Timeline
def timeline(selected_user, media_df):
    if selected_user != 'All':
        media_df = media_df[media_df['user'] == selected_user]

    timeline_df = media_df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline_df.shape[0]):
        time.append(timeline_df['month'][i] + "-" + str(timeline_df['year'][i]))

    timeline_df['time'] = time

    return timeline_df


# Daily Timeline
def daily_timeline(selected_user, media_df):
    if selected_user != 'All':
        media_df = media_df[media_df['user'] == selected_user]

    daily_timeline_df = media_df.groupby('only date').count()['message'].reset_index()

    return daily_timeline_df


# Activity Map
def week_activity_map(selected_user, media_df):
    if selected_user != 'All':
        media_df = media_df[media_df['user'] == selected_user]

    return media_df['day_name'].value_counts()


def month_activity_map(selected_user, media_df):
    if selected_user != 'All':
        media_df = media_df[media_df['user'] == selected_user]

    return media_df['month'].value_counts()


# Heat Map
def activity_heatmap(selected_user, media_df):
    if selected_user != 'All':
        media_df = media_df[media_df['user'] == selected_user]

    user_heatmap = media_df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
