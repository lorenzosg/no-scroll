#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import pandas as pd
import sys
sys.setrecursionlimit(15000)

class reccomend:
    
    def __init__(self):
        self.scores = {}
        self.similar = []
        self.diff = []
        
    def load_data(self):
        adj_df = pd.read_csv('/Users/lorenzogiamartino/Desktop/no-scroll/no-scroll/data/classified.csv', index_col = 0)
        adj_df = adj_df.iloc[:, 1:]
        wardrobe_df = pd.read_csv('/Users/lorenzogiamartino/Desktop/no-scroll/no-scroll/data/wardrobe.csv', index_col = 0)
        wardrobe_df = wardrobe_df.iloc[:, 1:]
        wardrobe = list(pd.unique(wardrobe_df.index))
        
        
        return adj_df, wardrobe
        
    def build_network(self, adj_df):
        '''
        Intake pandas df of adjacency matrix from image classifier and outputs symetric normalized covariance matrix of                 clothing items 
        elements at index [i,j] are the conditional probability of two clothing items being styled together in the same image 
        
        Parameters
        ----------
        adj_df: pandas dataframe of adjacency matrix of how often clothing items are styled in X posts 

        Returns
        -------
        network: symetric normalized covariance matrix of clothing items elements at index [i,j] 
        are the conditional probability of two clothing items being styled together in the same image 
        pieces: a list of the article descriptions from column names of adj_df


        '''
        
        
        pieces = list(adj_df.index)
        adj_m = adj_df.to_numpy()
        
        

        adj_m = adj_m
        adj_m_t = adj_m.transpose()
        
        

        mat_dot = np.dot(adj_m, adj_m_t)
        num_photos = np.count_nonzero(adj_m, axis=1) #get number of photos which the article of clothing is styled in


        #normalize matrix
        network = mat_dot / num_photos 
        network2 = mat_dot / num_photos

        #fill diagonals with zeros so that the network doesn't have any self-loops
        np.fill_diagonal(network, 0)

        #get the indices for the upper and lower traingles of the matrix
        i_lower = np.tril_indices(len(mat_dot))
        i_upper = np.triu_indices(len(mat_dot))

        #make each matrix symmetrical 
        network[i_lower] = network.T[i_lower]
        network2[i_upper] = network2.T[i_upper]

        #We want to conservatively estimate the similarity by taking the lower value
        
        for i in range(len(network)):
            for j in range(len(network)):
                if network2[i][j] < network[i][j]:
                    network[i][j] = network2[i][j]
                else:
                    pass

        return network, pieces
    
    
    def categorize_pieces(self, pieces):
       
        '''
        Parses each article description and creates a dictionary linking the attribute(color, type) to the article ID. 
        
        Parameters
        ----------
        pieces: a list of clothing article descriptions which are taken from the columns of the adjacency matrix of 
        clothing article and X posts they appear in 

        Returns
        -------
        A dictionary of each clothing attribute(keys) and a list of all the clothing articles which have the arribute. 

        '''
        
        pieces_dict = {}
        for i, piece in enumerate(pieces):
            attributes = pieces.split('_')
            for att in attributes: 
                pieces_dict[att] += [i]
                
        return pieces_dict
    
    
    def score_wardrobe(self, wardrobe = 'wardrobe', adj_df = 'adj_df', efficient = True, testing = True, only_new = True, long = True, iterations = 3):
        
        '''
        Intake network in numpy array form of clothing article options and list of wardrobe items from user 
        and calculate the optimal purchase score. 
        
         
        Parameters
        ----------
        network: pandas dataframe of adjacency matrix of how often clothing items are styled in X posts 
        optimal: if True, specialization and relatedness scores will be multiplied to get optimal score, otherwise
        similarity scores will be used. This is for purposes of testing and comparison in 'test_recs'. 

        Returns
        -------
        A sorted dictionary in decreasing order with article ID's as keys and optimal purchase values as values. 

        '''
       
        #Need function here to intake and categorize wardrobe data. 
        if testing == False:
            adj_df, wardrobe = self.load_data()
        graph, pieces = self.build_network(adj_df)
        wardrobe_index = [pieces.index(x) for x in wardrobe]
        pieces_index = range(len(pieces))
        if long == False: 
            wardrobe_graph = graph[:, wardrobe_index]
            similar = self.similarity(graph, wardrobe_graph, pieces)
            #include if statement where if they have no similarity don't bother with diff calc. 
            diff = self.difference(graph, wardrobe_graph, pieces)
        else: 
            dic_iter = {}
            mast_dict = {}
            print(pieces)
            results = self.long_difference(mast_dict, dic_iter, graph, wardrobe_index, pieces_index, index = 0, iterations = 3)
            print(results)
            optimal = results['optimal_'+str(iterations)]
            print(optimal)
            
            #similar = self.long_similarity(graph, wardrobe_index, pieces)
            #diff = self.long_difference(graph, wardrobe_index, pieces)
       # if efficient == True:
            #optimal = [x * y for x, y in zip(similar, diff)]
        #else: 
            #optimal = similar[:]
        
        scores = {}
        for score, item in zip(optimal, pieces):
            if only_new == True: 
                if item not in wardrobe:
                    scores[item] = score
                    
            else:
                scores[item] = score
            
        
        sort_scores = sorted(scores.items(), key=lambda x:x[1], reverse = True)
        dict_scores = dict(sort_scores)
        
            
        return dict_scores, optimal
            
            

    def similarity(self, graph, wardrobe_graph, pieces):
        '''
        Compute metrics of relatedness between all possible items and the users wardrobe by subsetting the network matrix 
        to calculate density between users current wardobe and all possible items
        
        Parameters
        ----------
        graph: graph object in numpy array form returned by build_network
        wardrobe_graph: graph subset by columns to include only items in the users wardrobe
        pieces: names of all possible items 

        Returns
        -------
        A list of similarity scores        

        '''
        similar = []
        for i, item in enumerate(pieces):
            item_prox = wardrobe_graph[i, :].sum()
            item_total_prox = graph[i, :].sum()
            if item_total_prox > 0:
                wardrobe_prox = item_prox/item_total_prox
            else:
                wardrobe_prox = 0 
            
            similar.append(wardrobe_prox)
        
        return similar
            

    def difference(self, graph, wardrobe_graph, pieces):
        '''
        Compute metrics of differentiation between all possible items and the users wardrobe by subsetting the network matrix 
        to calculate density between users current wardobe and all possible items
        
        Parameters
        ----------
        graph: graph object in numpy array form returned by build_network
        wardrobe_graph: graph subset by columns to include only items in the users wardrobe
        pieces: names of all possible items 

        Returns
        -------
        A list of differentation scores     

        '''
        diff = []
        for i in range(len(pieces)):
            neighbors_i = graph[i, :] > 0 
            neighbors_w = wardrobe_graph.sum(axis = 1) > 0 
            item_diff = graph[neighbors_i, :][:, neighbors_w].sum()
            item_total_diff = graph[neighbors_i, :].sum()
            if item_total_diff > 0:
                neighbor_prox = item_diff/item_total_diff
            else:
                neighbor_prox = 0
            
            diff.append(neighbor_prox)
        
        return diff
            
        
    def long_similarity(self, graph, wardrobe_index, pieces):
        total_prox = []
        pieces_index = [pieces.index(x) for x in pieces]
        for i in pieces_index:
            prox = []
            piece_prox = graph[i,:] #get the relatedness of that piece with all pieces 
            for j in range(len(wardrobe_index)):
                item_total_prox = graph[:, j].sum() #get the realtedness of the wardrobe item 
                item_prox = piece_prox[j]
                prox.append(item_prox/item_total_prox)
                
            total_prox.append(np.mean(prox))
            
        return total_prox
    

    
    def dif_sim():
        '''
        Will take in an index of articles and
        '''
        
        
    
    
    def long_diff(graph, pieces, wardrobe, counter, iterations):
        key = 'round' + str(counter)
        mast_dict[key] = []
        pieces_lst = []
        for i in pieces: 
            if counter == iterations: 
                piece_prox = graph[i, :] 
            piece_bool = graph[i,:] > 0 
            pieces_index = [i for i, x in zip(range(len(piece_bool)), piece_bool) if x == True]

            if counter < iterations: 
                war_key = 'round_' + str(counter) +"_war_" 
                mast_dict[war_key] = []

            war_lst = []
            for j in wardrobe:
                wardrobe_bool = graph[j,:] > 0
                war_index = [i for i, x in zip(range(len(wardrobe_bool)), wardrobe_bool) if x == True]
                if counter == iterations: 
                    sim_num = piece_prox[j]
                    sim_denom = graph[:, j].sum()
                    item_prox = sim_num/sim_denom
                    diff = np.mean([graph[x, y]/graph[x:].sum() for x in war_index for y in pieces_index])
                    war_lst.append(item_prox * diff)

                elif counter < iterations:
                    long_diff(graph, pieces_index, war_index, counter + 1, iterations)

            if counter == iterations:
                pieces_lst.append(np.mean(war_lst))


            elif counter < iterations: 
                war_key = 'round_' + str(counter) +"_war_"
                pieces_lst.append(np.mean(mast_dict[war_key])) 
                
        loop_mean = np.mean(pieces_lst)

        if counter > 0: 
            war_key = 'round_' + str(counter - 1) +"_war_" 
            mast_dict[war_key].append(loop_mean)


        return pieces_lst

    


    def generate_recs(self, optimal, images):
        
        '''
        Organize optimal purchases into a matrix to be displayd on main page 
        
        Parameters
        ----------
        optimal: dictionary of optimal purchaes created by score_wardrobe 
        images: a dictionary of images that represent the item type being reccomended 
        
        Returns
        -------
        A matrix or dataframe of the images associated with each item in decreasing order of optimality 
        from top left to bottom right

        '''
        
        
        for key in optimal.keys(): #need to know what format is most beneficial here. 
            yield images[key]
        
    

