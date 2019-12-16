from Error import AccessError, ValueError_http
from data_structure import getData, getUserByEmail, getUserFromToken, getUserById, getUserByHandle
import re
# for imgDownload
import urllib.request
import requests
import sys
# for cropping
from PIL import Image

image_name = 0
#def get_x_y():
#    global x1, y1, x2, y2
#    return x1, y1, x2, y2


def user_profile(token, u_id):
    valid_userT = getUserFromToken(token)
    valid_userU = getUserById(u_id)
      
    return ({
        'u_id' : valid_userU['u_id'],
        'email' : valid_userU['email'],
        'name_first' : valid_userU['name_first'],
        'name_last' : valid_userU['name_last'],
        'handle_str' : valid_userU['handle_str'],
        'profile_img_url' : valid_userU['profile_img_url'],
    })

def user_profile_setname(token, name_first, name_last):
    validUserT = getUserFromToken(token)
    if len(name_first) > 50:
        raise ValueError_http("Invalid name_first, above the range of 50 characters")
    if len(name_last) > 50:
        raise ValueError_http("Invalid name_last, above the range of 50 characters")    
    if validUserT != None:
        validUserT['name_first'] = name_first
        validUserT['name_last'] = name_last
    return ({})


def user_profile_setemail(token, email):
    data = getData()
    #'''Email entered is not a valid email''' 
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError_http("Invalid email")
    # if getUserByEmail(email) != None:
    for user in data['users']:
        if user['email'] == email:
            raise ValueError_http("Email address is already being used by another user")
    found_user = getUserFromToken(token) 
    found_user['email'] = email
    return ({})


 
def user_profile_sethandle(token, handle_str):
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise ValueError_http("handle_str should be between 3-20 characters")  
    if getUserByHandle(handle_str) != None:
        raise ValueError_http("handle_str is already being used by another user")
    found_user2 = getUserFromToken(token)
    found_user2['handle_str'] = handle_str
    return ({})

# for iteration 3
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    global image_name
    image_name += 1
    filePath = './static/' + str(image_name) +'.jpg'

    downloadImage(img_url, filePath)
    
    #crop image
    img_obj = Image.open(filePath)
    width, height = img_obj.size
    #no input
    if x_start is None and x_end is None and y_start is None and y_end is None:
        x_start = 0
        x_end = width
        y_start = 0
        y_end = height
    
    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)

    #x_start and y_start has to be less than width and hight
    if x_end > width or y_end > height or x_start >= x_end or y_start >= y_end:
        raise ValueError_http(f"Crop has to be within the dimension ({width} x {height})")
    cropped = img_obj.crop((x_start,y_start,x_end,y_end))
    #save cropped image
    filePath_cropped = './static/' + str(image_name) +'_cropped'+'.jpg'
    #print(final_url)
    cropped.save(filePath_cropped)
    
    final_url = 'http://localhost:'+sys.argv[1]+'/static/'+str(image_name) + '_cropped.jpg'
    getUserFromToken(token)['profile_img_url'] = final_url




 
def sendRequest(url):
    try:
        page = requests.get(url, stream = True, timeout = 1)

    except Exception as e:
        print("error:", e)
        return False

    # check status code
    if (page.status_code != 200):
        return False

    return page

def downloadImage(imageUrl: str, filePath: str):
    img = sendRequest(imageUrl)

    if (img == False):
        raise AccessError("Please enter a valid URL (image has to be .jpg)")

    if not img.content[:4] == b'\xff\xd8\xff\xe0': raise ValueError_http("Please enter a valid URL (image has to be .jpg)")

    urllib.request.urlretrieve(imageUrl, filePath)



def users_all(token):
    data = getData()
    foundUser = getUserFromToken(token)
    all_users = []
    for user in data['users']:
        user_dic = {
            'u_id' : user['u_id'],
            'email' : user['email'],
            'name_first' : user['name_first'],
            'name_last' : user['name_last'],
            'handle_str' : user['handle_str'],
            'profile_img_url' : user['profile_img_url']
        }
        all_users.append(user_dic)

    return {
        'users' : all_users,
    }
