#-*- coding: utf-8 -*-


#要跑起demo请填上以下的几个值，包括API_KEY和API_SECRET，两个本地文件的图片
API_KEY = ""#API_KEY
API_SECRET = ""#API_SECRETַ
face_one = ""#网络图片的URL地址,调用demo前请填上内容 Network picture of the URL address, call demo before you fill in the content
face_two = ""#本地图片的地址,调用demo前请填上内容  local pictures address, please fill in the contents before calling demo
face_search = ""#本地图片的地址,调用demo前请填上内容  local pictures address, please fill in the contents before calling demo




from pprint import pformat
def print_result(hit,result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v):encode(k) for (v,k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        
    print hit
    result = encode(result);
    print '\n'.join("  " + i for i in pformat(result, width = 75).split('\n'))


from facepp import API, File

api = API(API_KEY, API_SECRET)

#1.创建一个Faceset用来存储FaceToken
#1.create a Faceset to save FaceToken
ret = api.faceset.create(outer_id = 'test')
print_result("faceset create", ret)

#2.对图片进行检测
#2.detect image
Face = {};
res = api.detect(image_url = face_one)
print_result("person_one", res)
Face['person_one'] = res["faces"][0]["face_token"]

res = api.detect(image_file = File(face_two))
print_result("person_two", res)
Face['person_two'] = res["faces"][0]["face_token"]

#3.将得到的FaceToken存进Faceset里面
#3.save FaceToken in Faceset
api.faceset.addface(outer_id = 'test', face_tokens = Face.itervalues())

#4.对待比对的图片进行检测，再搜索相似脸
#4.detect image and search same face
ret = api.detect(image_file = File(face_search))
print_result("detect", ret)
search_result = api.search(face_token = ret["faces"][0]["face_token"], outer_id = 'test')

#5.输出结果
#5.print result
print_result('search', search_result)
print '=' * 60
for k,v in Face.iteritems():
    if v == search_result['results'][0]['face_token']:
        print 'The person with highest confidence:', k
        break


#6.删除无用的人脸库
#6.delect faceset because it is no longer needed
api.faceset.delete(outer_id = 'test', check_empty = 0)

# Congratulations! You have finished this tutorial, and you can continue
# reading our API document and start writing your own App using Face++ API!
# Enjoy :)
# 恭喜！您已经完成了本教程，可以继续阅读我们的API文档并利用Face++ API开始写您自
# 己的App了！
# 旅途愉快 :)
