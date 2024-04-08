import re
import pandas as pd


# DataFrame with media messages
def preprocess(data):
    pattern = '\[\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[AP]M]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [date.replace('[', '').replace(']', '') for date in dates]
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M:%S %p ')

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[0:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['only date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['message'] = df['message'].str.lower().str.strip()
    df['user'] = df['user'].str.replace(r"[@+]", '', regex=True)
    df['message'] = df['message'].str.replace(r"[~!@#$%^&*()_+{}:\"><?.`1234567890-=\[\];',/]", '', regex=True)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    # Identify users who have sent the target message
    target_message = "messages and calls are end-to-end encrypted no one outside of this chat not even whatsapp can read or listen to them"
    group_name = df[df['message'].str.contains(target_message, case=False)]['user']

    # Remove identified user from the DataFrame
    media_df = df[~df['user'].isin(group_name)]

    return media_df


# DataFrame without any media messages
def preprocess_clean(data):
    refined_df = preprocess(data)
    non_media_df = refined_df[
        ~refined_df['message'].str.contains(
            'image omitted|.heic|.png|.jpeg|.jpg|document omitted|video omitted|.mov|.mp4|audio omitted|sticker omitted',
            na=False)].reset_index()

    return non_media_df
