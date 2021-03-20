""" all functions:
[Display events]
        select_event(self, tags) WORKS
            eid_by_likes(self) WORKS
            get_event(self, eid) WORKS
        recommend_for_user(self, uid) WORKS

[One event]
        num_likes(self, eid) WORKS
        who_likes(self, eid) WORKS

[Use Info]
        insert_user(self, bio) WORKS
        get_user_bio(self, uid) WORKS
        edit_bio(self, uid) WORKS

[Manage events]
        insert_event(self, event, organizer) WORKS
        my_events(self, uid) WORKS
        edit_event(self, eid) WORKS
        add_tags(self, tags, event) WORKS
            new_tag(self, tag_name) WORKS
            get_tid(self, tag_name) WORKS
            tags_by_freq(self) WORKS
        delete_event(self, uid) WORKS
        get_event_tags(self, eid) WORKS
        remove_tags(self, eid, tids) WORKS
            delete_tag_all(self, tid, tag) WORKS (probably not used at all) 
        
[User Preferences]           
        like_event(self, uid, eid) WORKS       
        my_likes(self, uid) WORKS
        unlike_event(self, uid, eid) WORKS
        interest_tag(self, uid, tids) WORKS
        my_interests(self, uid) WORKS
        uninterest_tags(self, uid, tids) WORKS
        

        
"""

# TEST insert_requirement
# sample user string input
# {"requirement": "", "dept": , "code": , "function": "", "further_spec": ""}
r1 =  {"requirement": "CS", "dept": "COMS" , "code": "COMS_W1004", "function": "major", "further_spec": "CC"}
r2 =  {"requirement": "CS", "dept": "COMS" , "code": "COMS_W3134", "function": "major", "further_spec": "CC"}
r3 =  {"requirement": "CS", "dept": "COMS" , "code": "COMS_W3137", "function": "major", "further_spec": "CC"}
reqs =[r1,r2,r3]
for req in reqs:
    print(sess_db.insert_requirement(req))


# TEST insert_user 
# sample user string input
# {"name": "", "UNI": , "school":, "email":, "year":}

u1 = {"name": "user1", "UNI":"u1", "school":"CC", "email":"confuseduser1@columbia.edu","year":"1111"}
u2 = {"name": "user2", "UNI":"u2", "school":"CC", "email":"happyuser2@columbia.edu", "year":"2222"}
u3 = {"name": "user3", "UNI":"u3", "school":"SEAS", "email":"saduser3@columbia.edu", "year":"2222"}
u4 = {"name": "user4", "UNI":"u4", "school":"CC", "email":"loluser4@columbia.edu", "year":"2222"}
u5 = {"name": "user5", "UNI":"u5", "school":"GS", "email":"whoamiuser5@columbia.edu", "year":"2222"}
u6 = {"name": "user6", "UNI":"u6", "school":"Barnard", "email":"dpiuser6@columbia.edu", "year":"2222"}
u7 = {"name": "user7", "UNI":"u7", "school":"SEAS","email":"testuser7@columbia.edu", "year":"2222"}
u8 = {"name": "ddppii", "UNI":"dpi123", "school":"SEAS","email":"ddppii@columbia.edu", "year":"3333"}

users = [u1,u2,u3,u4,u5,u6,u7,u8]
for user in users:
    print(sess_db.insert_user(user))




# TEST insert_event 
# sample event string input
# {"title":" ", "location": " ", "timestamp": "2020-04-01 00:00:00", "description":" ", "link":" "}
e1 = {"title":"April Fools Party", "location": "Zoom", "timestamp": "2020-04-01 00:00:00", "description":"You are fooled!", "link":"https://aprilfools.com"}
e2 = {"title":"Escape the Zoom", "location": "Zoom", "timestamp": "2020-04-02 20:00:00", "description":"Escape the Zoom with your friends", "link":"https://bit.ly/zoom"}
e3 = {"title":"Event 3", "location": "333", "timestamp": "2020-04-03 03:00:00", "description":"third test event", "link":"https://event3.com"}
e4 = {"title":"Event 4", "location": "444", "timestamp": "2020-04-04 04:00:00", "description":"fourth test event", "link":"https://event4.com"}
e5 = {"title":"Event 5", "location": "555", "timestamp": "2020-04-05 05:00:00", "description":"fifth test event", "link":"https://event5.com"}
e6 = {"title":"Event 6", "location": "666", "timestamp": "2020-04-06 06:00:00", "description":"sixth test event", "link":"https://event6.com"}
e7 = {"title":"Event 7", "location": "777", "timestamp": "2020-04-07 07:00:00", "description":"seventh test event", "link":"https://event7.com"}
e8 = {"title":"Event 8", "location": "888", "timestamp": "2020-04-08 08:00:00", "description":"eighth test event", "link":"https://event8.com"}
e9 = {"title":"Event 9", "location": "999", "timestamp": "2020-04-09 09:00:00", "description":"ninth test event", "link":"https://event9.com"}
e10 = {"title":"Event 10", "location": "101010", "timestamp": "2020-04-10 10:00:00", "description":"tenth test event", "link":"https://event10.com"}
e11 = {"title":"Final Exam", "location": "Columbia", "timestamp": "2020-05-12 10:00:00", "description":"You passed the final", "link":"https://final.com"}
e12 = {"title":"DPI Expo", "location": "Zoom", "timestamp": "2020-05-06 20:00:00", "description":"Come and take a look", "link":"https://dpidpidpidpi.com"}

