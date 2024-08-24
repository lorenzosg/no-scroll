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
    
    
    def return_pieces(self, optimal, pieces, wardrobe, only_new = True):
        scores = {}
        
        
        for score, item in zip(optimal, pieces):
            if only_new == True: 
                if item not in wardrobe:
                    scores[item] = score
                    
            else:
                scores[item] = score
            
        
        sort_scores = sorted(scores.items(), key=lambda x:x[1], reverse = True)
        dict_scores = dict(sort_scores)
        
            
        return dict_scores
    
    
    def score_wardrobe(self, wardrobe, adj_df, only_new, iterations, method, standard = False, key = 'opt'):
        
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
        dictionary = {}
        graph, pieces = self.build_network(adj_df)
        wardrobe_index = [pieces.index(x) for x in pieces if x in wardrobe]
        pieces_index = range(len(pieces))
        if standard == False:
            scores_dict = self.long_diff(dictionary, graph, pieces_index, wardrobe_index, iterations)
            optimal = scores_dict[key]
        elif standard == True:
            scores_dict = self.standard_scoring(graph, pieces_index, wardrobe_index, method)
            optimal = scores_dict[key]
            
        scores = self.return_pieces(optimal, pieces, wardrobe, only_new)
        
        return scores 
    
        
            
    def similarity(self, graph, pieces_index, wardrobe_index):
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
        wardrobe_graph = graph[:, wardrobe_index]
        similar = []
        for i in pieces_index:
            item_prox = wardrobe_graph[i, :].sum()
            item_total_prox = graph[i, :].sum()
            if item_total_prox > 0:
                wardrobe_prox = item_prox/item_total_prox
            else:
                wardrobe_prox = 0 
            
            similar.append(wardrobe_prox)
        
        return similar
    
    
    def long_difference(self, graph, pieces_index, wardrobe_index):
        pieces_list = []
        for i in pieces_index: 
            piece_neighbs = graph[i, :] > 0 
            piece_neighbs_index = [i for i, x in zip(range(len(piece_neighbs)), piece_neighbs) if x == True]
            
            total_diff = []
            for j in wardrobe_index:
                war_neighbs = graph[j, :] > 0 
                war_neighbs_index = [i for i, x in zip(range(len(war_neighbs)), war_neighbs) if x == True]
                
                diff = []
                for y in piece_neighbs_index:
                    diff.append(np.mean([graph[x, y]/graph[x, :].sum() for x in war_neighbs_index]))
                
                total_diff.append(np.mean(diff))
           
            pieces_list.append(np.mean(total_diff))
         
        return pieces_list
            
        
       
                
        
            

    def difference(self, graph, pieces_index, wardrobe_index):
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
        wardrobe_graph = graph[:, wardrobe_index]
        diff = []
        for i in pieces_index:
            neighbors_i = graph[i, :] > 0 
            neighbors_w = wardrobe_graph.sum(axis = 1) > 0 #gets all pieces which are neighbors with any of the items in the wardrobe
            item_diff = graph[neighbors_i, :][:, neighbors_w].sum() #get the prox between the neighbors of i and the wardrobe
            item_total_diff = graph[neighbors_i, :].sum() #and the total prox between the peice and all others. 
            if item_total_diff > 0:
                neighbor_prox = item_diff/item_total_diff
            else:
                neighbor_prox = 0
            
            diff.append(neighbor_prox)
        
        return diff
            
        
    def long_similarity(self, graph, pieces_index, wardrobe_index):
        total_prox = []
        for i in pieces_index:
            prox = []
            piece_prox = graph[i,:] #get the relatedness of that piece with all pieces 
            for j in wardrobe_index:
                item_total_prox = graph[:, j].sum() #get the realtedness of the wardrobe item 
                item_prox = piece_prox[j]
                prox.append(item_prox/item_total_prox)
                
            total_prox.append(np.mean(prox))
            
        return total_prox
    
    
    def standard_scoring(self, graph, pieces_index, wardrobe_index, method = 'long'):
        
        
        if method == 'long':
            similar = self.long_similarity(graph, pieces_index, wardrobe_index)
            different = self.long_difference(graph, pieces_index, wardrobe_index)
            
        elif method == 'short':
            similar = self.similarity(graph, pieces_index, wardrobe_index)
            different = self.difference(graph, pieces_index, wardrobe_index)
            print(f'elif statement in standard_scoring was executed')
            
        opt = [sim * diff for sim,diff in zip(similar, different)]
        
        scores = {'sim' : similar, 'diff': different, 'opt': opt}
        
        return scores
                
    

    
    
    def long_diff(self, dictionary, graph, pieces, wardrobe, iterations, counter = 0):
        key = 'round' + str(counter)
        dictionary[key] = {'opt': [], 'sim': [], 'diff': []}
        for i in pieces: 
            if counter == iterations: 
                piece_prox = graph[i, :] 
            piece_bool = graph[i,:] > 0 
            pieces_index = [i for i, x in zip(range(len(piece_bool)), piece_bool) if x == True]

            #if counter < iterations: 
            war_key = 'round_' + str(counter) +"_war_" 
            dictionary[war_key] = {'war_sim': [], 'war_diff': [], 'war_opt': []}
   

            for j in wardrobe:
                wardrobe_bool = graph[j,:] > 0
                war_index = [i for i, x in zip(range(len(wardrobe_bool)), wardrobe_bool) if x == True]
                if counter == iterations: 
                    sim_num = piece_prox[j]
                    sim_denom = graph[:, j].sum()
                    item_prox = sim_num/sim_denom
                    dictionary[war_key]['war_sim'].append(item_prox)
                    diff_y = []
                    for y in pieces_index:
                        diff_y.append(np.mean([graph[x, y]/graph[x, :].sum() for x in war_index for y in pieces_index]))
                    diff = np.mean(diff_y)
                    dictionary[war_key]['war_diff'].append(diff)
                    dictionary[war_key]['war_opt'].append(item_prox * diff)

                elif counter < iterations:
                    self.long_diff(dictionary, graph, pieces_index, war_index, iterations, counter + 1)

            if counter == iterations:
                dictionary[key]['opt'].append(np.mean(dictionary[war_key]['war_opt'])) 
                dictionary[key]['sim'].append(np.mean(dictionary[war_key]['war_sim']))
                dictionary[key]['diff'].append(np.mean(dictionary[war_key]['war_diff']))


            elif counter < iterations: 
                war_key = 'round_' + str(counter) +"_war_"
                
                dictionary[key]['opt'].append(np.mean(dictionary[war_key]['war_opt'])) 
                dictionary[key]['sim'].append(np.mean(dictionary[war_key]['war_sim']))
                dictionary[key]['diff'].append(np.mean(dictionary[war_key]['war_diff']))
                
        opt_mean = np.mean(dictionary[key]['opt'])
        sim_mean = np.mean(dictionary[key]['sim'])
        diff_mean = np.mean(dictionary[key]['diff'])

        if counter > 0: 
            war_key = 'round_' + str(counter - 1) +"_war_" 
            dictionary[war_key]['war_opt'].append(opt_mean)
            dictionary[war_key]['war_sim'].append(sim_mean)
            dictionary[war_key]['war_diff'].append(diff_mean)
            

        return dictionary[key]

    


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
        
    

