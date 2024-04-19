import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import helper
import preprocesser

st.title("Whatsapp Chat Analyzer")
st.write("⚠️ Export your WhatsApp chat from either an iPhone or an Android device to ensure accurate data presentation. For iPhone, uncompress the ZIP file and upload the \"_chat.txt\" file.")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.read().decode("utf-8")
    data = helper.remove_escape_sequence(bytes_data)
    media_df = preprocesser.preprocess_p1(data)
    if media_df.empty:
        media_df = preprocesser.preprocess_p2(data)
        non_media_df = preprocesser.preprocess_clean_p2(data)
        user_list = media_df['user'].unique().tolist()  # Making the drop-down menu in the sidebar
        user_list.sort()
        user_list.insert(0, "All")  # Keeping 'All' at the top of the drop-down menu for instant total group analysis
        selected_user = st.sidebar.selectbox("Users", user_list)

        if st.sidebar.button("Show Analysis"):
            num_messages, words, num_videos, num_images, num_stickers, num_audios, num_media_messages, num_documents = helper.fetch_stats(
                selected_user,
                media_df, non_media_df)
            links = helper.find_links(media_df['message'])

            st.title("Statistics")
            col1, col2, col3, col4 = st.columns(4, gap="large")

            with col1:
                st.header("Messages")
                st.subheader(num_messages)
            with col2:
                st.header("Words")
                st.subheader(words)
            with col3:
                st.header("Media")
                st.subheader(num_media_messages)
            with col4:
                st.header("Links")
                st.subheader(links)

            if selected_user == 'All':
                st.title('Most Busy Users')
                x, new_df = helper.busy_users(media_df)
                fig, ax = plt.subplots()  # fig and axes for graph. This is a matplotlib function.

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df, height=320, width=500)

            # WordCloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user, non_media_df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most Common Words
            most_common_words_df = helper.most_common_words(selected_user, non_media_df)
            st.title('Most Common Words')
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(most_common_words_df[0], most_common_words_df[1])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(most_common_words_df, height=290, width=500)

            # Most Common Emojis
            emoji_df = helper.most_common_emojis(selected_user, non_media_df)
            if not emoji_df.empty:
                st.title("Emoji Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(emoji_df[0].head(), emoji_df[1].head())
                    st.pyplot(fig)
                with col2:
                    st.dataframe(emoji_df, height=260, width=500)

            # Timeline
            st.title("Timeline")
            col1, col2 = st.columns([0.475, 0.525])

            with col1:
                st.subheader("Monthly")
                monthly = helper.timeline(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.plot(monthly['time'], monthly['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.subheader("Daily")
                daily = helper.daily_timeline(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.plot(daily['only date'], daily['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Week Activity Map
            st.title("Activity Map")
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                st.subheader("Month")
                month_activity = helper.month_activity_map(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.bar(month_activity.index, month_activity.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.subheader("Week")
                week_activity = helper.week_activity_map(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.bar(week_activity.index, week_activity.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Heat Map
            st.title("Heat Map")
            user_heatmap = helper.activity_heatmap(selected_user, media_df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
    else:
        non_media_df = preprocesser.preprocess_clean_p1(data)
        user_list = media_df['user'].unique().tolist()  # Making the drop-down menu in the sidebar
        user_list.sort()
        user_list.insert(0, "All")  # Keeping 'All' at the top of the drop-down menu for instant total group analysis
        selected_user = st.sidebar.selectbox("Users", user_list)

        if st.sidebar.button("Show Analysis"):
            num_messages, words, num_videos, num_images, num_stickers, num_audios, num_media_messages, num_documents = helper.fetch_stats(
                selected_user,
                media_df, non_media_df)
            links = helper.find_links(media_df['message'])

            st.title("Statistics")
            col1, col2, col3, col4 = st.columns(4, gap="large")
            col5, col6, col7, col8 = st.columns(4, gap="large")

            with col1:
                st.header("Messages")
                st.subheader(num_messages)
            with col2:
                st.header("Words")
                st.subheader(words)
            with col3:
                st.header("Stickers")
                st.subheader(num_stickers)
            with col4:
                st.header("Videos")
                st.subheader(num_videos)
            with col5:
                st.header("Images")
                st.subheader(num_images)
            with col6:
                st.header("Audios")
                st.subheader(num_audios)
            with col7:
                st.header("Documents")
                st.subheader(num_documents)
            with col8:
                st.header("Links")
                st.subheader(links)

            if selected_user == 'All':
                st.title('Most Busy Users')
                x, new_df = helper.busy_users(media_df)
                fig, ax = plt.subplots()  # fig and axes for graph. This is a matplotlib function.

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df, height=320, width=500)

            # WordCloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user, non_media_df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most Common Words
            most_common_words_df = helper.most_common_words(selected_user, non_media_df)
            st.title('Most Common Words')
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(most_common_words_df[0], most_common_words_df[1])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(most_common_words_df, height=290, width=500)

            # Most Common Emojis
            emoji_df = helper.most_common_emojis(selected_user, non_media_df)
            if not emoji_df.empty:
                st.title("Emoji Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(emoji_df[0].head(), emoji_df[1].head())
                    st.pyplot(fig)
                with col2:
                    st.dataframe(emoji_df, height=260, width=500)

            # Timeline
            st.title("Timeline")
            col1, col2 = st.columns([0.475, 0.525])

            with col1:
                st.subheader("Monthly")
                monthly = helper.timeline(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.plot(monthly['time'], monthly['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.subheader("Daily")
                daily = helper.daily_timeline(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.plot(daily['only date'], daily['message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Week Activity Map
            st.title("Activity Map")
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                st.subheader("Month")
                month_activity = helper.month_activity_map(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.bar(month_activity.index, month_activity.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.subheader("Week")
                week_activity = helper.week_activity_map(selected_user, media_df)
                fig, ax = plt.subplots()
                ax.bar(week_activity.index, week_activity.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Heat Map
            st.title("Heat Map")
            user_heatmap = helper.activity_heatmap(selected_user, media_df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
