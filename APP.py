import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st

st.title("Analysis of IMDb Movies")
def intro():
  st.markdown('''
    Hey there! Welcome to my project. This project is all about Analysis of IMDb Movies from 1894-2020 .
    
    Movies are very important. It is a complex art form. In a perfect film, there is a splendid combination of many art forms. Image and sound and text are the basic. Then there is storywriting, acting, lighting, editing etc.
    
    Now, if you ask me ...."Why movies are important to you?"
    
     -> They make me:


       - Laugh when I need to laugh
       - Cry when I need to cry (Or in my case hold back the tears until no one is looking)
       - Cheer when I need to cheer
       - Scream when I want to scream
       - Be thrilled when I want to be thrilled
       - Be shocked when I want to be shocked
       - And overall, escape when I want to escape.

    Movies are therapy, entertainment, escapism, portals to different worlds, and time machines to the past and possible future.

    That's why movies are important to me.
    
    ''')
intro()
st.markdown('***')

st.subheader('Dataset for IMDb Movies')
st.text('* try filter from the sidebar to see the requested data.')

df=pd.read_csv('IMDbmovies.csv')[:65536]

df.drop(columns=['imdb_title_id', 'title', 'date_published','description','usa_gross_income', 'metascore', ], inplace=True)
df.rename(columns={'original_title': 'Movie_Name', 'year':'Year', 'genre': 'Genre', 'country': 'Country','worlwide_gross_income': 'Worldwide_gross_income' , 'language': 'Language', 'director': 'Director', 'writer': 'Writer', 'preoduction_company': 'Production Company', 'actors': 'Actors', 'avg_vote': 'Rating', 'reviews_from_users': 'Reviews from users', 'reviews_from_critics': 'Reviews from critics'}, inplace= True)

df['Genre'] = df['Genre'].apply(lambda a : a.split(',')[0])




st.sidebar.header("Filter here to get your desired Data in the Dataset :)")

year= st.sidebar.multiselect(
  "First select the Year:",
  options=df["Year"].unique()
)

genre= st.sidebar.multiselect(
  "Now, select the Genre:",
  options=df["Genre"].unique()
)

rating= st.sidebar.slider(
  "Now, select the Rating:", 0.5,10.0,6.0,0.1
  )

df_selection = df.query(
  "Year == @year & Genre == @genre & Rating== @rating"
)

st.dataframe(df_selection)


col1, col2= st.columns(2)
col1.image('LCA.jpg' ,use_column_width= True)
col2.image('FILMROLL.jpg',use_column_width=True)
sidebar= st.sidebar

sidebar.image('cam.png' ,use_column_width=None )


st.markdown('---')
st.subheader('No. of Movies made each year' )
df_2= df.groupby('Year',as_index=False).count().sort_values('Movie_Name',ascending=False)
st.plotly_chart(px.scatter(data_frame=df_2, x='Year' , y='Movie_Name', color='Year' ))
st.markdown('---')

st.subheader('Top 20 years which contributed the most to the Movies')
df5= df.groupby('Year', as_index=False).count().sort_values('Movie_Name',ascending=False)
st.plotly_chart(px.pie(data_frame= df5.head(20), names='Year', values='Movie_Name',height=1000, color_discrete_sequence=px.colors.sequential.dense_r))
st.markdown('---')


dfs=df.sort_values('Rating', ascending= False)
st.subheader('Top 10 Best Movies According to Rating')
st.plotly_chart(px.histogram( data_frame = dfs.head(10), x = 'Movie_Name', y='Rating', color = 'Genre' , template='plotly_dark'))

st.markdown('---')

dfv=df.sort_values('Rating')
st.subheader('Bottom 10 Worst Movies According to Rating')
st.plotly_chart(px.histogram( data_frame = dfv.head(10), x = 'Movie_Name', y='Rating', color = 'Genre' , template='plotly_dark'))
st.markdown('---')

dft=df.sort_values('duration', ascending= False)
st.subheader('10 Longest Movies (in mins.)')
st.plotly_chart(px.histogram( data_frame = dft.head(10), x = 'Movie_Name', y='duration', color = 'Genre' , template='plotly_dark'))
st.markdown('---')




st.subheader('100 Biggest Budget Movies')
df2=df.sort_values('budget', ascending=False)
st.plotly_chart(px.scatter(df2.head(100), x='Movie_Name' , y='budget', color= 'Year',width =1000,  height=800))
st.markdown('---')

st.subheader('100 Highest Gross Income Movies')
df3=df.sort_values('Worldwide_gross_income', ascending=False)
st.plotly_chart(px.scatter(df3.head(100), x='Movie_Name', y='Worldwide_gross_income' ,color= 'Year',width =1000,  height=800))
st.markdown('---')


st.subheader('No. of Reviews from users and critics of Top 100 Rated Movies')
st.plotly_chart(px.bar(dfs.head(100), x='Movie_Name' , y=['Reviews from users', 'Reviews from critics'],width =1000,  height=900 , template='plotly_dark'))
st.markdown('---')


st.subheader('Top 10 Production Companies with most No. of Movies rated 8 or above 8')
dfz=df[(df['Rating']>7.9)]
dfy=dfz.groupby('production_company',as_index=False).count().sort_values('Year',ascending=False)
st.plotly_chart(px.histogram( data_frame = dfy.head(10), x = 'production_company', y='Movie_Name' , template='plotly_dark'))
st.markdown('---')

st.subheader('Top 20 Directors with maximum no. of High Rated Movies')

dfv=dfz.groupby('Director',as_index=False).count().sort_values('Year',ascending=False)
st.plotly_chart(px.histogram( data_frame = dfv.head(20), x = 'Director', y='Movie_Name' , template='plotly_dark'))
st.markdown('---')



st.subheader('Top 100 Most Voted Movies')
dfc=df.sort_values('votes', ascending= False)
st.plotly_chart(px.bar( data_frame = df.head(100), x = 'Movie_Name', y='votes', color = 'Genre',width =1100,  height=900  ,hover_name='Movie_Name', template='plotly_dark'))
st.markdown('---')


st.subheader('3-D visual of the Top-Rated Movies')
dfx=df[(df['Rating']>=7.9)]
st.plotly_chart(px.scatter_3d( data_frame = dfx, x = 'Language', y='Country', z= 'Year',color = 'Genre' ,hover_name='Movie_Name',width =1100,  height=900  , template='plotly_dark', size='votes'))
st.markdown('---')
