from os import defpath
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import datetime
import sys
from selenium.webdriver.support.wait import WebDriverWait

user_id="your-insta-id"    # instagram id  
user_passwd="your-insta-passwd"  # instagram password 
instagram_login_btn="#loginForm > div > div:nth-child(3) > button > div"    # instagram login button css selector
driver_path="your-driver-path"    # driver path

#------------- instagram login start -------------
print("login start!")
login_url = "https://www.instagram.com/accounts/login/"
driver = wd.Chrome(driver_path)
driver.get(login_url)
time.sleep(10)
try:    
    # username, userpasswd 입력 후 로그인 버튼 클릭
    instagram_id_form = driver.find_element_by_name("username")
    instagram_id_form.send_keys(user_id)
    time.sleep(5)

    instagram_pw_form = driver.find_element_by_name("password")
    instagram_pw_form.send_keys(user_passwd)
    time.sleep(7)

    login_ok_button = driver.find_element_by_css_selector(instagram_login_btn)
    login_ok_button.click()
    print("instagram login success")
except:
    print("instagram login fail")
    exit()
#------------- instagram login end --------------

#------------- load influencer data -------------
# 제공된 데이터 파일로부터 인플루언서 계정명들 가져오기
df = pd.read_csv("your-influencer-data")

cat = df['인스타그램 계정']
cat_val = cat.values
addresses = cat_val.tolist()
#-------------- load influencer data end ------------

#-------------- required variables ------------------
jumpedCount = 0 # 제한된 계정이 있어서 건너뛴 횟수
check_arrow = True # 다음 게시물이 있는가? 
first_img_css="div.v1Nh3.kIKUG._bz0w"
date_object_css="div.k_Q0X.NnvRN > a.c-Yi7 > time._1o9PC.Nzb55"
comment_more_btn="body > div._2dDPU.QPGbb.CkGkG > div._32yJO > div > article > div > div.HP0qD > div > div > div.eo2As > div.EtaWk > ul > li > div > button > div > svg"
comment_ids_objects_css="ul.Mr508 > div.ZyFrc > li.gElp9.rUo9f > div.P9YgZ > div.C7I1f > div.C4VMK > h3"
comment_texts_objects_css="ul.Mr508 > div.ZyFrc > li.gElp9.rUo9f > div.P9YgZ > div.C7I1f > div.C4VMK > span"
upload_id_object_css="body > div._2dDPU.QPGbb.CkGkG > div._32yJO > div > article > div > div.HP0qD > div > div > div.UE9AK > div > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.e1e1d > span > a"
next_arrow_btn_css2="body > div._2dDPU.QPGbb.CkGkG > div.EfHg9 > div > div > div.l8mY4 > button > div > span > svg"
next_arrow_btn_css1="body > div._2dDPU.QPGbb.CkGkG > div.EfHg9 > div > div > div > button > div > span > svg"
comment_write_btn="body > div._2dDPU.QPGbb.CkGkG > div._32yJO > div > article > div > div.HP0qD > div > div > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button"
like_indicator_css="body > div._2dDPU.QPGbb.CkGkG > div._32yJO > div > article > div > div.HP0qD > div > div > div.eo2As > section.EDfFK.ygqzn > div > div > a > span"
hided_like_indicator_css="body > div._2dDPU.QPGbb.CkGkG > div._32yJO > div > article > div > div.HP0qD > div > div > div.eo2As > section.EDfFK.ygqzn > div > div.Nm9Fw > a"
#-------------- 필요 변수들 생성 끝 -----------------------

# 최종 아웃풋 딕셔너리 
output_dict = {
    'user_id': [],
    'insta_url': [],
    'follower_num': [],
    'media_count_public': [],
    'media_count_private': [],
    'comment_count': [],
    'like_count': [],
    'profile_image_source': []
}

