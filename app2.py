# importing shit 
import pandas as pd
import requests 
import csv 
import warnings
import streamlit as st
from time import sleep

from stqdm import stqdm

st.markdown('built by [yesyes](https://warpcast.com/yesyes)')

st.title("Farcaster Follow recommendations")
st.write("if the app isn't working on your phone then please view it in your browser as a  desktop site or open it in your pc. thanks")

username = st.text_input('Enter your username on Farcaster')

option = st.selectbox(
        'Do you want to include people without the active badge in the recommended list?',
        ('Include everyone', 'Only include people with active badges'))

number = int(st.number_input('Number of recommendations(enter a positive integer)', value=5.00))

x = st.button('search')


if(x):
    st.write("processing - give it 2 minutes")
    #st.write(number)
    url5 = "https://api.warpcast.com/v2/user-by-username"

    params5 = {"username": username} 
    testing = requests.get(url5,params5)
    data5 = testing.json()
    result5 =  data5["result"]["user"]
    fid = result5["fid"]

    #getting collections
    url = "https://api.warpcast.com/v2/user-collections"
    cursor = None
    list = []
    params = {"ownerFid": fid,"limit":100, "cursor": cursor} if cursor else {"ownerFid": fid,"limit":100}

    response = requests.get(url,params=params)
    data = response.json()
    result =  data["result"]["collections"]

    for i in range(len(result)):
        list.append(result[i]['id'])


    cursor = data.get("next",{}).get("cursor")

    while(cursor != None):

        params = {"ownerFid": fid,"limit": 100, "cursor": cursor} if cursor else {"ownerFid": fid,"limit": 100}
        response = requests.get(url,params=params)
        data = response.json()
        result = data["result"]["collections"]
        cursor = data.get("next",{}).get("cursor")

        for i in range(len(result)):
            list.append(result[i]['id'])
    length = len(list)
    increment = 1
    progress = stqdm(total=length)
    index = 0

    #getting all users of that list
    if(option != None):
        #st.write(option)
        url2 = "https://api.warpcast.com/v2/collection-owners"
        cursor2 = None
        list2 = []
        if(option == 'Include everyone' ):

            for i in range(len(list)):
                index += increment
                progress.update(increment)
                params2 = {"collectionId":list[i] ,"limit":100, "cursor": cursor2} if cursor2 else {"collectionId": list[i],"limit":100}

                response2 = requests.get(url2,params=params2)
                data2 = response2.json()
                result2 =  data2["result"]["users"]
                #st.progress(i)
                for j in range(len(result2)):
                    list2.append(result2[j]['fid'])

                #st.write("on", list[i])
                #placeholder = st.empty()
                #placeholder.write(i)
                #placeholder = st.empty()
                cursor2 = data2.get("next",{}).get("cursor")

                while(cursor2 != None):
                    #st.write("on", list[i])
                    params2 = {"collectionId": list[i] ,"limit": 100, "cursor": cursor2} if cursor2 else {"collectionId": list[i],"limit": 100}
                    response2 = requests.get(url2,params=params2)
                    data2 = response2.json()
                    result2 =  data2["result"]["users"]
                    cursor2 = data2.get("next",{}).get("cursor")

                    for j in range(len(result2)):
                        list2.append(result2[j]['fid'])
        elif(option == 'Only include people with active badges' ):
            
            for i in range(len(list)):
                index += increment
                progress.update(increment)
                params2 = {"collectionId":list[i] ,"limit":100, "cursor": cursor2} if cursor2 else {"collectionId": list[i],"limit":100}
                #st.write(list[i])
                #st.progress(i)
                response2 = requests.get(url2,params=params2)
                data2 = response2.json()
                result2 =  data2["result"]["users"]

                for j in range(len(result2)):
                    if(result2[j]["activeOnFcNetwork"] == True):
                        list2.append(result2[j]['fid'])


                cursor2 = data2.get("next",{}).get("cursor")

                while(cursor2 != None):

                    params2 = {"collectionId": list[i] ,"limit": 100, "cursor": cursor2} if cursor2 else {"collectionId": list[i],"limit": 100}
                    response2 = requests.get(url2,params=params2)
                    data2 = response2.json()
                    result2 =  data2["result"]["users"]
                    cursor2 = data2.get("next",{}).get("cursor")
                    #st.write(list[i])
                    #st.progress(i)
                    for j in range(len(result2)):
                        if(result2[j]["activeOnFcNetwork"] == True):
                            list2.append(result2[j]['fid'])            

        #x = st.selectbox('Pick one', ['cats', 'dogs'])
        
        url3 = "https://api.warpcast.com/v2/following"
        cursor3 = None

        list3 = []

        params3 = {"fid": fid,"limit":100, "cursor": cursor3} if cursor3 else {"fid": fid, "limit":100}

        response3 = requests.get(url3,params=params3)
        data3 = response3.json()
        result3 = data3["result"]["users"]
        cursor3 = data3.get("next",{}).get("cursor")
        for i in range(len(result3)):
            list3.append(result3[i]["fid"])
                



        while(cursor3 != None):
            params3 = {"fid": fid,"limit":100, "cursor": cursor3} if cursor3 else {"fid": fid, "limit":100}
            #st.write(cursor3)
            response3 = requests.get(url3,params=params3)
            data3 = response3.json()
            result3 = data3["result"]["users"]
            cursor3 = data3.get("next",{}).get("cursor")
            for i in range(len(result3)):
                list3.append(result3[i]["fid"])
                                                
        def remove_values(lst, values):
            return [x for x in lst if x not in values]
        
        from collections import Counter

        def top_most_repeated_numbers(lst, n):
            counter = Counter(lst)
            most_common = counter.most_common(n)
            return [num for num, count in most_common]
        

        result = remove_values(list2, list3)
        mc = [fid]
        winner = None
        result = remove_values(result ,mc)
        winner = top_most_repeated_numbers(result,number)
        #st.write(winner)

        if(winner != None):
            
            for i in range(len(winner)):
                url6 = "https://api.warpcast.com/v2/user"
                params6 = {"fid": winner[i]} 
                response6 = requests.get(url6,params=params6)
                data6 = response6.json()
                st.write(data6["result"]["user"]["username"])
                