evs = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]
for ev in evs:
    print(sess_db.insert_event(ev, 2))



# TEST add_tags, new_tag and get_tid works
tev1 = ["party", "social", "free food", "online","stupid"]
tev2 = ["social", "online"]
tev3 = ["tech", "resume drop", "professional"]
tev4 = ["tech", "free food", "online"]
tev5 = ["free food", "professional", "finance", "social", "resume drop"]
tev6 = ["art", "concert", "choir", "free food", "social"]
tev7 = ["sports", "social", "varsity"]
tev8 = ["stupid", "useless"]
tev9 = ["online", "club meeting", "tech", "panel"]
tev10 =["club meeting", "social", "party", "free food"]

tevs = [tev1, tev2, tev3, tev4, tev5, tev6, tev7, tev8, tev9, tev10]
num = 10
for tev in tevs:
    print(sess_db.add_tags(num, tev))
    num += 1

tev11 = ["academic", "party", "challenge"]
print(sess_db.add_tags(20,tev11))

tev12 = ["club meeting", "online", "tech", "study break", "academic"]
print(sess_db.add_tags(21,tev12))



# TEST show tags
res = sess_db.tags_by_freq()
for r in res:
    print(r)




# TEST select_event, get_event and eid_by_likes
# test1
print("test1:")
tev1 = ["party", "social", "free food", "online","stupid"]
res = sess_db.select_event(tev1)
for r in res:
    print(r)

# test 2
print("test2:")
res = sess_db.select_event(["useless"])
for r in res:
    print(r)

# test 3
print("test3:")
res = sess_db.select_event(["stupid"])
for r in res:
    print(r)
    
# test 4
print("test4:")
res = sess_db.select_event(["social"])
for r in res:
    print(r)

# test 5
print("test5:")
res = sess_db.select_event([])
for r in res:
    print(r)



# TEST eid_by_likes
print(sess_db.eid_by_likes())



# TEST interest_tag
# online x4,  tech x4, social x3, free food x2, finance x2, party x2, sports x3, varsity x2, 
# resumedrop x1, art x1, panel x1, professional x1, club meeting x1,
# stupid x0, useless x0
"""
ut1 = ["social","online","tech"]
ut2 = ["free food", "tech", "online"]
ut3 = ["tech", "finance", "party", "social","resume drop"]
ut4 = ["art","online","choir","concert"]
ut5 = ["sports", "varsity"]
ut6 = ["sports, varsity"]
ut7 = ["online", "sports" "social", "free food", "party", "tech", "resume drop", "panel", "professional", "club meeting", "finance"]
"""
ut1 = [12,13,2]
ut2 = [1, 2, 13]
ut3 = [2 ,16, 9, 12, 15]
ut4 = [5,13,18,17]
ut5 = [8, 19]
ut6 = [8, 19]
ut7 = [13, 8, 12, 1, 9, 2, 15, 22, 3, 21, 16]

uts = [ut1,ut2,ut3,ut4,ut5,ut6,ut7]
num = 2
for ut in uts:
    print(sess_db.interest_tag(num,ut))
    num += 1



# TEST like 
ues = [20, 10, 2, 10, 12, 14, 20]
num = 2
for ue in ues:
    print(sess_db.like_event(num,ue))
    num += 1
for u in range(2, 9, 1):
    print(sess_db.like_event(u,21))
    num += 1



# TEST my_likes
for u in range(2, 9, 1):
    print("user " + str(u) + " likes: ")
    res = sess_db.my_likes(u)
    for r in res:
        print(r)



# TEST num_likes
for e in range(10, 22, 1):
    res = sess_db.num_likes(e)
    print("event " + str(e) + " is liked by " + str(res) + " people.")



# TEST who_likes
for e in range(10, 22, 1):
    res = sess_db.who_likes(e)
    print("event " + str(e) + " is liked by :")
    print(res)



# TEST get_event_tags
for e in range(10, 22, 1):
    res = sess_db.get_event_tags(e)
    print("event " + str(e) + " is has tags :")
    print(res)



# TEST my_interests
print(sess_db.my_interests(3))



# TEST recommend_for_user
res = sess_db.recommend_for_user(3)
for r in res:
    print(r)



# TEST remove_tags
print(sess_db.get_event_tags(20))
sess_db.remove_tags(20, [9,23])
print(sess_db.get_event_tags(20))



# TEST get_user_bio and edit_bio
u1 = {"name": "Very Confused", "UNI":"vc1", "school":"CC", "email":"confuseduser1@columbia.edu","year":"2020"}
sess_db.edit_bio(3,u1)
print(sess_db.get_user_bio(3))



# TEST edit_event
e3 = {"title":"Google Workshop", "location": "Lerner", "timestamp": "2020-05-10 19:00:00", "description":"Gooooooogle", "link":"https://google.com"}
sess_db.edit_event(12)
print(sess_db.get_event(12))



# TEST unlike_event
# user 3 unlike event 10
print(sess_db.who_likes(10))
print(sess_db.my_likes(3))
print(sess_db.unlike_event(3, 10))
print(sess_db.who_likes(10))
print(sess_db.my_likes(3))  


# TEST uninterest_tags
print(sess_db.my_interests(4)) # [2, 16, 9, 12, 15]
sess_db.uninterest_tags(4, [2,16])
print(sess_db.my_interests(4)) # [9, 12, 15]


