#Class for testing the efficacy of the algorithm

import reccomend as rec 


class test_recs:
    
    
    def __init__(self):
        self.rec_instance = rec.reccomend()
    
    def static_purchase(self, wardrobe = 'wardrobe', efficient = True, only_new = True, long = False):
        recs = self.rec_instance.score_wardrobe(efficient = efficient, testing = False, only_new = only_new, long = long)
        recs_list = list(recs.keys()) 
        
        return wardrobe[:], recs_list
            
    def dynamic_purchase(self, wardrobe = 'wardrobe', adj_df = 'adj_df', efficient = True, only_new = True, long = False):
        recs = self.rec_instance.score_wardrobe(wardrobe, adj_df, efficient = efficient, testing = True, only_new = only_new, long = long)
        recs_list = list(recs.keys()) 
        wardrobe.append(recs_list[0])
        
        return wardrobe, recs_list
                
        
        
    def complete_fits(self, adj_df = 'adj_df', wardrobe = 'wardrobe'):
        num_fits = 0
        for outfit in adj_df.columns:
            fit = adj_df.loc[:, outfit] > 0
            fit_names = [x for x, y in zip(fit.index, fit.values) if y == True]
            is_whole = set(wardrobe) & set(fit_names)
            if len(is_whole) == len(fit_names):
                num_fits += 1
        
        return num_fits/len(adj_df.columns)
              
 
    
    def distributed(self, adj_df = 'adj_df', wardrobe = 'wardrobe'):
        graph, pieces = self.rec_instance.build_network(adj_df)
        all_edges = []
        for i, item in enumerate(wardrobe):
            
            wardrobe_copy = wardrobe[:]
            piece = wardrobe_copy.pop(i)
            wardrobe_index = [pieces.index(x) for x in wardrobe_copy]
            piece_index = pieces.index(piece)
            edges = graph[piece_index, wardrobe_index]
            all_edges.extend(edges)
            
        return all_edges
    
    
    def num_items(self, wardrobe):
        freq_dict = {}
        for item in wardrobe:
            if item in freq_dict.keys(): 
                freq_dict[item] += 1
            else:
                freq_dict[item] = 1
        
        freq_dict2 = {}
        for num in freq_dict.values():
            if num in freq_dict.keys():
                freq_dict2[str(num)] += 1
            else:
                freq_dict2[str(num)] = 1
 
        return freq_dict2
                
            
     
    def get_results(self, efficient = True, only_new = True, long = False):
        adj_df, wardrobe = self.rec_instance.load_data()
        n = len(adj_df.index) - len(wardrobe) - 1
        fits_dict = {}
        
        fits_static = [] 
        edges_static = []
        static_wardrobe, recs_list = self.static_purchase(wardrobe, efficient, only_new, long)
        
        for i in range(n): #not sure why I can't just run through the whole recs_list here. Not sure why I need to calculate how many recs there are. Maybe change. 
            if recs_list[i] == 0:
                break
        
            static_wardrobe.append(recs_list[i])

           # print(len(wardrobe))
            percent_complete = self.complete_fits(adj_df, static_wardrobe)
            fits_static.append(percent_complete)
            dist_static = self.distributed(adj_df, static_wardrobe)
            edges_static.append(dist_static)
            freq_static = self.num_items(static_wardrobe)
        
            
        fits_dict['fits_static_'] = fits_static
        fits_dict['dist_static_'] = edges_static
        fits_dict['freq_static_'] = freq_static

        fits_dynamic = []
        edges_dynamic = []
        for i in range(n):
            wardrobe, recs_list = self.dynamic_purchase(wardrobe, adj_df, efficient, only_new, long)
            if recs_list[0] == 0:
                break
            print(recs_list)
            percent_complete = self.complete_fits(adj_df, wardrobe)
            dist_dynamic = self.distributed(adj_df, wardrobe)
            fits_dynamic.append(percent_complete) 
            edges_dynamic.append(dist_dynamic)
            freq_dynamic = self.num_items(wardrobe)
            
        fits_dict['fits_dynamic_'] = fits_dynamic
        fits_dict['dist_dynamic_'] = edges_dynamic
        fits_dict['freq_dynamic_'] = freq_dynamic
                
        return fits_dict
        
        
     
 
        
         
        
        
        
        
        