import numpy as np

def check_unitable(intervals):
    interv_arr = np.array(intervals)
    idxs = np.array(range(interv_arr.size)).reshape(interv_arr.shape)
    lll =  [np.where(((inf <= interv_arr) & (interv_arr <= sup)) & (idxs//2 != i)) for i, (inf, sup) in enumerate(interv_arr)]
    intersection_ref = [(i, x[0]) for i, x in enumerate(lll) if x[0].size!=0 and x[1].size!=0]
    
    return intersection_ref

def intervals_union(intervals):
    interv_arr = np.array(intervals)
    intersection_ref = check_unitable(intervals)
    new_lims = set(intervals)
    new_idx = {}

    if intersection_ref:        
        for k in intersection_ref:
            i, (idx, *_) = k
        
            temp1, temp2 = interv_arr[i], interv_arr[idx]
            if tuple(temp1) in new_idx.keys():
                temp1 = new_idx[tuple(temp1)]
            if tuple(temp2) in new_idx.keys():
                temp2 = new_idx[tuple(temp2)]

            inf, sup = temp1
            inf2, sup2 = temp2

            if inf2 < inf:
                inf = inf2
            if sup2 > sup:
                sup = sup2
            
            new_idx[tuple(temp1)] = (inf, sup)
            new_idx[tuple(temp2)] = (inf, sup)
            new_lims.discard(tuple(temp1))
            new_lims.discard(tuple(temp2))
            new_lims.add((inf, sup))

        new_lims = list(new_lims)
        new_lims.sort(key=lambda x: x[0])
        new_lims = intervals_union(new_lims)
    else:
        new_lims = intervals
    
    return new_lims

def sum_of_intervals(intervals):
    intervals = intervals_union(intervals)
    length = sum([x[1] - x[0] for x in intervals])
    return length
    

#%%
intervals = [(-493, 70), (373, 484), (410, 415), (-274, 9), (-433, -276), (-102, 478), (-249, 268)]
sum_of_intervals(intervals)
