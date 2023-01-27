import os,subprocess,time,sys,requests,json,time

hours_to_upload=10  #How many hours to upload prior to alarm being triggered
frigate_url="http://10.1.1.2:5000"  #URL:port of frigate installation
gdrive_parent_folder_id="xxxxxxxxxxxxxxxxxxxxxxx" #google drive folder id you can copy from url when in that folder
sent_ids=[]

def convert_epoch(epoch_time):
    time_tuple = time.gmtime(epoch_time)
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday
    hour = time_tuple.tm_hour
    minute = time_tuple.tm_min
    formatted_time = "{}{:02d}{:02d}{:02d}{:02d}".format(year, month, day, hour, minute)
    return formatted_time

def runcmd(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


current_time = time.time()
hours_ago = current_time - (hours_to_upload * 60 * 60)
response=requests.get(frigate_url+"/api/events?after="+str(hours_ago)+"&has_clip=true")
data=json.loads(response.text)

for clip in data:
    id=clip['id']
    camera=clip['camera']
    start_time=convert_epoch(clip['start_time'])
    label=clip['label']
    clip_url=frigate_url+"/api/events/"+id+"/clip.mp4"
    file_path="tmp/"+start_time+"_"+camera+"_"+label+".mp4"
    sent_ids.append(id)
    print ("Uploading",clip_url,"to",file_path)
    r=requests.get(clip_url)
    open(file_path,"wb").write(r.content)
    runcmd("gdrive files upload --parent "+gdrive_parent_folder_id+" "+file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    


running=int(open("gbackup.ini").read())
while running==1:
    current_time = time.time()
    minutes_ago = current_time - (10*60)
    response=requests.get(frigate_url+"/api/events?after="+str(minutes_ago)+"&has_clip=true")
    data=json.loads(response.text)
    for clip in data:
        id=clip['id']
        camera=clip['camera']
        start_time=convert_epoch(clip['start_time'])
        label=clip['label']
        clip_url=frigate_url+"/api/events/"+id+"/clip.mp4"
        file_path="tmp/"+start_time+"_"+camera+"_"+label+".mp4"
        if id not in sent_ids:
            sent_ids.append(id)
            print ("Uploading",clip_url,"to",file_path)
            r=requests.get(clip_url)
            open(file_path,"wb").write(r.content)
            runcmd("gdrive files upload --parent "+gdrive_parent_folder_id+" "+file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
    running=int(open("gbackup.ini").read())
    time.sleep(10)
    
print("Alarm stoped, exiting.")
sys.exit()