# 데이터에 있는 각 url들에 대해서 크롤링 해보기
# 필요 데이터 : 팔로워 수, 계정명, 최근 45일간 총 게시글 숫자, 최근45일간 게시글 좋아요 수 합계, 최근 45일간 게시글 댓글 수 합계, 최근 45일간 댓글에서 언급(@) 수 합계, 성별, 이름
# 프로토타입 제작을 위해 간소화된 데이터 뽑기
# user_id, 팔로워 수, 최근45일간 총 게시글, 최근 45일간 총 좋아요 수, 최근 45일간 총 댓글 수
# jumpedCount = 0

start_index = 3770   # 시작 인덱스 1918
end_index = 3835  # 끝 인덱스 3835
today = datetime.datetime.now() # 현재 시각으로부터 게시글 크롤링 시작

for i in range(start_index, end_index):
    print('currentIndex = ', i)
    
    # url 요청
    time.sleep(10)
    driver.get(addresses[i])
    time.sleep(10)

    # 해당 인플루언서의 팔로워 데이터 가져오기
    try:
        followers = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'))).get_attribute("title")
        #followers = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute("title")
        output_dict['follower_num'] = int(followers.replace(',', ''))
        print('followers_count: ', followers)
    except:
        # 페이지에서 팔로워 수 가져올 수 없다는 것은 제한된 계정이기 때문에 건너뜀
        print('followers_count collect failed')
        jumpedCount += 1    # 계정을 건너뛴 횟수 추가
        continue

    # 해당 인플루언서의 user_id 가져오기
    try:
        user_id = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > div.nZSzR')))
        #user_id = driver.find_element_by_css_selector('#react-root > section > main > div > header > section > div.nZSzR')
        user_id = user_id.find_element(By.CLASS_NAME, '_7UhW9.fKFbl.yUEEX.KV-D4.fDxYl')
        #user_id = driver.find_element_by_css_selector('#react-root > section > main > div > header > section > div.nZSzR > h2')
        user_id = user_id.text
        output_dict['user_id'] = user_id
        print('user_id: ', user_id)
    except:
        print('user_id collect failed')
        print(i - 1, '번 인플루언서까지 크롤링되었습니다')
        break

    # 해당 인플루언서의 프로필 사진 이미지 소스 가져오기
    try:
        '#react-root > section > main > div > header > div > div > span > img'
        profile_image_source = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > div > div > span > img'))).get_attribute('src')
        #profile_image = driver.find_element(By.CSS_SELECTOR, '#react-root > section > main > div > header > div > div > div > button > img').get_attribute('src')
        output_dict['profile_image_source'] = profile_image_source
        print('profile image source:', profile_image_source)
    except:
        print('profile source collect failed')
        print(i-1, '번 인플루언서까지 크롤링되었습니다')
        break

    # 해당 인플루언서의 insta_url 저장하기
    try:
        insta_url = addresses[i]
        output_dict['insta_url'] = insta_url
        print('insta_url : ', output_dict['insta_url'])
    except:
        print('insta_url collect fail')
        print(i - 1, '번 인플루언서까지 크롤링되었습니다')
        break

    # 해당 인플루언서의 최근 45일간 게시글 수, 45일간 코멘트 수, 45일간 좋아요(동영상 뷰) 수 가져오기
    # 각 사진별로 정보 접근 시작
    total_post_llist = []
    likeCount = 0
    commentCount = 0
    mediaCount_private = 0
    mediaCount_public = 0
    date_texts = []
    isDateValid = True
   
    while isDateValid:
        post_list = driver.find_elements(By.CLASS_NAME, "v1Nh3.kIKUG._bz0w") #"_9AhH0"
        post_list = [post for post in post_list if post not in total_post_llist]
        total_post_llist += post_list
        # 더 이상 가져올 게시글이 없다면 while문 빠져나가기
        if len(post_list) == 0:
            print('no more post to get')
            break

        # 전체 게시글 중 post들 가져오기
        for post in post_list:
            # 각 post마다
            # 게시글을 클릭하여 게시글 날짜 확인
            time.sleep(5)
            try:
                #post.find_element(By.CLASS_NAME, '_9AhH0')
                media = post.find_element(By.CLASS_NAME, '_9AhH0')
                driver.execute_script('arguments[0].click();', media)
            except:
                print('media click failed')
                isDateValid = False
                break
            time.sleep(4)
            # 45일 이후의 게시글일 경우 post 탐색 중지
            try:
                date_object = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, date_object_css)))
                #date_object = driver.find_element_by_css_selector(date_object_css)
                date_text = datetime.datetime.strptime(date_object.get_attribute("title"), "%Y년 %m월 %d일")
                print(date_text)
                print('date_text collected')
                if today - date_text >= datetime.timedelta(days=45):
                    print('max date reached, searching next influencer')
                    isDateValid = False
                    break 
                else:
                    print('max date not reached yet')
            except:
                # date text가 수집되지 않는 것은 나쁜 신호
                # 프로그램을 정지
                print('date_text collect failed')
                sys.tracebacklimit = 1
                raise ValueError()
            
            # 45일 이전의 게시글일 경우 클릭한 게시글 종료
            try:
                exit_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div._2dDPU.QPGbb.CkGkG > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button')))
                #exit_button = driver.find_element_by_css_selector('body > div._2dDPU.QPGbb.CkGkG > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button')
                time.sleep(3)
                driver.execute_script('arguments[0].click();', exit_button)
                #exit_button.click() 
                print('closing media success')
            except:
                try:
                    exit_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div._2dDPU.CkGkG > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button')))
                    #exit_button = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button')
                    time.sleep(3)
                    driver.execute_script('arguments[0].click();', exit_button)
                    #exit_button.click() 
                    print('closing media success')
                except:
                    print('closing media failed')

            time.sleep(4)

            # 마우스 올려놓고 좋아요 수, 댓글 수 수집
            try:
                # 마우스 올려놓기
                hover = ActionChains(driver)
                driver.execute_script('arguments[0].scrollIntoView(true);', post)
                hover.move_to_element(post.find_element(By.CLASS_NAME, '_9AhH0')).perform()
                isHover = False
                
                # hover element가 있는지 확인 ( 좋아요, 댓글이 숨겨져 있으면 hover element가 나타나지 않음)
                try:
                    driver.find_element_by_class_name('-V_eO')
                    isHover = True
                except NoSuchElementException:
                    isHover = False

                # Hover element가 있을 때만 아래 액션 수행
                if isHover == True:
                    #print('likes and comments are public')
                    # 좋아요 수, 댓글 수 수집하고 mediaCount 증가시켜주기
                    peads = post.find_elements(By.CLASS_NAME, '-V_eO')
                    
                    # 좋아와 comment가 모두 public인 경우에만 데이터 가져오기
                    if len(peads) == 2:
                        print('likes and comments are public')
                        likeCount += int(peads[0].text.replace(',', ''))
                        commentCount += int(peads[1].text.replace(',', ''))
                        print('likes: ', peads[0].text, 'comments: ', peads[1].text, 'media_public:', mediaCount_public, 'media_private:', mediaCount_private)
                        mediaCount_public += 1
                    # like만 있는 경우에는 private으로 처리, media_count_private만 증가시킨다.
                    else:
                        print('like or comment is private')
                        mediaCount_private += 1
                    """
                    elif len(peads) == 1:
                        print('likes:', peads[0].text, 'medias:', mediaCount, 'no comments for this media')
                    print('total likes:', likeCount, 'total comments:', commentCount, 'total medias:', mediaCount)
                    """
                else:
                    print('likes and comments are private')
                    mediaCount_private += 1
                    # like도 comment도 숨겨져 있으면 그냥 지나가기
                    #elif len(peads) == 0:
                    #print('no like or comment... ')
            except:
                print('like and comment count collect failed')
            
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('scroll executed')
        time.sleep(5)

    # 크롤링한 결과 csv 파일에 저장하기
    output_dict['media_count_public'] = mediaCount_public
    output_dict['media_count_private'] = mediaCount_private
    output_dict['like_count'] = likeCount
    output_dict['comment_count'] = commentCount

    print(output_dict)

    insta_info_df = pd.read_csv('insta_info.csv', index_col=0)
    insta_info_df.loc[i] = output_dict
    insta_info_df.to_csv('insta_info.csv')

driver.close()
driver.quit()