"""
Recommend
Use data frrom the database to recommend classes to users
"""

import pandas as pd
import numpy as np


def get_sum(data):
    return data.groupby('Email').count()['Class']

def get_taking(data):
    taking = data.copy(deep = True)
    taking['Class_Title'] = data.apply(lambda x: '_'.join([x['Dept'],str(x['Num'])]),axis = 1)
    taking = taking[['Email','Class_Title','Sem']]
    taking = taking.sort_values(['Email','Sem']).reset_index(drop = True)  
    taking['Sem'] = taking.groupby('Email')['Sem'].apply(lambda x: x.map(dict(zip(x,np.unique(x,return_inverse=True)[1]))))
    
    taking.drop_duplicates(['Email','Class_Title'],inplace= True,keep = 'first')
    return taking

def pair_from(mylist):
    return [(i,j) for i in mylist for j in mylist if i < j]

def pair_from_2(user,col1 = 'Class_Idx',col2 = 'Sem'):
    a = user[col1]
    b = user[col2]
    di = dict(zip(a,b))
    return [(i, j, di[j]-di[i]) for i in a for j in a if i < j]

def get_all_courses(data):
    taking = get_taking(data)
    courses = list(taking['Class_Title'].unique())
    courses.sort()
    return courses

# IMPROVED
def all_dist_pairs(data):
    taking = get_taking(data)
    courses = list(taking['Class_Title'].unique())
    courses.sort()
    n = len(courses)
    
    c_to_i = dict(zip(courses,range(n)))
    taking['Class_Idx'] = taking['Class_Title'].map(c_to_i)
    grouped = taking.groupby('Email').apply(lambda x: pair_from_2(x))
    sum_d = np.zeros((n,n))
    count_d = np.zeros((n,n))

    for user in grouped:
        for pair in user:
            #print(pair)
            count_d[pair[0],pair[1]] += 1
            count_d[pair[1],pair[0]] += 1
            sum_d[pair[0],pair[1]] += pair[2]
            sum_d[pair[1],pair[0]] -= pair[2]
    
    i_to_c = dict(zip(range(n),courses))
    
    sum_df = pd.DataFrame(sum_d)
    sum_df.index = sum_df.index.map(i_to_c)
    sum_df.columns = sum_df.columns.map(i_to_c)
    
    count_df = pd.DataFrame(count_d)
    count_df.index = count_df.index.map(i_to_c)
    count_df.columns = count_df.columns.map(i_to_c)
    
    mean_df = sum_df/count_df
    
    return courses,count_df,mean_df

#%% Demos
    
# Input a course title 'ABCD_0000'
# Return a df about courses
# of: classes taken by people who have taken this course; how frequent; Mean and Median distance between the pair
def mean_dist(data, course):

    taking = get_taking(data)
    
    if course not in list(taking['Class_Title'].unique()):
        print('Invalid Course!')
        return None
    
    # People who have taken the course, and when
    taken = taking[['Email','Sem']][taking['Class_Title'] == course]
    taken.columns = ['Email','When']
    
    num = len(taken)
    
    dist = pd.merge(taking,taken, on = 'Email', how = 'left')
    dist['Dist'] = dist['Sem']-dist['When']
    valid_dist = dist.dropna().reset_index(drop = True)
    
     
    out = pd.DataFrame()
    out['Freq'] =  valid_dist.groupby('Class_Title').count()['Email']
    out['Mean_Dist'] = valid_dist.groupby('Class_Title').mean()['Dist']
    out['Med_Dist'] = valid_dist.groupby('Class_Title').median()['Dist']
    out.drop(course, inplace = True) # remove the course itself
    out['Ratio'] = out['Freq']/num
    
    out = out.sort_values('Ratio', ascending = False)
    out = pd.concat([out[out['Med_Dist']>=0.5], out[out['Med_Dist']<0.5]])
    out = out[['Ratio','Freq','Mean_Dist','Med_Dist']]
    
    return out



def when_taken(data, course):
    df = get_taking(data).groupby(['Class_Title','Sem']).count().reset_index('Sem').loc[course]
    #x = df['Sem']
    #y = df['Email']/sum(df['Email'])
    #plt.bar(x,y,color = 'silver')
    #plt.title(course, fontsize=24)
    #plt.show()
    return df

def when_taken_mean(data, courses):
    temp = when_taken(raw, courses)
    temp['Sum'] = temp['Sem']*temp['Email']
    temp = temp.reset_index()
    out = temp.groupby('Class_Title').apply(lambda x: x['Sum'].sum()/x['Email'].sum()).sort_values()
    df = pd.DataFrame(out,columns = ['Sem'])
    df['Count'] = temp.groupby('Class_Title').apply(lambda x: x['Email'].sum())
    return df
    
