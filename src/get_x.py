#!/usr/bin/env python
# coding: utf-8

# In[106]:


import requests
import json
import numpy as np
import pandas as pd

bearer_token = 'bearer token here'
lst_fields = "created_at,follower_count"
user_fields = 'created_at,description'


class get_posts:
    
    def __init__(self):
        self.posts = {}

    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2ListLookupPython"
        return r


    def create_url(query, id="276332668"):
        """
        Formats the proper url for the three separate queries needed to obtain the tweets from the accounts
        in a users list

        Parameters
        ----------
        query: the different endpoint to query for. 

        Returns
        -------
        A dictionary of the specified twitter user's lists which they follow with essential information such as list ID

        """
        if query == 'lst': 
            url = "https://api.twitter.com/2/users/{}/owned_lists".format(id)
        if query == 'brands':
            url = "https://api.twitter.com/2/lists/{}/members".format(id)
        if query == 'posts':
            url = "https://api.twitter.com/2/users/{}/tweets".format(id)

        return url 

    def parameters(query = 'query'):
        """
        Formats the proper parameters for the needed endoints to obtain essential data on tweets for the accounts in the user's list

        Parameters
        ----------
        query: the different endpoint to query for. 

        Returns
        -------
        A string of the proper format to request the specific data of interest. 
        """
        if query == 'lst':
            params = "list.fields={}".format(lst_fields)
        elif query == 'brands':
            params = "user.fields={}".format(user_fields)
        elif query == 'posts':
            params = {"tweet.fields": "created_at,entities,public_metrics", "expansions":"attachments.media_keys", "media.fields": "preview_image_url", "user.fields" : 'entities'}
        else:
            raise ValueError('paramter value not valid, check input and try again')

        return params




    def connect_endpoint(url, params):
        """
        Makes the api call to twitter using the url and parametrs specified in the previous functions

        Parameters
        ----------
        url: A string. The url created by "create_url" depending on the endpoint 
        params: A string of parameters for the api call

        Returns
        -------
        A dictionary of accounts and data requested given the parameters 

        """
        response = requests.request("GET", url, auth=bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()




    def get_data(query, id="276332668"):
        """
        Makes the api call to twitter using the url and parametrs specified in the previous functions

        Parameters
        ----------
        url: A string. The url created by "create_url" depending on the endpoint 
        params: A string of parameters for the api call

        Returns
        -------
        A dictionary of accounts and data requested given the parameters 

        """
        url = create_url(query = query, id = id)
        params = parameters(query = query)
        r = connect_endpoint(url, params = params)
        return r 




    def get_final(id="276332668"):
        """
        Calls all endpoints and extracts the data of interest from the returned query

        Parameters
        ----------
        id: the twitter id of the user

        Returns
        -------
        A dictionary of tweets, dates of the tweet, likes and impression counts, and the images associated with the tweets

        """
        r = get_data(query = 'lst', id = id)
        list_id = [x['id'] for x in r['data'] if x['name'] == "Fashion"][0]
        r = get_data(query = 'brands', id = list_id)
        brand_id = [x['id'] for x in r['data']]
        brands = [x['name'] for x in r['data']]

        timeline = {}
        for brand_name in brands:
            timeline[brand_name] = {'text': [], 'date': [], 'metrics': [], 'img': [], 'brand_id': []}


        for key, ID in zip(timeline.keys(), brand_id):

            tweets = get_data(query = 'posts', id = ID)


            timeline[key]['text'].append([x['text'] for x in tweets['data']])
            timeline[key]['date'].append([x['created_at'] for x in tweets['data']])
            timeline[key]['metrics'].append([x['public_metrics'] for x in tweets['data']])

            sublst = [x['entities']['urls'] for x in tweets['data']]

            timeline[key]['img'].append([x[0]['url'] for x in sublst])

        return timeline




    def get_metrics(dic = 'dic'):
        """
        Generates an index of tweets which are most relevant based on popularity which is based on just likes or 
        likes and impression count

        Parameters
        ----------
        dic: the dictionary returned from clean_data

        Returns
        -------
        A dictionary with lists of indices which determine which order to return the tweets. 

        """
        keys = dic.keys()
        popular = {}
        for key in keys:
            trics = dic[key]['met']
            likes = [x['like_count'] for x in trics]
            impres = [x['impression_count'] for x in trics]
            count_impres = 0 
            for i in impres:
                for l in likes:
                    if i*l != 0:
                        count_impres += 1
            if count_impres/len(impres) > .5:       
                pop = [a*b for a,b in zip(likes,impres)]
                pop_index = pop[:]
                pop_index.sort(reverse = True)


            else:
                pop = likes
                pop_index = pop[:]
                pop_index.sort(reverse = True)
            popular[key] = {'index' : pop, "pop" : pop_index}
            order = {}
            for key in popular:
                lst = []
                uni_pop = np.unique(popular[key]['pop'])
                for i in range(len(uni_pop)):
                    for j in range(len(popular[key]['pop'])):
                        if popular[key]['index'][j] == uni_pop[i]:
                            lst.append(j)
                order[key] = lst




        return order




    def clean_data(id="276332668"):
        """
        Cleans the tweets for weird characters

        Parameters
        ----------
        id: id of the user which is passed to the get_final function 

        Returns
        -------
        A dictionary with the new clean tweets at the front of the values for their respective keys. 

        """
        dic = get_final(id = id)
        for key in dic.keys():
            clean_text = []
            text = dic[key]['text']
            for t in range(len(text)):
                temp_t = text[t]
                temp_t = temp_t.replace('\n\n', ' ')
                clean_text.append(temp_t)
            dic[key]['text'] = clean_text

        return dic


    def gather_data(pop = 'popoular', id = id):
        """
        Gathers the data, indexes the list based on filtering method of choice, 
        and prints the recent tweets so one may avoid the depths of their social media timeline. 

        Parameters
        ----------
        id: id of the user which is passed to the get_final function 
        filter: if popular, then the tweets with the most engagement will be returned first. 

        Returns
        -------
        Prints the text and date of the most recent tweets with any included links.  

        """
        dic = clean_data(id)
        index = get_metrics(dic)
        if pop == 'popular':
            for key in dic.keys():
                for i in range(len(index[key])):
                    cnt = index[key][i]
                    print(f"Most popular recent tweet #{i}: {dic[key]['text'][cnt]}")
                    print(f"date of tweet:{dic[key]['date'][cnt]}")
        else:
             for key in dic.keys():
                for i in range(len(pop[key])):
                    cnt = pop[key][i]
                    print(f"Most popular recent tweet #{i}: {dic[key]['text'][cnt]}")
                    print(f"date of tweet:{dic[key]['date'][cnt]}")



    def get_images(id = 'id'):
        img_dic = {}
        dic = get_final()
        for key in dic.keys():
            print(dic[key])
            img_dic[key] = [x for x in dic[key]['img']]

        print(img_dic)
        df = pd.DataFrame(img_dic)
        df.to_csv('x_images.csv')



    def main():
        '''
        Call the get_images function which will save a dataframe of the image files to the directory 
        which can then be used by the image classifier once it exists
        '''

        get_images()


    
    
                

