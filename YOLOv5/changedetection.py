import datetime
import pathlib
import cv2
import requests

def add(self, names, detected_current, save_dir, image):
    self.title = ''
    self.text = ''
    change_flag= 0#변화감지플레그
    i = 0
    while i< len(self.result_prev):
        if self.result_prev[i] == 0 and detected_current[i] == 1:
            change_flag =  1
            self.title = names[i]
            self.text += names[i] + ", "
        i += 1 
        self.result_prev = detected_current[:]#객체검출상태저장
        if change_flag == 1:
            self.send(save_dir, image)

def send(self, save_dir, image):
    now = datetime.now()
    now.isoformat()
    
    today = datetime.now()
    save_path = os.getcwd() / save_dir/ 'detected'/ str(today.year) / str(today.month) / str(today.day) 
    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    full_path = save_path/ '{0}-{1}-{2}-{3}.jpg'.format(today.hour,today.minute,today.second,today.microsecond)

    dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
    cv2.imwrite(full_path, dst)
    # 인증이필요한요청에아래의headers를붙임
    headers = {'Authorization': 'JWT '+ self.token, 'Accept': 'application/json'}
    
    # Post Create
    data = {
        'title': self.title, 
        'text': self.text, 
        'created_date': now, 
        'published_date': now}
    file = {'image': open(full_path, 'rb')}
    res = requests.post(self.HOST+ '/api_root/Post/', data=data, files=file, headers=headers)
    print(res)