def sem_dist(data):
    taking = get_taking(data)
    df = taking.groupby(['Sem','Class_Title']).count().reset_index().set_index('Class_Title')
    tot = taking.groupby('Class_Title').count()['Email']
    df['Total'] = tot
    df['Ratio'] = df['Email']/df['Total']
    df = df[['Sem','Ratio','Total']]
    df = df.sort_values(['Sem','Total','Ratio'],ascending = [1,0,0])    
    df = df[df['Total']>=5]
    return df


# TODO: fix dataframe vs. matrix, idx vs. title issue
def dist_based_recommend(data, email, 
                         courses = None, count_df = None, mean_df = None, 
                         sem_lim = 0, lower = 2, upper = 2, mincount = 2):
    taking = get_taking(data)
    
    # Map class titles to indices
    if courses == None or count_df is None or mean_df is None :
        courses, count_df, mean_df = all_dist_pairs(data)

    
    user_take = taking[taking['Email'] == email].drop('Email', axis = 1)[['Class_Title','Sem']]
    user_take = user_take.sort_values('Class_Title').set_index('Class_Title',drop = True)
    user_status = int(user_take.max().loc['Sem'])

    # matrix; rows are classes taken by user, columns are other classes
    user_df = mean_df.loc[user_take.index] 
    user_taken = list(user_df.index)
    user_df = user_df.add(user_take.values, axis = 'columns')
    
    # select relevant classes for next semeter, remove na
    if lower == None: # you could've taken lower semesters ago
        lower = user_status
    user_filter = user_df[user_df >= user_status-lower][user_df <= user_status+upper].dropna(how ='all',axis = 0).dropna(how = 'all',axis = 1)

    rem_classes = user_filter.columns[~user_filter.columns.isin(user_taken)]
    user_filter = user_filter[rem_classes]
    
    
    user_count = count_df.loc[user_take.index]  
    user_count = user_count.loc[user_filter.index][user_filter.columns]
    
    
    # when people usually take this class, >= sem_lim th semester
    if sem_lim == 0:
        sem_lim = user_status/2
    when = when_taken(data,list(user_count.columns))
    when = when[when >= sem_lim]['Sem'].dropna().index.unique()

    # mincount = minimum number of people for crowd source
    user_filter = user_filter[user_count >= mincount].dropna(how = 'all').dropna(how = 'all', axis = 1)
    
    cols = user_filter.columns[user_filter.columns.isin(when)]
    user_filter = user_filter[cols]
    user_count = user_count.loc[user_filter.index][user_filter.columns]
    user_count = user_count[~user_filter.isna()]
    return user_filter, user_count
  



#%% Archived

# Input user email and matching options
# Output peopl who have the most similar background
def match(data, email, sec = False, sem = False):

    # 1 0
    if sec and not sem:
        print('Meaningless match')
        return None
    
    # 1 1
    if sec and sem:  
        classes = data[data['Email']==email]['Class']
        common = data[data['Class'].isin(classes)] # people who have taken classes together before
        ppl = common.groupby('Email').apply(lambda x: x['Class'])

        
    # 0 1
    elif sem:
        combined = data.copy(deep = True)
        combined['Class_Sem'] = data.apply(lambda x: '_'.join([x['Dept'],str(x['Num']),str(x['Sem'])]),axis = 1)
        classes = combined[combined['Email']==email]['Class_Sem']
        common = combined[combined['Class_Sem'].isin(classes)]
        ppl = common.groupby('Email').apply(lambda x: x['Class_Sem'])
        
    # 0 0, default
    elif not sec and not sem:
        combined = data.copy(deep = True)
        combined['Class_Title'] = data.apply(lambda x: '_'.join([x['Dept'],str(x['Num'])]),axis = 1)
        classes = combined[combined['Email']==email]['Class_Title']
        common = combined[combined['Class_Title'].isin(classes)]
        ppl = common.groupby('Email').apply(lambda x: x['Class_Title'])
    

    df = pd.DataFrame(ppl.drop(email)).reset_index()
    df.drop('level_1',axis = 1,inplace = True) # drop previous index column, useless
    df.drop_duplicates(inplace = True)
    df.columns = ['Email','Classes']
    
    all_class_count = get_sum(data)
    user_count = len(classes)
    
    grouped = df.groupby('Email')['Classes']
    out = grouped.apply(' '.join).reset_index()
    out['Count'] = grouped.count().reset_index()['Classes']
    
    out['Total'] = out['Email'].apply(lambda x: all_class_count[x])
    out['Ratio'] = out['Count']/(out['Total'] + user_count - out['Count'])
    
    # arranging, clean up
    out = out.sort_values('Ratio', ascending = False).reset_index(drop = True)
    out['Alias'] =  out['Email'].apply(lambda x: x.split('@')[0])
    out = out[['Alias','Email','Ratio','Count','Classes']]
    #out.drop(columns = 'index',inplace = True)
    
    return out
  